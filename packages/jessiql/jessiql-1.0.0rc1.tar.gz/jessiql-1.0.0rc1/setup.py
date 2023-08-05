# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jessiql',
 'jessiql.engine',
 'jessiql.integration',
 'jessiql.integration.fastapi',
 'jessiql.integration.graphql',
 'jessiql.operations',
 'jessiql.operations.pager',
 'jessiql.query_object',
 'jessiql.query_object.rewrite',
 'jessiql.query_object.tools',
 'jessiql.sainfo',
 'jessiql.sautil',
 'jessiql.testing',
 'jessiql.testing.graphql',
 'jessiql.util']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[mypy]']

setup_kwargs = {
    'name': 'jessiql',
    'version': '1.0.0rc1',
    'description': '',
    'long_description': None,
    'author': 'Mark Vartanyan',
    'author_email': 'kolypto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kolypto/py-jessiql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
