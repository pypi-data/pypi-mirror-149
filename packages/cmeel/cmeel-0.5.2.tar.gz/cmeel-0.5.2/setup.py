# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmeel']

package_data = \
{'': ['*']}

install_requires = \
['tomli>=2.0.1,<3.0.0']

extras_require = \
{'build': ['cmake>=3.22.3,<4.0.0',
           'packaging>=21.3,<22.0',
           'wheel>=0.37.1,<0.38.0']}

setup_kwargs = {
    'name': 'cmeel',
    'version': '0.5.2',
    'description': 'Create Wheel from CMake projects',
    'long_description': '# CMake Wheels\n\n[![PyPI version](https://badge.fury.io/py/cmeel.svg)](https://pypi.org/project/cmeel)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nim65s/cmeel/main.svg)](https://results.pre-commit.ci/latest/github/nim65s/cmeel/main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n',
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nim65s/cmeel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
