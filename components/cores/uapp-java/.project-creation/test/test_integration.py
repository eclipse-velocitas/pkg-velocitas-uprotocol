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

import os

from pytest_check import check


@check.check_func
def is_dir(path: str):
    assert os.path.isdir(path)


@check.check_func
def is_file(path: str):
    assert os.path.isfile(path)


def test_files_in_place():
    os.chdir(os.environ["VELOCITAS_APP_ROOT"])

    # vscode project
    is_dir(".vscode")
    is_file(".vscode/launch.json")

    # app
    is_dir("app")
    is_file("app/pom.xml")

    # uservices_jar
    is_dir("uservices")

    # general things
    is_file(".pre-commit-config.yaml")
