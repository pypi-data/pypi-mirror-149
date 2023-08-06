# Ory Django

This package provides integration with Ory Cloud or Ory Kratos for your django application

## Installing

You can simply run

```
   pip install django_ory_auth
```

or

```
   poetry add django_ory_auth
```

or

```
   pipenv install django_ory_auth
```

Add `django_ory_auth` to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django_ory_auth"
]
```

## Configuration

You need to add these variables to your settings

```python
ORY_SDK_URL=https://projectId.projects.oryapis.com
ORY_UI_URL=https://projectId.projects.oryapis.com/ui
LOGIN_URL=https://projectId.projects.oryapis.com/ui/login
```

`django_ory_auth` provides authentication backend. You must replace `ModelBackend` with `OryBackend` in the `AUTHENTICATION_BACKENDS` setting

```python
AUTHENTICATION_BACKENDS = [
    "django_ory_auth.backend.OryBackend",
]
```

Last step is to add `django_ory_auth.middleware.AuthenticationMiddleware` under `django.contrib.auth.middleware.AuthenticationMiddleware`

```python

MIDDLEWARE = [
    …
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_ory_auth.middleware.AuthenticationMiddleware",
    ...
]
```

## Using context processors

The package provides context processor to provide the following urls

- login_url
- logout_url (for authenticated users)
- signup_url
- recovery_url
- verify_url
- profile_url (available for authenticated users)

to enable context processor add `django_ory_auth.context.processor` to the `context_processor` setting
