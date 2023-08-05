# README

boi is a [cli](https://en.wikipedia.org/wiki/Command-line_interface) based builder of [docker](https://hub.docker.com/) images. It provides an interface for building and pushing the image as well as for tagging source code after build with a build version and other common image tasks.


### Requirements  ###

- python 3
- docker: docker must be set up as it is used to build and push the image
- git: if you use the source-tag feature you will need git installed and your code setup in git (it simply performs a git tag && git push from the working directory)


###  Overview  ###

- setup (see #setup)
- configure (see #configure): place a copy of the example/.boi.toml in the same directory as your Dockerfile of the app you want to build and adjust it as needed
- run (see #run): execute boi to build/push/tag a version of your app, its as simple as `boi build`


### Install

We recommend using [pipx](https://github.com/pypa/pipx) to install boi: `pipx install boi`. You can also install via pip: `pip install --user boi`.


###  Setup  ###

boi uses a config file to store your setup. Each 'app' you build with boi expects this file to be in the 'root' of the app that you are building. This file contains information such as whether to build, push, tag the image, labels to apply, Dockerfile to use, etc. You can grab an example config file from  [boi/example/.boi.toml](https://gitlab.com/drad/boi/-/blob/master/example/.boi.toml).


### Configure  ###

- create a project config file
  - place a copy of the `example/.boi.toml` file in your project (same directory as your Dockerfile) and configure as needed


### Features ###

If you create an arg with the name "BUILD_VERSION" its value will be replaced with the build version of the current build. This can be used to pass the build version from boi into your docker environment.


### Run  ###

- basic run: `boi build --version=1.2.3`
  - the above command assumes there is a `.boi.toml` in the current working directory which happens to be in the same directory as the Dockerfile which you wish to build

View help with `boi --help` or see help for a specific command: `boi build --help`.


###  Recommendations  ###

We recommend using docker's configuration storage for reg_auth-* related configuration items as it encrypts sensitive information and is likely already configured (if you have already used `docker login`). If you leave the remaining items empty the default values will be used. This will then try `$HOME/.docker/config.json` and `$HOME/.dockercfg` for your docker config settings. If you do not already have a docker config run `docker login` and it should be created for you. After a successful login you should not need to do anything else for the application as the needed info will be stored in your dockercfg and the app will use it when needed.


## Links

- [typer](https://typer.tiangolo.com/)
- [docker](https://pypi.org/project/docker/)
  - [docs](https://docker-py.readthedocs.io/en/stable/)
- [toml](https://pypi.org/project/toml/)