=================
django-start-tool
=================

.. image:: https://img.shields.io/pypi/v/django-start-tool.svg
    :target: https://pypi.org/project/django-start-tool
    :alt: PyPI

.. image:: https://img.shields.io/pypi/l/django-start-tool.svg
    :target: https://choosealicense.com/licenses/mit
    :alt: License

Introduction
------------

**django-start-tool** is a full-featured django_ project start tool.

.. _django: https://www.djangoproject.com

Installing
----------

Install and update:

.. code-block:: console

    $ pip install -U django-start-tool

Usage
-----

Create base project structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default ``project_name`` is ``config``
and ``target`` is ``.`` (current directory).

.. code-block:: console

    $ django-start
    # is equivalent to
    $ django-start config .

Structure is the same as `django-admin startproject`_:

.. _`django-admin startproject`: https://docs.djangoproject.com/en/4.0/ref/django-admin/#startproject

.. code-block::

    .
    ├── config
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── manage.py

Creating from template
~~~~~~~~~~~~~~~~~~~~~~

Option: ``-t <path or url>``, ``--template <path or url>``

.. code-block:: console

    $ django-start \
    > -t /path/to/template

    $ django-start \
    > -t https://github.com/user/repository/archive/main.zip

For example template have this structure:

.. code-block::

    /path/to/template
    ├── .env
    ├── .gitignore
    ├── manage.py-tpl
    ├── Pipfile
    ├── Pipfile.lock
    └── project_name
        ├── asgi.py-tpl
        ├── __init__.py
        ├── settings
        │   ├── base.py-tpl
        │   ├── development.py
        │   ├── __init__.py
        │   └── production.py
        ├── urls.py
        └── wsgi.py-tpl

Rendering files
~~~~~~~~~~~~~~~~~~~~~

There are two ways to specify which files should be rendered.

Using suffix
""""""""""""

**All** files with ``-tpl`` suffix will be renamed with no suffix and rendered.

.. code-block:: python

    # base.py-tpl -> base.py

    # From
    SECRET_KEY = '{{ secret_key }}'
    ROOT_URLCONF = '{{ project_name }}.urls'

    # To
    SECRET_KEY = 'django-insecure-3%=4apmw6jb(+$)x#8gu(3@0*vfzoh+e#jg5rdmkb#u=048qe&'  # Key is generated randomly
    ROOT_URLCONF = 'config.urls'  # By default 'project_name' is 'config'

.. code-block:: shell

    # .env-tpl -> .env

    # From
    SECRET_KEY='{{ secret_key }}'

    # To
    SECRET_KEY='django-insecure-3%=4apmw6jb(+$)x#8gu(3@0*vfzoh+e#jg5rdmkb#u=048qe&'  # Key is generated randomly

Using CLI option
""""""""""""""""

Option: ``-f '<patterns>'``, ``--files '<patterns>'``.

It takes space-separated glob patterns:

.. code-block:: console

    $ django-start \
    > -t /path/to/template \
    > -f '*.env *.rst Procfile'

Then **all** matched files will be rendered too.

.. code-block:: shell

    # .env

    # From
    SECRET_KEY='{{ secret_key }}'

    # To
    SECRET_KEY='django-insecure-3%=4apmw6jb(+$)x#8gu(3@0*vfzoh+e#jg5rdmkb#u=048qe&'  # Key is generated randomly

Extra configuration parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Option: ``-e '<parameters>'``, ``--extra '<parameters>'``

It takes space-separated key value pairs which will be available from ``extra`` object in Jinja2 template:

.. code-block:: console

    $ django-start \
    > -t /path/to/template \
    > -f '*.env *.rst Procfile' \
    > -e 'db_name=postgres db_password=secret! my_var=Hello'

.. code-block:: shell

    # .env

    # From
    DB_NAME='{{ extra.db_name }}'
    DB_PASSWORD='{{ extra.db_password }}'

    VAR='{{ extra.my_var }}'

    # To
    DB_NAME='postgres'
    DB_PASSWORD='secret!'

    VAR='Hello'

Excluding directories
~~~~~~~~~~~~~~~~~~~~~

Option: ``-x '<patterns>'``, ``--exclude <patterns>``

It takes space-separated glob patterns:

.. code-block:: console

    $ django-start \
    > -t /path/to/template \
    > -x '.github'

Then **all** matched directies will be excluded.

By default it's ``__pycache__`` or starting with ``.``.
