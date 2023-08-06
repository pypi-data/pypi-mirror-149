# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neclib',
 'neclib.controllers',
 'neclib.interfaces',
 'neclib.parameters',
 'neclib.parameters.parser',
 'neclib.simulators',
 'neclib.utils']

package_data = \
{'': ['*']}

install_requires = \
['n-const>=1.0.4,<2.0.0', 'numpy>=1.19,<2.0']

extras_require = \
{':python_version < "3.8"': ['astropy>=3.0,<4.0',
                             'importlib-metadata>=4.4,<5.0',
                             'typing-extensions>=3.0,<5.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9'],
 ':python_version >= "3.8"': ['astropy>=5.0.4,<6.0.0']}

setup_kwargs = {
    'name': 'neclib',
    'version': '0.6.2',
    'description': 'Pure Python tools for NECST.',
    'long_description': '# neclib\n\n[![PyPI](https://img.shields.io/pypi/v/neclib.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/neclib/)\n[![Python](https://img.shields.io/pypi/pyversions/neclib.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/neclib/)\n[![Test](https://img.shields.io/github/workflow/status/nanten2/neclib/Test?logo=github&label=Test&style=flat-square)](https://github.com/nanten2/neclib/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nPure Python tools for NECST.\n\n## Features\n\nThis library provides:\n\n- Miscellaneous tools for NECST system.\n\n## Installation\n\n```shell\npip install neclib\n```\n\n## Usage\n\nSee the [API reference](https://nanten2.github.io/neclib/_source/neclib.html).\n\n---\n\nThis library is using [Semantic Versioning](https://semver.org).\n',
    'author': 'KaoruNishikawa',
    'author_email': 'k.nishikawa@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://nanten2.github.io/neclib/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
