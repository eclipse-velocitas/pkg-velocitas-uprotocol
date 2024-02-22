#!/bin/bash

set -x

export VELOCITAS_HOME=$(pwd)
CLI_FOLDER=.cli

if [ ! -e "${CLI_FOLDER}" ]; then
    # Clone
    git clone https://github.com/eclipse-velocitas/cli.git $CLI_FOLDER
    # Fix dubious ownership
    git config --global --add safe.directory $(pwd)/$CLI_FOLDER
fi

cd $CLI_FOLDER
git switch feature/modularity
cp testbench/test-create/vehicle-app-template/package-index.json ../package-index.json

if [ ! hash node &> /dev/null ]; then
    ./install_node.sh
fi

npm i
cd ..

./${CLI_FOLDER}/bin/dev $@
