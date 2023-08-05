#!/usr/bin/env python3
"""
Dbyml is a CLI tool to build your docker image with the arguments loaded from configs in yaml.

Passing the config file where the arguments are listed to build the image from your dockerfile,
push it to the docker registry.


To make sample config file, run the following command.

>>> dbyml --init normal


To make config file where all files are listed, run the following command.

>>> dbyml --init full

"""
import argparse
import json
import os
import re
import sys
import textwrap
from pathlib import Path
from pprint import pprint
from typing import Optional, Union

import docker
import docker.models.images
import requests
from docker.errors import APIError, ImageNotFound
from requests.auth import HTTPBasicAuth
from ruamel.yaml import YAML


class DockerImage:
    def __init__(self, config_file: Union[str, Path] = None) -> None:
        self.config_file = config_file
        if self.config_file is not None:
            self.load_conf(self.config_file)
        self.client = docker.from_env()
        self.apiclient = docker.APIClient()

    def load_conf(self, path: Union[str, Path], set_param: bool = True) -> None:
        """Loads the settings from config file.

        Args:
            path (str): Path to the config file.
            set_param (bool, optional): Set the settings to the attributes. Defaults to True.
        """
        with open(path, "r") as f:
            self.config = self.parse_config(YAML().load(f))
        if set_param is True:
            self.set_param(self.config)

    def parse_config(self, config: dict) -> dict:
        """Parse values in config file.

        Detect environment variables in the config, replace these to the os env values.

        Args:
            config (dict): the config parameters.

        Returns:
            dict: The parsed config.
        """
        config_str = json.dumps(config)
        envs = re.findall(r"\$\{.+?\}", config_str)
        for e in envs:
            config_str = config_str.replace(e, self.parse_env(e))
        return json.loads(config_str)

    def parse_env(self, env_name: str) -> str:
        e = env_name.strip("${}")
        comp = re.split(":-*", e)
        if len(comp) == 1:
            return self.get_env(comp[0])
        elif len(comp) == 2:
            return os.getenv(comp[0], comp[1])
        else:
            raise SyntaxError(f"ENV {env_name} is invalid format.")

    def get_env(self, env: str) -> str:
        """Get the environment value.

        Args:
            env (str): The ENV name.

        Raises:
            KeyError: The ENV value dose not be defined.

        Returns:
            str: The ENV value.
        """
        v = os.getenv(env)
        if v is None:
            raise KeyError(f"ENV ${{{env}}} not defined.")
        else:
            return v

    def set_param(self, config: dict) -> None:
        try:
            self.name = config["name"]
        except KeyError:
            sys.exit("Field 'name' is required in config file.")

        self.tag = config.get("tag", "latest")
        self.image_name = f"{self.name}:{self.tag}"
        self.verbose = config.get("verbose", False)
        self.build_args = config.get("build_args", {})
        self.label = config.get("label", {})
        self.remove_dangling = config.get("remove_dangling", False)
        self.stdout = config.get("stdout", True)
        self.no_cache = config.get("no_cache", False)

        build_dir = config.get("path", None)
        if build_dir is None:
            self.build_dir = Path.cwd()
        else:
            self.build_dir = Path(build_dir).resolve()

        dockerfile = config.get("dockerfile", "Dockerfile")
        self.dockerfile = self.build_dir / dockerfile

        self.push_param = config.get("push", {})
        if self.push_param != {}:
            self.username = self.push_param.get("username", "")
            self.password = self.push_param.get("password", "")
            self.auth = {"username": self.username, "password": self.password}
            self.registry = Registry(
                self.push_param.get("protocol", "http"),
                self.push_param.get("registry", {}).get("host", ""),
                self.push_param.get("registry", {}).get("port", ""),
                self.name,
                self.tag,
                self.push_param.get("namespace", ""),
                self.username,
                self.password,
            )
        else:
            self.push_param["enabled"] = False

    def check_dockerfile(self) -> bool:
        """Check that dockerfile to build an image exists.

        Raises:
            FileNotFoundError: Raise if the dockerfile does not exist.

        Returns:
            bool: True when the dockerfile exists.
        """
        if self.dockerfile.exists():
            return True
        else:
            raise FileNotFoundError(f"{self.dockerfile} does not exist.")

    def info(self) -> None:
        """Show build information"""
        print()
        print("-" * 20 + f"{'Build information':^20}" + "-" * 20)
        info = textwrap.dedent(
            f"""\
            {'build_dir':<20} {self.build_dir}
            {'image name':<20} {self.image_name}
            """
        )
        if self.build_args:
            for i, (key, value) in enumerate(self.build_args.items()):
                if i == 0:
                    info += f"{'build_args':<20} {{'{key}': '{value}'}}\n"
                else:
                    info += f"{'':<20} {{'{key}': '{value}'}}\n"
        else:
            info += f"{'build_args':<20} {self.build_args}\n"

        if self.label:
            for i, (key, value) in enumerate(self.label.items()):
                if i == 0:
                    info += f"{'label':<20} {{'{key}': '{value}'}}\n"
                else:
                    info += f"{'':<20} {{'{key}': '{value}'}}\n"
        else:
            info += f"{'label':<20} {self.label}\n"

        info += f"{'push to registry':<20} {self.push_param.get('enabled', False)}"
        if self.push_param.get("enabled", False) is True:
            info += "\n"
            info += f"{'registry':<20} {self.registry.registry}\n"
            info += f"{'pushed image':<20} {self.registry.repository}"

        print(info)
        print("-" * 60)
        print()

    def build(self) -> None:
        """Build a docker image."""
        if self.verbose is True:
            self.info()
        self.check_dockerfile()
        if self.remove_dangling is True:
            try:
                self.remove_local_image(self.image_name)
            except ImageNotFound as e:
                print(f"{e} .... skip.")

        if self.stdout is True:
            print()
            print("-" * 20 + f"{'Build start':^20}" + "-" * 20)
            for line in self.apiclient.build(
                path=str(self.build_dir),
                tag=self.image_name,
                buildargs=self.build_args,
                labels=self.label,
                # forcerm=True,
                decode=True,
                nocache=self.no_cache,
            ):
                for k, v in line.items():
                    if k == "error":
                        print(
                            "\033[31mAn error has occurred. The details of the error are following.\033[0m"
                        )
                        print(v)
                    else:
                        if v != "\n":
                            if isinstance(v, str):
                                print(v.strip("\n"))
                            else:
                                print(v)
            print()
            print("-" * 20 + f"{'Build end':^20}" + "-" * 20)
            print(f"Image '{self.image_name}' has been created successfully.")
        else:
            ret = self.client.images.build(
                path=str(self.build_dir),
                tag=self.image_name,
                buildargs=self.build_args,
                labels=self.label,
                forcerm=True,
                nocache=self.no_cache,
            )
            if ret:
                print(f"Image '{self.image_name}' has been created successfully.")

    # def local_search(self) -> bool:
    #     ret = self.client.search(self.name)
    #     try:
    #         for tag in ret["RepoTags"]:
    #             if tag == self.image_name:
    #                 return True
    #         return False
    #     except ImageNotFound:
    #         return False

    def push(self) -> None:
        """Push a docker image to the registry."""
        self.get_image()
        self.docker_tag()
        ret = self.client.images.push(self.registry.repository, auth_config=self.auth)
        print()
        print("-" * 20 + f"{'push result':^20}" + "-" * 20)
        pprint(ret)
        print("-" * 60)
        print()
        if self.push_param.get("remove_local", True):
            self.remove_local_image(self.registry.repository)

    def get_image(self) -> Optional[docker.models.images.Image]:
        try:
            self.image = self.client.images.get(self.image_name)
            return self.image
        except ImageNotFound:
            print(f"Image '{self.image_name}' not found.")
            return None

    def pull(self, name: str, auth: dict = {}) -> None:
        """Pull a docker image from the registry.

        Auth parameters must be set when pull a docker image from the registry that requires basic authentication.
        The format of the auth must be {"username": yourname, "password": yourpassword}.

        Args:
            name (str): The name of the docker image to pull. The name should include a tag.
            auth (dict, optional): Auth credentials to access the registry. Defaults to {}.

        Raises:
            APIError: Raises when the docker api error occurs.
        """
        try:
            # ret = self.client.pull(name, auth_config=self.auth)
            ret = self.apiclient.pull(name, auth_config=self.auth)
            print()
            print("-" * 20 + f"{'pull result':^20}" + "-" * 20)
            pprint(ret)
            print("-" * 60)
            print()
        except APIError as e:
            if e.response.status == 500:
                raise APIError(e.response.message.decode())

    def docker_tag(self) -> None:
        """Add tag to the image"""
        ret = self.image.tag(self.registry.repository)
        if ret is True:
            print(f"Image '{self.registry.repository}' has been created successfully.")

    def remove_local_image(self, name: str) -> None:
        try:
            self.client.images.remove(name)
            print(f"Image '{name}' has been successfully removed from local.")
        except ImageNotFound:
            raise ImageNotFound(message=f"Image '{name}' not found.")


class Registry:
    def __init__(
        self,
        protocol: str = "http",
        host: str = "",
        port: str = "",
        name: str = "",
        tag: str = "",
        namespace: str = "",
        username: str = "",
        password: str = "",
    ) -> None:
        self.protocol = protocol
        self.host = host
        self.port = port
        if self.port != "" and self.host != "":
            self.registry = f"{self.host}:{self.port}"
        else:
            self.registry = ""

        self.name = name
        self.tag = tag
        self.image_name = f"{self.name}:{self.tag}"

        self.namespace = namespace
        if self.namespace != "":
            self.url = f"{self.protocol}://{self.registry}/v2/{self.namespace}/{self.name}/manifests/{self.tag}"
            self.repository = f"{self.registry}/{self.namespace}/{self.image_name}"
        else:
            self.url = (
                f"{self.protocol}://{self.registry}/v2/{self.name}/manifests/{self.tag}"
            )
            self.repository = f"{self.registry}/{self.name}"

        self.username = username
        self.password = password
        self.auth = HTTPBasicAuth(self.username, self.password)

        self.headers = {
            "Accept": "application/vnd.docker.distribution.manifest.v2+json"
        }

    def get_digest(self) -> Optional[str]:
        ret = requests.get(self.url, headers=self.headers, auth=self.auth)
        if ret.status_code == 200:
            return ret.headers.get("Docker-Content-Digest")
        else:
            return None

    def remove_repo_image(self) -> None:
        self.digest = self.get_digest()
        if self.digest is not None:
            # Put the digest into url.
            url = re.sub(r"/[^/]+$", f"/{self.digest}", self.url)
            ret = requests.delete(url, headers=self.headers, auth=self.auth)
            if ret.status_code == 202:
                print(
                    f"{self.repository} has been successfully removed from repository."
                )
            else:
                print(f"{self.repository} cannot be removed. ...skip.")
        else:
            print(f"{self.image_name} not found in {self.registry}.")


def get_config_file() -> Optional[Path]:
    cwd = Path.cwd()
    configs = [cwd / "dbyml.yml", cwd / "dbyml.yaml"]
    for c in configs:
        if c.exists():
            return c
    return None


def create_config(config_type: str) -> None:
    if config_type == "normal":
        filename = "normal.yml"
    elif config_type == "full":
        filename = "full.yml"

    src = Path(__file__).resolve().parent / f"data/{filename}"
    cwd = Path.cwd()
    config = cwd / "dbyml.yml"
    with open(config, "w") as fout:
        with open(src, "r") as fin:
            y = YAML()
            y.dump(y.load(fin), fout)
    print(
        f"Create {config.name}. Check the contents and edit according to your docker image."
    )


def main() -> None:
    usage = "%(prog)s -c [config_file] [options]"
    parser = argparse.ArgumentParser(
        usage=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    parser.add_argument("-c", "--conf", type=str, help="Config file.")
    parser.add_argument(
        "--init",
        type=str,
        choices=["normal", "full"],
        help="Create sample config file. The acceptable values are 'normal' or 'full'.",
    )

    args = parser.parse_args()

    if args.init:
        create_config(args.init)
        sys.exit()

    if args.conf:
        config = args.conf
    else:
        config = get_config_file()
        if config is None:
            parser.print_help()
            sys.exit()

    img = DockerImage(config)
    img.build()
    if img.push_param.get("enabled") is True:
        img.push()


if __name__ == "__main__":
    main()
