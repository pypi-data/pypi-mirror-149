# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ibuilder', 'ibuilder.config']

package_data = \
{'': ['*']}

install_requires = \
['arrow==1.2.2',
 'click==8.1.3',
 'docker==5.0.3',
 'packaging==21.3',
 'pydantic==1.9.0',
 'requests==2.27.1',
 'rich==12.3.0',
 'tinydb==4.7.0',
 'tomli==2.0.1',
 'typer==0.4.1']

entry_points = \
{'console_scripts': ['ib = ibuilder.main:app']}

setup_kwargs = {
    'name': 'ibuilder',
    'version': '3.0.0',
    'description': 'image builder; build, tag, and push docker images',
    'long_description': '# README\n\nboi is a [cli](https://en.wikipedia.org/wiki/Command-line_interface) based builder of [docker](https://hub.docker.com/) images. It provides an interface for building and pushing the image as well as for tagging source code after build with a build version and other common image tasks.\n\n\n### Requirements  ###\n\n- python 3\n- docker: docker must be set up as it is used to build and push the image\n- git: if you use the source-tag feature you will need git installed and your code setup in git (it simply performs a git tag && git push from the working directory)\n\n\n###  Overview  ###\n\n- setup (see #setup)\n- configure (see #configure): place a copy of the example/.boi.toml in the same directory as your Dockerfile of the app you want to build and adjust it as needed\n- run (see #run): execute boi to build/push/tag a version of your app, its as simple as `boi build`\n\n\n### Install\n\nWe recommend using [pipx](https://github.com/pypa/pipx) to install boi: `pipx install boi`. You can also install via pip: `pip install --user boi`.\n\n\n###  Setup  ###\n\nboi uses a config file to store your setup. Each \'app\' you build with boi expects this file to be in the \'root\' of the app that you are building. This file contains information such as whether to build, push, tag the image, labels to apply, Dockerfile to use, etc. You can grab an example config file from  [boi/example/.boi.toml](https://gitlab.com/drad/boi/-/blob/master/example/.boi.toml).\n\n\n### Configure  ###\n\n- create a project config file\n  - place a copy of the `example/.boi.toml` file in your project (same directory as your Dockerfile) and configure as needed\n\n\n### Features ###\n\nIf you create an arg with the name "BUILD_VERSION" its value will be replaced with the build version of the current build. This can be used to pass the build version from boi into your docker environment.\n\n\n### Run  ###\n\n- basic run: `boi build --version=1.2.3`\n  - the above command assumes there is a `.boi.toml` in the current working directory which happens to be in the same directory as the Dockerfile which you wish to build\n\nView help with `boi --help` or see help for a specific command: `boi build --help`.\n\n\n###  Recommendations  ###\n\nWe recommend using docker\'s configuration storage for reg_auth-* related configuration items as it encrypts sensitive information and is likely already configured (if you have already used `docker login`). If you leave the remaining items empty the default values will be used. This will then try `$HOME/.docker/config.json` and `$HOME/.dockercfg` for your docker config settings. If you do not already have a docker config run `docker login` and it should be created for you. After a successful login you should not need to do anything else for the application as the needed info will be stored in your dockercfg and the app will use it when needed.\n\n\n## Links\n\n- [typer](https://typer.tiangolo.com/)\n- [docker](https://pypi.org/project/docker/)\n  - [docs](https://docker-py.readthedocs.io/en/stable/)\n- [toml](https://pypi.org/project/toml/)',
    'author': 'David Rader',
    'author_email': 'sa@adercon.com',
    'maintainer': 'David Rader',
    'maintainer_email': 'sa@adercon.com',
    'url': 'https://gitlab.com/drad/boi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
