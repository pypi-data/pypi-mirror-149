# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nshm_toshi_client', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'async-timeout>=4.0.2,<5.0.0',
 'gql>=3.2.0,<4.0.0',
 'graphql-core>=3.2.1,<4.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'nshm-toshi-client',
    'version': '0.6.0',
    'description': 'client for toshi API',
    'long_description': '# nshm-toshi-client\n\n[![pypi](https://img.shields.io/pypi/v/nshm-toshi-client.svg)](https://pypi.org/project/nshm-toshi-client/)\n[![python](https://img.shields.io/pypi/pyversions/nshm-toshi-client.svg)](https://pypi.org/project/nshm-toshi-client/)\n[![Build Status](https://github.com/gns-science/nshm-toshi-client/actions/workflows/dev.yml/badge.svg)](https://github.com/gns-science/nshm-toshi-client/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/gns-science/nshm-toshi-client/branch/main/graphs/badge.svg)](https://codecov.io/github/gns-science/nshm-toshi-client)\n\nA python3 client for the nshm-toshi-api.\n\n* Documentation: <https://gns-science.github.io/nshm-toshi-client>\n* GitHub: <https://github.com/gns-science/nshm-toshi-client>\n* PyPI: <https://pypi.org/project/nshm-toshi-client/>\n* Free software: MIT\n\n## Features\n\n- TODO\n\n',
    'author': 'Chris Chamberlain',
    'author_email': 'chrisbc@artisan.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
