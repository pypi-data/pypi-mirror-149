===========================
Django Admin Oauth Sessions
===========================


.. image:: https://img.shields.io/pypi/v/django_admin_oauth_sessions.svg
        :target: https://pypi.python.org/pypi/django_admin_oauth_sessions


.. image:: https://readthedocs.org/projects/django-admin-oauth-sessions/badge/?version=latest
        :target: https://django-admin-oauth-sessions.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A django Project for custom authentication for sso tokens


* Free software: BSD license
* Documentation: https://django-admin-oauth-sessions.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



django_admin_oauth_sessions is a Django app to validate SSO tokens.


Quick start
-----------

1. Add "django_admin_auth_keycloak" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_admin_oauth_sessions',
    ]

2. Add "DjangoAdminOAuthSessionMiddleware" in your MIDDLEWARE in settings file::

    MIDDLEWARE = [
        ...
        'django_admin_oauth_sessions.django_admin_oauth_sessions.DjangoAdminOAuthSessionMiddleware',
    ]

3. Update the logout url in urls.py as::

    path('admin/logout/', logout_view, name='logout')
    import logout_view from django_admin_oauth_sessions
    e.g from django_admin_oauth_sessions.views import logout_view


4. Start the development server::

    visit http://localhost:8000/admin/
    to create a django_admin_oauth_sessions (you'll need the Admin app enabled).

