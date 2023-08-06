import os

import sys

from .runbot_docker import InteractiveRunbotEnvironment, RunbotEnvironment, ScriptFull, get_argparse


def main():
    ns = get_argparse().parse_args()
    env = RunbotEnvironment()
    if not env.CI or ns.interactive:
        env = InteractiveRunbotEnvironment(dict(os.environ, **{
            "CI_API_V4_URL": "https://gitlab.ndp-systemes.fr",
            "NEW_SPEC_ODOO_DEPENDS": "True",
            "ADDONS_GIT_DEFAULT_SERVER": "gitlab.ndp-systemes.fr",
            "ADDONS_GIT_DEFAULT_PROTOCOLE": "https",
            "ADDONS_GIT_COMMON_MODULES": "odoo-addons/common-modules", # New format for ODOO_DEPENDS
            "ADDONS_GIT_COMMUNITY_ADDONS": "odoo-addons/community-addons", # New format for ODOO_DEPENDS
        })).interactive()
    script = ScriptFull(env)
    if not script.env.CI_DEPLOY_USER:
        script.gitlab_api.auth()
        script.env.environ["CI_DEPLOY_USER"] = script.gitlab_api.user.username
    sys.exit(script.run_script())




if __name__ == '__main__':
    main()
