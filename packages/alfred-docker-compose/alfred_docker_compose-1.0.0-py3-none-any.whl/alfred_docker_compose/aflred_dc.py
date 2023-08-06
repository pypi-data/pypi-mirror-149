
from typing import Optional, Protocol, Union, Dict, List, Any

import abc

import os
from os import PathLike

import tempfile

import string

import random
from ndp_utils.gitlab_utils import GITLAB_CI_VARS

from oyaml import dump, load


def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


class DockerRegistryImage:
    def __init__(self, name: str, port: str = ""):
        self.name = name
        self.port = port

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.name}:{self.port}"


class DockerImage:
    def __init__(self, name: str, tag: str, registry: DockerRegistryImage = None):
        self.tag = tag
        self.registry = registry
        self.name = name

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        repr = f"{self.name}"
        if self.registry:
            repr = f"{self.registry}/{repr}"
        if not self.tag:
            return repr
        return f"{repr}:{self.tag}"


class DockerComposeService:
    image: DockerImage
    name: str
    volumes: Dict[str, str]
    environment: Dict[str, Union[str, bool, int]]
    ports: Dict[str, int]
    links: List[Union[str, "DockerComposeService"]]
    depends_on: List[Union[str, "DockerComposeService"]]

    def __init__(self, name: str, image: DockerImage):
        super(DockerComposeService, self).__init__()
        self.image = image
        self.name = name
        self.volumes = {}
        self.environment = {}
        self.ports = {}
        self.links = []
        self.depends_on = []

    def to_dict(self):
        data = {"image": str(self.image)}
        if self.environment:
            data["environment"] = {k :v for k, v in self.environment.items()}
        if self.volumes:
            data["volumes"] = [f"{k}:{v}" for k, v in self.volumes.items()]
        if self.ports:
            data["ports"] = [f"{k}:{v}" for k, v in self.ports.items()]
        if self.links:
            data["links"] = []
            for link in self.links:
                if isinstance(link, DockerComposeService):
                    data["links"].append(link.name)
                else:
                    data["links"].append(str(link))
        if self.depends_on:
            data["depends_on"] = []
            for depends_on in self.depends_on:
                if isinstance(depends_on, DockerComposeService):
                    data["depends_on"].append(depends_on.name)
                else:
                    data["depends_on"].append(str(depends_on))
        return data




    @staticmethod
    def from_dict(name, data) -> "DockerComposeService":
        img = data["image"]
        img_name = data["image"].split(":")[0]
        tag = ""
        if ":" in img:
            tag = data["image"].split(":")[1]
        service = DockerComposeService(name, DockerImage(img_name, tag=tag))
        service.environment = data["environment"]
        service.volumes = data["volumes"]
        service.ports = data["ports"]
        service.links = data["links"]
        return service


class DatabaseCredential:
    name: str
    user: str
    password: str
    port: int
    db_name: str

    def __init__(self, name:str=None, user:str=None, password:str=None, port:int=5432, db_name:str=None):
            self.name = name
            self.user = user or get_random_string(5)
            self.password = user or get_random_string(10)
            self.port = port
            self.db_name = self.name + get_random_string(4)

class DatabaseDockerComposeServiceABC(DockerComposeService, DatabaseCredential, abc.ABC):
    ...


class DatabaseDockerComposeService(DockerComposeService):

    def __init__(self, credential: DatabaseCredential, postgres_version: str):
        super(DatabaseDockerComposeService, self).__init__(credential.name, DockerImage("postgres", postgres_version))
        self.credential = credential
        self.environment["POSTGRES_USER"] = credential.user
        self.environment["POSTGRES_PASSWORD"] = credential.password


class DockerComposeFile:
    service: Dict[str, DockerComposeService]
    version: str
    file_name: str

    def __init__(self, file_name, version: str = "3.9"):
        self.file_name = file_name
        self.version = version
        self.services: Dict[str, DockerComposeService] = {}

    def add_service(self, service: DockerComposeService):
        self.services[service.name] = service
        if service.links or service.depends_on:
            for link in service.links + service.depends_on:
                if isinstance(link, DockerComposeService):
                    self.add_service(link)

    def to_dict(self):
        return {
            "version": self.version,
            "services": {
                name: service.to_dict() for name, service in self.services.items()
            }
        }

    def save(self):
        print("Save to", self.file_name)
        with open(self.file_name, "w+") as dc_file:
            print(dump(self.to_dict()))
            dump(self.to_dict(), dc_file)

    def load(path: Union[str, bytes, PathLike[str], PathLike[bytes]]) -> "DockerComposeFile":
        docker_yaml = load(open(path))
        inst = DockerComposeFile(path, docker_yaml["version"])
        for name, content in docker_yaml["services"]:
            inst.add_service(DockerComposeService.from_dict(name, content))
        return inst
