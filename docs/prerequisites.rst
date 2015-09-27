.. _prerequisites:

=============
Prerequisites
=============

The feincms-in-a-box project template has a few prerequisites. This page
explains how to prepare your system for the initial setup and continued
development.


Operating system-specific instructions
======================================

Debian and Ubuntu
-----------------

Install the following libraries, tools and services::

    sudo apt-get install build-essential python-dev python-pip \
    python-virtualenv libjpeg8-dev liblcms2-dev libopenjpeg-dev libwebp-dev \
    libpng12-dev libtiff4-dev libxslt1-dev libfreetype6-dev \
    postgresql-9.3 postgresql-server-dev-9.3 gettext npm redis-server

.. note::

   Other versions of PostgreSQL_ will work as well if you are running a
   different version of Debian or Ubuntu.


OS X
----

An installation of Xcode including command line tools is required::

    xcode-select --install

It is recommended to use Homebrew_ for all additional dependencies::

    brew install gettext libxslt libxml2 jpeg freetype libpng
    brew install libtiff node postgresql redis sqlite
    brew link --force gettext

It will also help to add a clean installation of Python_::

    brew install python

It is not required to set up an installation of PostgreSQL_ which runs in the
background. Adding the following lines to your ``~/.bash_profile`` and starting
``postgres`` in the shell is good enough for local development::

    echo "export PGDATA=/usr/local/var/postgres" >> ~/.bash_profile

You can also just install the `Postgres App <http://postgresapp.com/>`_.
You then need to add the app to the PATH variable (depending on the version)::

    PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"

.. note::

   You'll have to open a new Terminal, otherwise the ``PGDATA`` of ``.profile``
   environment variable will not be available.


Python-based command line tools
===============================

We also require a few Python-based command line tools, Fabric_ and flake8_. It
is very much recommended to use pipsi_ for their installation.  Instructions
for installing pipsi_ can be found on
`Github <https://github.com/mitsuhiko/pipsi>`_::

    pip install virtualenv
    pipsi install fabric
    pipsi install flake8


Node-based command line tools
=============================

Install the following packages using npm_::

    npm install -g bower jshint

gulp_ is recommended, but not strictly required::

    npm install -g gulp


.. _PostgreSQL: http://www.postgresql.org/
.. _Homebrew: http://brew.sh/
.. _Python: https://www.python.org/
.. _Fabric: http://fabfile.org/
.. _flake8: https://pypi.python.org/pypi/flake8
.. _pipsi: https://github.com/mitsuhiko/pipsi
.. _npm: https://www.npmjs.org/
.. _gulp: http://gulpjs.com/
