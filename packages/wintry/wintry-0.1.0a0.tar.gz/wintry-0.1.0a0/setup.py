# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wintry',
 'wintry.drivers',
 'wintry.errors',
 'wintry.mqs',
 'wintry.query',
 'wintry.repository',
 'wintry.transactions',
 'wintry.utils']

package_data = \
{'': ['*']}

install_requires = \
['Inject>=4.3.1,<5.0.0',
 'dataclass-wizard>=0.22.0,<0.23.0',
 'fastapi>=0.75.2,<0.76.0',
 'motor>=2.5.1,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pyee>=9.0.4,<10.0.0',
 'uvicorn>=0.17.6,<0.18.0']

extras_require = \
{'postgres': ['SQLAlchemy>=1.4.35,<2.0.0', 'asyncpg>=0.25.0,<0.26.0']}

setup_kwargs = {
    'name': 'wintry',
    'version': '0.1.0a0',
    'description': 'A Web Framework for you, the developer, in a clean way, a cool way',
    'long_description': None,
    'author': 'adriangs1996',
    'author_email': 'adriangonzalezsanchez1996@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
