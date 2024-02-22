# Velocitas uProtocol Support package

This repository is supposed to be used as a self-contained [Velocitas toolchain package](https://github.com/eclipse-velocitas/cli/blob/main/docs/features/PACKAGES.md) which enables
the development of uProtocol applications and services (uApps and uServices). No further Velocitas packages are needed to develop uApps and uServices.


## Setting up your local developoment environment

Testing of the package shall be done in the `testbench` folder, where a `run_cli.sh` script is provided. This script will download and run the correct branch of the Velocitas CLI for the uProtocol integration using this repository as the package contents. This allows you to instantly test your package without further copying to other repos.


## Structure

The package is structured as follows, please follow the links for a detailed description of the component:

* $root/
    * 📁 components/
        * 📁 cores/
            * [uapp-java](./components/cores/uapp-java/README.md)/
                * 📁 .project-creation/
                    * 📁 .skeleton/
                        * 📁 src/
                    * 📁 examples/
                        * 📁 horn-activator/
                            * 📁 src/
                    * 📁 templates/
                    * 📁 test/
                    * 📄 config.json
                    * 📄 run.py
                * 📁 uservices/
        * 📁 extensions/
            * 📁 [devcontainer-setup-java](./components/extensions/devcontainer-setup-java/README.md)/
            * 📁 [github-workflows](./components/extensions/github-workflows/README.md)/
            * 📁 [service-catalogue-support](./components/extensions/service-catalogue-support/README.md)/ (?)
            * 📁 [tool-manager](./components/extensions/tool-manager/README.md)/ (?)
                * 📄 manager.py
                * 📄 tools.yaml
    * 📁 [testbench](./testbench/README.md)
    * 📄 manifest.json
