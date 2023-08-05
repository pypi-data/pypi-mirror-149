# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apiens',
 'apiens.crud',
 'apiens.crud.base',
 'apiens.crud.mutate',
 'apiens.crud.query',
 'apiens.structure',
 'apiens.structure.error',
 'apiens.structure.func',
 'apiens.testing',
 'apiens.testing.models_match',
 'apiens.testing.object_match',
 'apiens.tools',
 'apiens.tools.ariadne',
 'apiens.tools.ariadne.directives',
 'apiens.tools.ariadne.testing',
 'apiens.tools.fastapi',
 'apiens.tools.fastapi.class_based_view',
 'apiens.tools.graphql',
 'apiens.tools.graphql.directives',
 'apiens.tools.graphql.middleware',
 'apiens.tools.pydantic',
 'apiens.tools.settings',
 'apiens.tools.sqlalchemy',
 'apiens.tools.sqlalchemy.types']

package_data = \
{'': ['*']}

install_requires = \
['jessiql>=1.0.0-rc1,<2.0.0']

setup_kwargs = {
    'name': 'apiens',
    'version': '2.0.0rc1',
    'description': '',
    'long_description': None,
    'author': 'Mark Vartanyan',
    'author_email': 'kolypto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kolypto/py-apiens',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
