import sys

import re

import gitlab
import subprocess

import argparse

import tempfile

import yaml
from typing import Type, Protocol, Dict, List, Optional

import abc
import os
import addons_installer
from .aflred_dc import get_random_string, DockerComposeService, DatabaseDockerComposeService, DatabaseCredential, \
    DockerComposeFile, DockerImage
from python_on_whales import DockerClient
from ndp_utils import gitlab_utils, env_utils

RE_ERROR = re.compile(r"(?:\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \d+ (?:FATAL|CRITICAL) )|(: FAILED)$", re.M)
RE_WARNING = re.compile(r'\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \d+ WARNING ', re.M)


class RunbotEnvironment(gitlab_utils.GitlabCIVars):

    def __init__(self, environ: Dict[str, str] = None):
        super(RunbotEnvironment, self).__init__(environ)
        # In case there is no GITLAB_USER_NAME we preset to "gitlab-ci-token"
        # see https://docs.gitlab.com/ee/ci/jobs/ci_job_token.html
        self.add_addons_git_default()

    def add_addons_git_default(self):
        self.environ["CI_DEPLOY_USER"] = self.get_value(["CI_DEPLOY_USER"], default="gitlab-ci-token")
        self.environ["ADDONS_GIT_DEFAULT_PROTOCOLE"] = self.get_value(["ADDONS_GIT_DEFAULT_PROTOCOLE"], default="https")
        self.environ["ADDONS_GIT_DEFAULT_HTTPS_LOGIN"] = self.get_value(["ADDONS_GIT_DEFAULT_HTTPS_LOGIN"], default=self.CI_DEPLOY_USER)
        self.environ["ADDONS_GIT_DEFAULT_HTTPS_PASSWORD"] = self.get_value(["ADDONS_GIT_DEFAULT_HTTPS_PASSWORD"],  default=self.CI_DEPLOY_PASSWORD or self.CI_JOB_TOKEN)
        if self.PATH_DOCKER_COMPOSE == tempfile.gettempdir():
            self.environ["PATH_DOCKER_COMPOSE"] = os.path.join(self.get_value(['PATH_DOCKER_COMPOSE'], default=tempfile.gettempdir()), self.UNIQUE_ID)

    @property
    def UNIQUE_ID(self) -> str:
        return "job-" + (self.CI_JOB_ID or get_random_string(5))

    @property
    def default_ODOO_MODULE(self) -> str:
        return ("%s_erp" % self.CI_PROJECT_PATH.replace('-', '_')).lower()

    @property
    def ODOO_VERSION(self) -> str:
        return self.get_value(['ODOO_VERSION'])

    @property
    def ODOO_DEPENDS(self) -> str:
        return self.get_value(['ODOO_DEPENDS'])

    @property
    def PATH_DOCKER_COMPOSE(self) -> str:
        return self.get_value(['PATH_DOCKER_COMPOSE'], default=tempfile.gettempdir())

    @property
    def POSTGRES_IMG_VERSION(self) -> str:
        return self.get_value(['POSTGRES_IMGAGE_TAG'], default="13")

    @property
    def BEFORE_ODOO_MODULE(self) -> str:
        return self.get_value(['BEFORE_ODOO_MODULE'])

    @property
    def ODOO_MODULE(self) -> str:
        return self.get_value(['ODOO_MODULE'], default=self.default_ODOO_MODULE)

    @property
    def WORKERS(self) -> int:
        """
        Threaded Mode ?
        :return: 0 by default
        """
        return 0

    @property
    def NEW_SPEC_ODOO_DEPENDS(self) -> bool:
        return env_utils.is_true(self.get_value(["NEW_SPEC_ODOO_DEPENDS"]))

    def get_value(self, possible_value: List[str], default: str = None):
        return env_utils.get_value(possible_value=possible_value, env_vars=self.environ, default=default)

    def print_info_running(self):
        res = []
        res.append(f"CI_API_V4_URL => {self.CI_API_V4_URL}")
        res.append(f"CI_PROJECT_PATH => {self.CI_PROJECT_PATH}")
        res.append(f"ODOO_VERSION => {self.ODOO_VERSION}")
        res.append(f"PATH_DOCKER_COMPOSE => {self.PATH_DOCKER_COMPOSE}")
        res.append(f"POSTGRES_IMG_VERSION => {self.POSTGRES_IMG_VERSION}")
        res.append(f"ODOO_MODULE => {self.ODOO_MODULE}")
        res.append(f"BEFORE_ODOO_MODULE => {self.BEFORE_ODOO_MODULE}")
        res.append(f"CI_JOB_TOKEN => {self.CI_JOB_TOKEN and '*' * len(self.CI_JOB_TOKEN)}")
        if self.NEW_SPEC_ODOO_DEPENDS:
            res.append("Other git repo:")
            for addon_def in addons_installer.AddonsRegistry().parse_env(self.environ):
                res.append(" ".join(addon_def.arg_cmd()))
        elif self.ODOO_DEPENDS:
            res.append("Other git repo:")
            res.extend(self.ODOO_DEPENDS.split(","))
        print("\n".join(res))



class InteractiveRunbotEnvironment(RunbotEnvironment):
    def __init__(self, environ: Dict[str, str] = None):
        super(InteractiveRunbotEnvironment, self).__init__(environ)
        self.environ["CI_API_V4_URL"] = "https://gitlab.ndp-systemes.fr"

    def interactive(self):
        print("CI_PROJECT_PATH ?")
        print("Nom du projet git (Sans le 'odoo-addons/' ex: mettre `aef` pour `odoo-addons/aef`) ?")
        print("Mettre un '/' si c'est un path absolut (ex /odoo/v15/tms/core')")
        self.environ["CI_PROJECT_PATH"] = input("=>")
        if self.CI_PROJECT_PATH:
            if not self.CI_PROJECT_PATH.startswith("/"):
                self.environ["CI_PROJECT_PATH"] = "odoo-addons/" + self.CI_PROJECT_PATH
            else:
                self.environ["CI_PROJECT_PATH"] = self.CI_PROJECT_PATH.removeprefix("/")
        else:
            print("Un projet est obligatoire")
            sys.exit(1)
        self.environ["CI_PROJECT_PATH_SLUG"] = self.CI_PROJECT_PATH.replace("-", "_").replace("/", "_")
        print("ODOO_VERSION ?")
        self.environ["ODOO_VERSION"] = round(float(input("=>")), 1)
        print("Branch ? default=", self.ODOO_VERSION)
        self.environ["CI_COMMIT_REF_NAME"] = input("=>") or self.ODOO_VERSION
        print(f"GITLAB_TOKEN ? default {self.CI_JOB_TOKEN}")
        self.environ["CI_JOB_TOKEN"] = input("=>") or self.CI_JOB_TOKEN
        self.add_addons_git_default()
        self.environ.update(gitlab_utils.BranchManager.convert_CI_VARS_to_ADDONS_GIT(self))
        if self.NEW_SPEC_ODOO_DEPENDS:
            res = []
            print("If the branch is 'master', 'main', or not set it's ok")
            print("They will be resolved later")
            for addon_def in addons_installer.AddonsRegistry().parse_env(self.environ):
                res.append(" ".join(addon_def.arg_cmd()))
            print("\n".join(res))
            print(f"Ajouter ou modifier ? [yN]")
            if input("=>") == "y":
                self.interactive_git_depends()
        elif self.ODOO_DEPENDS:
            print(f"ODOO_DEPENDS ? default {self.ODOO_DEPENDS}")
            self.environ["NEW_SPEC_ODOO_DEPENDS"] = False
            self.environ["ODOO_DEPENDS"] = input("=>") or self.ODOO_DEPENDS
        print(f"PATH DOCKER COMPOSE ? default = {self.PATH_DOCKER_COMPOSE}")
        result = input("=>")
        if result:
            self.environ["PATH_DOCKER_COMPOSE"] = os.path.join(result, self.UNIQUE_ID)
        print(f"PostgreSQL versoin ? default = {self.POSTGRES_IMG_VERSION}")
        self.environ["POSTGRES_IMG_VERSION"] = input("=>") or self.POSTGRES_IMG_VERSION
        print(f"ODOO_MODULE ?")
        self.environ["ODOO_MODULE"] = input("=>") or self.ODOO_MODULE
        print(f"BEFORE_ODOO_MODULE ?")
        self.environ["BEFORE_ODOO_MODULE"] = input("=>") or self.BEFORE_ODOO_MODULE
        super(InteractiveRunbotEnvironment, self).print_info_running()
        print(f"Ok with the config ? [yN]")
        ok = input("=>") == "y"
        return ok and self or self.interactive()

    def interactive_git_depends(self):

        print(f"Path ?")
        project_path = input("=>")
        if not project_path:
            return


        name = project_path.replace("-", "_").replace("/", "_").upper()
        print(f"Name ? default ", name)
        print("set the same name if you want to override an already depends")
        name = input("=>").replace("-", "_").replace("/", "_").upper()
        self.environ[f"ADDONS_GIT_{name}"] = project_path

        print(f"branch ? else auto resolve")
        result = input("=>")
        if result:
            self.environ[f"ADDONS_GIT_{name}_BRANCH"] = result

        print(f"login ? default")
        result = input("=>")
        if result:
            self.environ[f"ADDONS_GIT_{name}_HTTPS_LOGIN"] = result or self.CI_DEPLOY_USER

        print(f"password ? default")
        result = input("=>")
        if result:
            self.environ[f"ADDONS_GIT_{name}_HTTPS_PASSWORD"] = result or self.CI_DEPLOY_PASSWORD or self.CI_JOB_TOKEN




    @property
    def CI_JOB_TOKEN(self):
        return self.get_value(["CI_JOB_TOKEN", "PERSONAL_GITLAB_TOKEN", "GITLAB_TOKEN"], default=super().CI_JOB_TOKEN)


class ScriptRunbot(abc.ABC):
    def __init__(self, env: RunbotEnvironment):
        self.env = env
        self.gitlab_api = gitlab.Gitlab(env.CI_API_V4_URL, private_token=self.env.CI_JOB_TOKEN)

    def get_argparse(self) -> argparse.ArgumentParser:
        return argparse.ArgumentParser()

    @abc.abstractmethod
    def run_script(self) -> int:
        ...

def get_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive", "-i", help="InteractiveMode", dest="interactive", action="store_true")
    return parser

class ScriptFull(ScriptRunbot):
    compose_file: DockerComposeFile = None
    odoo_service: DockerComposeService = None
    db_service: DatabaseDockerComposeService = None

    def __init__(self, env: RunbotEnvironment):
        super().__init__(env)
        self.database_credential = DatabaseCredential("database")
        self.compose_file = DockerComposeFile(os.path.join(self.env.PATH_DOCKER_COMPOSE, "docker-compose.yml"))
        self.docker = DockerClient(compose_files=[self.compose_file.file_name])
        self.db_service = DatabaseDockerComposeService(self.database_credential, self.env.POSTGRES_IMG_VERSION)
        self.odoo_service = DockerComposeService("odoo", DockerImage("ndpsystemes/odoo", tag=self.env.ODOO_VERSION))



    def run_script(self) -> int:
        # TODO gestion code source
        if not os.path.exists(self.env.PATH_DOCKER_COMPOSE):
            os.mkdir(self.env.PATH_DOCKER_COMPOSE)

        print("Pulling images")
        self.docker.image.pull([self.odoo_service.image, self.db_service.image])

        print("Populate Odoo service with Environment")
        self._populate_odoo_service()
        self.odoo_service.environment["STOP_AFTER_INIT"] = True

        self.odoo_service.depends_on.append(self.db_service)
        self.compose_file.add_service(self.odoo_service)

        if self.env.BEFORE_ODOO_MODULE:
            print("Start Odoo with before odoo modules =>", self.env.BEFORE_ODOO_MODULE)
            result = self.start_odoo(mode_test=False, to_install=self.env.BEFORE_ODOO_MODULE)
            if result.res_num:
                print("Before Odoo Module failed")
                print(result)
                self._clean()
                return result.res_num

        print("Start Odoo with test =>", self.env.ODOO_MODULE)
        result = self.start_odoo(mode_test=True, to_install=self.env.ODOO_MODULE)
        print(result)
        self._clean()
        return result.res_num

    def start_odoo(self, mode_test, to_install):
        self.odoo_service.environment["TEST_ENABLE"] = mode_test
        self.odoo_service.environment["LOG_LEVEL"] = mode_test and "test" or "info"
        self.odoo_service.environment["INSTALL"] = to_install
        self.compose_file.save()

        self.docker.compose.up(["odoo"], detach=False, log_prefix=False)
        return self.parse_logs()

    def parse_logs(self) -> "RunbotResult":
        logs = self.docker.compose.logs(["odoo"], no_log_prefix=True)
        result = RunbotResult()
        for log_line in logs.split("\n"):
            result.test_line(log_line)
        return result

    def _clean(self):
        print("Cleaning stuff")
        self.docker.compose.down(remove_orphans=True, volumes=True)
        self.docker.container.prune()
        self.docker.network.prune()
        self.docker.volume.prune()

    def apply_rule_raise(self, logs):
        error_list = RE_ERROR.findall(logs)
        warning_list = RE_WARNING.findall(logs)
        return error_list, warning_list

    def _populate_odoo_service(self):
        # Define Database environment variable
        self.odoo_service.environment["DB_USER"] = self.database_credential.user
        self.odoo_service.environment["DB_PASSWORD"] = self.database_credential.password
        self.odoo_service.environment["DB_FILTER"] = self.database_credential.db_name
        self.odoo_service.environment["DB_NAME"] = self.database_credential.db_name
        self.odoo_service.environment["DB_HOST"] = self.database_credential.name
        self.odoo_service.environment["DB_PORT"] = self.database_credential.port
        self.odoo_service.environment["DATABASE"] = self.database_credential.db_name

        self.odoo_service.environment["ADMIN_PASSWD"] = get_random_string(20)
        if self.env.WORKERS:
            self.odoo_service.environment["WORKERS"] = self.env.WORKERS

        # Define source to pull
        defs = self._create_all_spec_sources()
        if self.odoo_service.image.name == "ndpsystemes/odoo":
            for depot_number, addon_def in zip([""] + list(range(2, len(defs) + 1)), defs):
                self.odoo_service.environment[f"DEPOT_GIT{depot_number}"] = " ".join(addon_def.arg_cmd())

    def _create_all_spec_sources(self):
        current_gl_project = self.gitlab_api.projects.get(self.env.CI_PROJECT_PATH)
        branch_env = dict(self.env.environ)
        branch_env["ADDONS_GIT_DEFAULT_PROTOCOLE"] = "https"
        branch_env["ADDONS_GIT_DEFAULT_HTTPS_LOGIN"] = self.env.CI_DEPLOY_USER
        branch_env["ADDONS_GIT_DEFAULT_HTTPS_PASSWORD"] = self.env.CI_DEPLOY_PASSWORD or self.env.CI_JOB_TOKEN

        branch_env.update(gitlab_utils.BranchManager.convert_CI_VARS_to_ADDONS_GIT(self.env))

        if not self.env.NEW_SPEC_ODOO_DEPENDS:
            branch_env.update(gitlab_utils.BranchManager.convert_ODOO_DEPENDS_to_ADDONS_GIT(
                gitlab_api=self.gitlab_api,
                odoo_depends=self.env.ODOO_DEPENDS,
                env_vars=dict(os.environ),
                default_branch_to_try_names=[
                    self.env.CI_COMMIT_REF_NAME,
                    current_gl_project.default_branch,
                    self.env.ODOO_VERSION,
                ]
            ))
            defs = list(addons_installer.AddonsRegistry().parse_env(branch_env))
        else:
            defs = list(addons_installer.AddonsRegistry().parse_env(branch_env))
            for addon in defs:
                if not isinstance(addon, addons_installer.GitOdooAddons.Result):
                    continue
                addon.branch = gitlab_utils.BranchManager.try_find_suitable_branch(
                    self.gitlab_api.projects.get(addon.git_path),
                    branch_to_try_names=[
                        addon.branch or self.env.CI_COMMIT_REF_NAME,
                        self.env.CI_COMMIT_REF_NAME,
                        current_gl_project.default_branch,
                        self.env.ODOO_VERSION,
                    ]
                )
        return defs

class RunbotResult():
    module_result: Dict[Optional[str], "ModuleResult"]

    def __init__(self):
        self.module_result = {None: ModuleResult()}
        self.current_module = None
        self.matches = 0

    @property
    def res_num(self) -> int:
        return int(bool(self.matches))

    def test_line(self, line: str) -> int:
        if "odoo.modules.registry: module " in line:
            self.current_module = line.split("odoo.modules.registry: module ")[1].removesuffix(": creating or updating database tables")
            self.module_result.setdefault(self.current_module, ModuleResult())
        if "odoo.modules.loading: Modules loaded." in line:
            self.current_module = None
        self.matches += self.module_result[self.current_module].test_line(line)
        return self.matches

    def __repr__(self):
        res = []
        res.append("Summary:")
        res.append(f"> {sum(map(lambda it: len(it.error_list), self.module_result.values()))} Errors founded")
        res.append(f"> {sum(map(lambda it: len(it.warning_list), self.module_result.values()))} Warnings founded")
        res.append(f"> {sum(map(lambda it: len(it.bad_queries), self.module_result.values()))} Bad queries founded")
        res.append(f"> {sum(map(lambda it: len(it.py_warnings), self.module_result.values()))} py.warnings")
        res.append("----------")
        res.append("")
        for module, result in self.module_result.items():
            if result.res_num:
                res.append(f"In Module {module}")
                res.append(result)
        return "\n".join([str(r) for r in res])

class ModuleResult():

    def __init__(self):
        self.bad_queries = []
        self.error_list = []
        self.warning_list = []
        self.py_warnings = []

    @property
    def res_num(self) -> int:
        return int(bool(self.error_list)) + int(bool(self.warning_list)) + int(bool(self.bad_queries))

    def test_line(self, line: str) -> int:
        matches = 0

        if "odoo.sql_db: bad query:" in line:
            self.bad_queries.append(line)
            matches += 1
        if "py.warnings" in line:
            self.py_warnings.append(line)
            matches += 1
        if not matches and {"ERROR", "CRITICAL", "FATAL"}.intersection(set(line.split(" "))):
            self.error_list.append(line)
            matches += 1
        if not matches and "WARNING" in line:
            self.warning_list.append(line)
            matches += 1
        return matches

    def __repr__(self):
        res = [""]

        def append_info(lines):
            res.append("---------------")
            res.extend(lines)
            res.append("---------------")

        res.append(f"{len(self.error_list)} Errors founded")
        if self.error_list:
            append_info(self.error_list)

        res.append(f"{len(self.warning_list)} Warnings founded")
        if self.warning_list:
            append_info(self.warning_list)

        res.append(f"{len(self.bad_queries)} Bad queries founded")
        if self.bad_queries:
            append_info(self.bad_queries)

        res.append(f"{len(self.py_warnings)} py.warnings")
        if self.py_warnings:
            append_info(self.py_warnings)
        return "\n".join(res)
