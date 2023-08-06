=======
dc-auth
=======

dc-auth is a dedicated Django app to connect the Data Central authentication
backend (LDAP) to multiple dc sites (api, cms etc) via CAS.
It supports session-based authentication (tested) and JWT authentication
(untested).

For users outside of Data Central, you'll need to send us details about your
application in order to be able to connect, please contact us at
https://jira.aao.org.au/servicedesk/customer/portal/3.


Quick start
-----------
Add "dc_auth" + the following apps to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'rest_framework',
        'rest_framework.authtoken',
        'rest_auth',
        ...
        'dc_auth',
    ]

Add django_settings_export.settings_export to your project's
context_processors::

    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django_settings_export.settings_export',                   # <----
        ],
    },

Include the dc_auth URLconf in your project urls.py like this::

    path('auth/', include('dc_auth.urls')),

Migrate to create the Profile table. Run `python manage.py migrate`.

Start the development server and visit http://127.0.0.1:8000/auth/login to log
into your account.

Tests
-----

From the top-level directory run:

.. code-block::

    $ tox

dcauth comes with some helpers that tools building on dcauth can use,
specifically pytest fixtures for affiliation (`affiliation`) and test passwords
(`secure_password`), as well as factories and fixtures for the `User` and
`Profile` classes.

Installing for internal applications
------------------------------------

To install into another Data Central project, add `dc_auth` to your requirements
file (lock to a specific version), and ensure that pip is pointed to the DC
devpi instance.
