# Copyright (c) 2023-2024 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import os
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable, List

PROJECT_CREATION_TEMPLATE_PATH_PREFIX = ".project-creation/templates/"
PROJECT_CREATION_EXAMPLES_DIR = ".project-creation/examples/"
PROJECT_CREATION_SKELETON_DIR = ".project-creation/.skeleton/"
DEFAULT_VEHICLE_APP_NAME = "vehicle_app"
JAVA_OUTPUT_DIR = "target"

def get_core_dir_path() -> str:
    return os.path.join(Path(os.path.dirname(__file__)).parent)


def get_pkg_root_path() -> str:
    return os.path.abspath(
        os.path.join(Path(os.path.dirname(__file__)).parent.parent.parent.parent)
    )


def get_destination_pom_path(destination: str) -> str:
    return os.path.join(destination, "app", "pom.xml")


def verbose_copy(src, dst) -> object:
    print(f"Copying {src!r} to {dst!r}")
    return shutil.copy2(src, dst)


def read_creation_config() -> dict:
    with open(f"{os.path.dirname(__file__)}/config.json") as f:
        config = json.load(f)
        return config


def copy_files(creation_files: list, root_destination: str) -> None:
    for file in creation_files:
        destination = root_destination
        source = f"{get_pkg_root_path()}/{file}"
        if PROJECT_CREATION_TEMPLATE_PATH_PREFIX in file:
            destination = os.path.join(
                root_destination,
                os.path.dirname(
                    file.removeprefix(PROJECT_CREATION_TEMPLATE_PATH_PREFIX)
                ),
            )
            source = f"{get_core_dir_path()}/{file}"

        Path(destination).mkdir(parents=True, exist_ok=True)
        verbose_copy(source, destination)


def _filter_hidden_files(_: str, dir_contents: List[str]) -> Iterable[str]:
    hidden_files = [".git"]
    return filter(lambda file: file in hidden_files, dir_contents)


def copy_uservices_jar(destination_repo: str) -> None:
    uservices_jar_source = os.path.join(get_core_dir_path(), "uservices")
    uservices_jar_destination = os.path.join(destination_repo, "uservices")

    shutil.copytree(
        uservices_jar_source,
        uservices_jar_destination,
        copy_function=verbose_copy,
        dirs_exist_ok=True,
        ignore=_filter_hidden_files,
    )


def update_pom_uservices_jar_path(destination_repo: str) -> None:
    destination_pom_path = get_destination_pom_path(destination_repo)
    uservices_api_path_property = "uservices-api.path"
    uservices_destination_dir = os.path.join(destination_repo, "uservices")
    new_uservices_api_path_value = os.path.join(
        uservices_destination_dir, os.listdir(uservices_destination_dir)[0]
    )

    tree = ET.parse(destination_pom_path)
    root = tree.getroot()
    # Remove namespaces from tags
    for elem in root.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]

    for elem in root.iter(uservices_api_path_property):
        elem.text = new_uservices_api_path_value

    tree.write(destination_pom_path, encoding="utf-8", xml_declaration=True)


def copy_project(source_path: str, destination_repo: str) -> None:
    app_path = os.path.join(destination_repo, "app")

    shutil.copytree(
        source_path,
        app_path,
        copy_function=verbose_copy,
        dirs_exist_ok=True,
        ignore=_filter_hidden_files,
    )

    readme_path = os.path.join(app_path, "README.md")
    if os.path.exists(readme_path):
        existing_readme_path = os.path.join(destination_repo, "README.md")
        if os.path.exists(existing_readme_path):
            os.remove(existing_readme_path)
        shutil.move(readme_path, destination_repo, copy_function=verbose_copy)


def sanitize_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "", name)


def replace_app_name(creation_name: str, destination_repo: str) -> None:
    creation_name = sanitize_name(creation_name)
    for root, dirs, files in os.walk(destination_repo):
        if JAVA_OUTPUT_DIR in dirs:
            dirs.remove(JAVA_OUTPUT_DIR)
        for name in dirs[:]:
            if name == DEFAULT_VEHICLE_APP_NAME:
                old_dir_path = os.path.join(root, name)
                new_dir_path = os.path.join(root, creation_name)
                os.rename(old_dir_path, new_dir_path)
                print(f"Directory '{old_dir_path}' renamed to '{new_dir_path}'.")
            for index, directory in enumerate(dirs):
                if directory == DEFAULT_VEHICLE_APP_NAME:
                    dirs[index] = creation_name
        for file in files:
            if ".jar" not in file:
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                modified_content = content.replace(DEFAULT_VEHICLE_APP_NAME, creation_name)
                with open(file_path, "w") as f:
                    f.write(modified_content)
                    print(
                        f"Replaced '{DEFAULT_VEHICLE_APP_NAME}' with '{creation_name}' in file '{file_path}'."
                    )


def main():
    parser = argparse.ArgumentParser("run")
    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        required=True,
        help="Path to the root of the repository.",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        required=False,
        help="Name of the VApp.",
    )
    parser.add_argument(
        "-e",
        "--example",
        type=str,
        required=False,
        help="Copy the given example to the new repo.",
    )
    args = parser.parse_args()
    creation_config = read_creation_config()

    copy_files(creation_config["files"], args.destination)

    examples_directory_path = os.path.join(get_core_dir_path(), PROJECT_CREATION_EXAMPLES_DIR)
    example_app = (
        os.path.join(examples_directory_path, args.example)
        if args.example
        else os.path.join(get_core_dir_path(), PROJECT_CREATION_SKELETON_DIR)
    )

    copy_project(example_app, args.destination)
    copy_uservices_jar(args.destination)
    update_pom_uservices_jar_path(args.destination)
    # For now only when skeleton is created
    if not args.example:
        replace_app_name(args.name, args.destination)


if __name__ == "__main__":
    main()
