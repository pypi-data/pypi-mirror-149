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
    'version': '0.1.3',
    'description': 'A django package to enable integration with Ory Cloud',
    'long_description': '# Ory Django\n\nThis package provides integration with Ory Cloud or Ory Kratos for your django application\n\n## Installing\n\nYou can simply run\n\n```\n   pip install django_ory_auth\n```\n\nor\n\n```\n   poetry add django_ory_auth\n```\n\nor\n\n```\n   pipenv install django_ory_auth\n```\n\nAdd `django_ory_auth` to `INSTALLED_APPS`\n\n```python\nINSTALLED_APPS = [\n    "django.contrib.admin",\n    "django.contrib.auth",\n    "django.contrib.contenttypes",\n    "django.contrib.sessions",\n    "django.contrib.sites",\n    "django_ory_auth"\n]\n```\n\n## Configuration\n\nYou need to add these variables to your settings\n\n```python\nORY_SDK_URL=https://projectId.projects.oryapis.com\nORY_UI_URL=https://projectId.projects.oryapis.com/ui\nLOGIN_URL=https://projectId.projects.oryapis.com/ui/login\n```\n\n`django_ory_auth` provides authentication backend. You must replace `ModelBackend` with `OryBackend` in the `AUTHENTICATION_BACKENDS` setting\n\n```python\nAUTHENTICATION_BACKENDS = [\n    "django_ory_auth.backend.OryBackend",\n]\n```\n\nLast step is to add `django_ory_auth.middleware.AuthenticationMiddleware` under `django.contrib.auth.middleware.AuthenticationMiddleware`\n\n```python\n\nMIDDLEWARE = [\n    …\n    "django.contrib.auth.middleware.AuthenticationMiddleware",\n    "django_ory_auth.middleware.AuthenticationMiddleware",\n    ...\n]\n```\n\n## Using context processors\n\nThe package provides context processor to provide the following urls\n\n- login_url\n- logout_url (for authenticated users)\n- signup_url\n- recovery_url\n- verify_url\n- profile_url (available for authenticated users)\n\nto enable context processor add `django_ory_auth.context.processor` to the `context_processor` setting\n',
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
