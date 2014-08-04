================
FeinCMS in a Box
================

Useful commands:

- ``fab dev``:
  Starts the development server and a grunt task which watches the SCSS files
  and recompiles them if anything changes. Also starts a redis and a postgres
  instance if connecting locally fails.

- ``fab deploy``:
  Deploys and restarts everything on the server (if installed already).

- ``fab setup_local``:
  Create a new local development environment. Installs all dependencies.

- ``fab setup_local.setup_with_live_data``:
  Create the local development environment and pull down the database and all
  mediafiles from the server. The services redis and postgres have to be
  running already.

Get the whole list: ``fab -l`` (or ``fab --list``)
