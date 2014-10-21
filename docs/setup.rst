.. _setup:

=====
Setup
=====

Setting up a new project
========================

After following all the steps outlined in :ref:`prerequisites`, you're now
ready to generate the first project. A folder is automatically created. It will
have the domain name as folder name.

Run the following command inside a terminal of your choice::

    cookiecutter https://github.com/feinheit/cookiecutter-box

You'll be asked a few questions:

- ``nice_name``: Some nice, descriptive name. This variable will be used to
  fill in the initial ``<title>``, among other things.
- ``project_name`` (Defaults to ``box``): The name of the main Python module.
  If you have no differing preferences, just keep ``box``.
- ``domain``: The final domain for this project. This value is also slugified
  and used as default database and repository name, so choose well.
- ``server``: The server this project will be deployed to. Currently
  cookiecutter-box has many assumptions about server layout, deployment will
  probably not work out-of-the-box if you have a different setup (which you
  will most probably have).

Next, ``fab setup_local`` will be executed automatically. The setup step should
complete successfully, if it does not please report it as a bug_!

.. _bug: https://www.pivotaltracker.com/projects/1156128


Further steps
-------------

- ``fab dev``: Starts the development server and background services (if they
  are not running already).
- ``fab versioning.init_bitbucket``: Uploads the project to bitbucket.
- ``fab setup_server``: Installs the project on a server. The project has to be
  cloneable from somewhere, Github or Bitbucket.


Setting up a local development installation of an existing project
==================================================================

Obviously you also have to complete all steps outlined in :ref:`prerequisites`.
After that, clone the repository and run the setup command::

    git clone <repo-url>
    cd <project>
    fab setup_local.setup_with_production_data


Installing the project on a server
==================================

That's all::

    fab setup_server


Installing a staging copy of an existing project
================================================

First, edit ``fabfile/config.py`` and remove (or comment out) the line
``env.box_hardwired_environment = 'production'``. This activates multi-env
support which is required to work with several installations of the same code
base.

Switch to the ``develop`` branch (creating it if it does not exist already),
and run the following commands::

    fab staging setup_server
    fab staging setup_server.copy_data_from:production

If the staging site is not required anymore, it can be removed using the
following command::

    fab staging remove_host
