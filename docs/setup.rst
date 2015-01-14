.. _setup:

=====
Setup
=====

Setting up a new project
========================

After following all the steps outlined in :ref:`prerequisites`, you're now
ready to generate the first project. A folder is automatically created. It will
have the slugified domain name as folder name.

Run the following commands inside a terminal of your choice::

    git clone git://github.com/feinheit/feincms-in-a-box
    cd feincms-in-a-box
    ./generate.py --help

A command line to create a site for ``http://some.example.tld`` named
``A nice example`` would be::

    ./generate.py some.example.tld "A nice example"

A full list of all supported options is available with
``./generate.py --help``. It is also recommended to create a file named
``.box.env`` in your home folder containing the following values::

    BITBUCKET_USERNAME=<Your bitbucket username>
    BITBUCKET_ORGANIZATION=<The bitbucket organization for all repositories>
    SERVER=<username@server.tld where your sites will be hosted>
    SSO_DOMAIN=<domain.tld for django-admin-sso>

The project will be created inside the ``build/`` folder by default. ``cd``
into that directory and run ``fab local.setup`` to continue the setup. The
setup step should complete successfully, if it does not please report it as
a bug_!

.. _bug: https://www.pivotaltracker.com/projects/1156128


Further steps
-------------

- ``fab dev``: Starts the development server and background services (if they
  are not running already).
- ``fab git.init_bitbucket``: Uploads the project to bitbucket.
- ``fab server.setup``: Installs the project on a server. The project has to
  be cloneable from somewhere, Github or Bitbucket. Please note that the
  server setup scripts are heavily tailored for our setup and probably will
  not work without modifications for other hosters.
- Configure `Admin SSO`_


Setting up a local development installation of an existing project
==================================================================

Obviously you also have to complete all steps outlined in :ref:`prerequisites`.
After that, clone the repository and run the setup command::

    git clone <repo-url>
    cd <project>
    fab local.setup_with_production_data


Installing the project on a server
==================================

That's all::

    fab server.setup


Installing a staging copy of an existing project
================================================

First, edit ``fabfile/config.py`` and remove (or comment out) the line
``env.box_hardwired_environment = 'production'``. This activates multi-env
support which is required to work with several installations of the same code
base.

Switch to the ``develop`` branch (creating it if it does not exist already),
and run the following commands::

    fab staging server.setup
    fab staging server.copy_data_from:production

If the staging site is not required anymore, it can be removed using the
following command::

    fab staging server.remove_host


.. _`Admin SSO`: https://github.com/frog32/django-admin-sso/blob/develop/README.rst