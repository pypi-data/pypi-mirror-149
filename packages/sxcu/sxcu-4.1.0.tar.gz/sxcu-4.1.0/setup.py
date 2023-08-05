# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sxcu']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.0.0']

extras_require = \
{'cli': ['rich>=10.5,<11.0', 'pyperclip>=1.8,<2.0']}

entry_points = \
{'console_scripts': ['sxcu = sxcu._cli:main']}

setup_kwargs = {
    'name': 'sxcu',
    'version': '4.1.0',
    'description': 'Python API wrapper for sxcu.net',
    'long_description': '# SXCU Python API Wrapper\n<p align="center">\n  <a href="https://pypi.org/project/sxcu/">\n    <img src="https://img.shields.io/pypi/v/sxcu" alt="sxcu PyPI Version">\n  </a>\n  <a href="https://sxcu.readthedocs.io">\n    <img src="https://readthedocs.org/projects/sxcu/badge/?version=latest" alt="sxcu Documentation Status">\n  </a>\n  <a href="https://opensource.org/licenses/Apache-2.0">\n    <img src="https://img.shields.io/badge/License-Apache2.0-green.svg" alt"sxcu License">\n  </a>\n  <a href="https://codecov.io/gh/naveen521kk/sxcu">\n    <img src="https://codecov.io/gh/naveen521kk/sxcu/branch/master/graph/badge.svg" alt="sxcu codecov">\n  </a>\n  <a href="https://lgtm.com/projects/g/naveen521kk/sxcu/alerts/">\n    <img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/naveen521kk/sxcu.svg?logo=lgtm&logoWidth=18"/>\n  </a>\n  <a href="https://lgtm.com/projects/g/naveen521kk/sxcu/context:python">\n    <img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/naveen521kk/sxcu.svg?logo=lgtm&logoWidth=18"/>\n  </a>\n</p>\n\n![sxcu-logo](https://github.com/naveen521kk/sxcu/raw/master/logo/readme-logo.png)\n<p align="center">\nA friendly API wrapper around https://sxcu.net.\n</p>\n\n## Installation\n\nThe package is published on\n[PyPI](https://pypi.org/project/sxcu/) and can be installed by running:\n```sh\npip install sxcu\n```\n\n## Basic Use\n\nEasily query the sxcu.net from you Python code. The data returned from the sxcu.net\nAPI is mapped to python resources:\n\n```python\n>>> import sxcu\n>>> con = sxcu.SXCU()\n>>> con.upload_image("foo.jpg")\n{\'url\': \'https://sxcu.net/2kW7IT\', \'del_url\': \'https://sxcu.net/d/2kW7IT/455c7e40-9e3b-43fa-a95a-ac17dd920e55\', \'thumb\': \'https://sxcu.net/t/2kW7IT.jpeg\'}\n```\nReady for more? Look at our whole [documentation](https://sxcu.readthedocs.io/) on Read The Docs.\n\n## Contributing\nPlease refer to [CONTRIBUTING.md](CONTRIBUTING.md) file for more information on how to\ncontribute to this project.\n\n<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->\n[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)\n<!-- ALL-CONTRIBUTORS-BADGE:END -->\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://naveen.syrusdark.website"><img src="https://avatars1.githubusercontent.com/u/49693820?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Naveen M K</b></sub></a><br /><a href="https://github.com/naveen521kk/sxcu/commits?author=naveen521kk" title="Code">💻</a> <a href="https://github.com/naveen521kk/sxcu/commits?author=naveen521kk" title="Documentation">📖</a> <a href="#maintenance-naveen521kk" title="Maintenance">🚧</a> <a href="#projectManagement-naveen521kk" title="Project Management">📆</a> <a href="https://github.com/naveen521kk/sxcu/pulls?q=is%3Apr+reviewed-by%3Anaveen521kk" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/naveen521kk/sxcu/commits?author=naveen521kk" title="Tests">⚠️</a> <a href="#platform-naveen521kk" title="Packaging/porting to new platform">📦</a></td>\n    <td align="center"><a href="https://github.com/shahprog"><img src="https://avatars0.githubusercontent.com/u/40076722?v=4?s=100" width="100px;" alt=""/><br /><sub><b>shahprog</b></sub></a><br /><a href="https://github.com/naveen521kk/sxcu/issues?q=author%3Ashahprog" title="Bug reports">🐛</a> <a href="https://github.com/naveen521kk/sxcu/commits?author=shahprog" title="Code">💻</a></td>\n    <td align="center"><a href="https://hexiro.me"><img src="https://avatars.githubusercontent.com/u/42787085?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Hexiro</b></sub></a><br /><a href="https://github.com/naveen521kk/sxcu/commits?author=Hexiro" title="Code">💻</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n',
    'author': 'Naveen M K',
    'author_email': 'naveen521kk@gmail.com',
    'maintainer': 'Naveen M K',
    'maintainer_email': 'naveen521kk@gmail.com',
    'url': 'https://github.com/naveen521kk/sxcu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
