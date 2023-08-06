# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_ory_auth']

package_data = \
{'': ['*']}

install_requires = \
['Django>3', 'requests', 'urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'django-ory-auth',
    'version': '0.1.0',
    'description': 'A django package to enable integration with Ory Cloud',
    'long_description': '# Ory Django\n\nThis package provides integration with Ory Cloud or Ory Kratos for your django application\n\n## Installing\n\nTBD\n\n## Configuration\n\nYou need to add these variables to your settings\n\n```\nORY_SDK_URL=https://projectId.projects.oryapis.com\nLOGIN_URL=https://projectId.projects.oryapis.com/ui/login\nLOGOUT_URL=https://projectId.projects.oryapis.com/logout\n```\n',
    'author': 'Andrew Minkin',
    'author_email': 'minkin.andrew@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gen1us2k/django_ory_auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
