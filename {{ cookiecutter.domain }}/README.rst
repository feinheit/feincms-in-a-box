================
{{ cookiecutter.domain }}
================

Overview
========

- Title: ...
- Repository: https://bitbucket.org/feinheit/{{ cookiecutter.domain }}
- URL: http://www.{{ cookiecutter.domain }}/
- Production server: {{ cookiecutter.server }}:{{ cookiecutter.domain }}/


Project team
============

- Project manager: ...
- Design: ...
- Frontend programming: ...
- Backend programming: ...


Project description
===================

Modules
-------

- ``{{ cookiecutter.project_name }}.cms``:
  Django app containing FeinCMS configuration.


Management commands
-------------------

- ``./manage.py cleanup``:
  Standard Django management command to remove stale entries from the session
  database table.


Cronjobs
--------

Describe optional and required cronjobs for the project, and also mention the
preferred periodicity.


Dependencies on external services
=================================

Describe external services used here, if any.


Other dependencies
==================

Python packages are mostly contained in ``requirements/``.

JavaScript packages are currently defined in
``{{ cookiecutter.project_name }}/static/{{ cookiecutter.project_name }}/bower.json``.


Development and deployment
==========================

Useful commands:

- ``fab dev``:
  Starts the development server and a grunt task which watches the SCSS files
  and recompiles them if anything changes. Also starts a redis and a postgres
  instance if connecting to them locally fails.

- ``fab deploy``:
  Deploys and restarts everything on the server (if installed already).

- ``fab setup_local``:
  Create a new local development environment. Installs all dependencies.

- ``fab setup_local.setup_with_live_data``:
  Create the local development environment and pull down the database and all
  mediafiles from the server. The services redis and postgres have to be
  running already.

Get the whole list: ``fab -l`` (or ``fab --list``)
