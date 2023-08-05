# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hurocon']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'huawei-lte-api>=1.6.0,<2.0.0',
 'serialix>=2.3.1,<3.0.0']

entry_points = \
{'console_scripts': ['hurocon = hurocon.cli:cli']}

setup_kwargs = {
    'name': 'hurocon',
    'version': '0.2.0',
    'description': 'Command line interface tool for interacting with Huawei LTE routers',
    'long_description': '# Hurocon\nHurocon *(**hu**awei **ro**uter **con**trol)* - command line interface tool for interacting with Huawei LTE routers\n\n\n- [Features](#features)\n- [Supported Devices](#supported-devices)\n- [Availability](#availability)\n- [Installation](#installation)\n- [Quickstart](#quickstart)\n- [Development](#development)\n- [Special](#special)\n\n\n## Features\n- Device Control\n  - Reboot\n- SMS Control\n  - Send\n\n> There are many features planned for future releases, you can view their full list [here](https://github.com/maximilionus/hurocon/projects/1)\n\n\n## Supported Devices\nFull list of supported devices is available on [this link](https://github.com/Salamek/huawei-lte-api#tested-on).\n\n\n## Availability\nThis tool is OS-independent, which means it should work on any platform where python3 can run. Minimal python3 version required for this package is `3.7`. This does not mean that it cannot work on python versions below the minimal, but its behavior is unpredictable and no support will be provided for any issues.\n\n\n## Installation\nCurrently this tool can only be installed with `pip` on `python` >= 3.7.\n\n- You can install it from PyPi:\n\n  ```bash\n  pip install hurocon\n  ```\n\n- Or directly from Github repo:\n\n  ```bash\n  pip install git+https://github.com/maximilionus/hurocon.git\n  ```\n\n> Built executable binary *([pyinstaller](https://pyinstaller.org/)-based)* is planned but no ETA yet\n\n\n## Quickstart\n### Intro\nAfter successful [installation](#installation) of this tool it can be accessed in shell using the following commands:\n\n```bash\n$ hurocon\n# OR\n$ python -m hurocon\n```\n\nYou can also view a list of all main commands with:\n```bash\n$ hurocon --help\n```\n\nEach command and subcommand in this tool has a special `--help` flag to display detailed information about it\n\n### Authentification\nFirst of all, you need to specify the authorization and connection data so that this tool can access the router in the future. You do it in two ways.\n\n- In interactive mode:\n  ``` bash\n  $ hurocon auth login\n  ```\n\n- Manually, by running:\n  ```bash\n  # Initialize local configuration file\n  $ hurocon config init\n\n  # Show path to local configuration file\n  $ hurocon config path\n  ```\n\n  And then manually editing the `json` file with any text editor. It has a human-readable structure, so every part of it is exactly what you think it is.\n\n### Testing Connection\nAfter auth details successfully specified you can test your connection with router by running\n\n```bash\n$ hurocon auth test\n\n# Returns\n# Success: Successful Authentification\n# Failure: Auth failed, reason: "..."\n```\n\n### Conclusion\nThat\'s it, you\'re ready to go. And remember - no matter how deep you go, `--help` flag is always here to help 👍\n\n\n## Development\n### Prepare The Environment\nTo prepare the development environment for this project, follow these steps:\n\n1. Install `poetry` package manager with ([pip](https://pypi.org/project/poetry/), [standalone](https://python-poetry.org/docs/master/#installing-with-the-official-installer) *(recomended)*)\n\n2. Run the command below to prepare the virtual environment for this project\n   ```bash\n   $ poetry install\n   ```\n\n3. That\'s it, now you can modify the code the way you want and test it in two ways\n    - Run this tool with\n      ```bash\n      $ poetry run hurocon\n      ```\n    - Or activate the project shell with\n      ```bash\n      $ poetry shell\n      Spawning shell within ...\n\n      $ hurocon\n      ```\n\n### Build\n#### Python Package\nTo build this tool to package *([sdist](https://docs.python.org/3/distutils/sourcedist.html) and wheel)* you should execute:\n\n```bash\n$ poetry build\nBuilding hurocon ...\n```\n\nPrepared for distribution package will be located in `./dist/` directory\n\n\n## Special\nBig thanks to [Adam Schubert](https://github.com/Salamek) for his amazing [`huawei-lte-api`](https://github.com/Salamek/huawei-lte-api) package, that made this whole thing possible.\n',
    'author': 'maximilionus',
    'author_email': 'maximilionuss@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maximilionus/hurocon.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
