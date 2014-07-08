================
FeinCMS in a Box
================

Prerequisites
-------------

An up-to-date installation of `foundation <http://foundation.zurb.com>`_. These
commands assume that you have already installed nodejs and npm::

    [sudo] gem install foundation
    [sudo] npm install -g bower grunt-cli

`pip <http://www.pip-installer.org/>`_,
`virtualenv <http://www.virtualenv.org/>`_ and
`Fabric <http://fabfile.org>`_::

    sudo pip install -U pip virtualenv fabric

If ``pip`` is missing on your system, you can install it using
``easy_install``.  That's also the one and only occasion when ``easy_install``
should be used::

    sudo easy_install pip

Under Debian-derivatives, you need the following libraries to successfully
compile all dependencies of FeinCMS-in-a-Box, notably
`lxml <http://lxml.de/>`_ and
`Pillow <https://pypi.python.org/pypi/Pillow/>`_::

    sudo apt-get install build-essential python-dev libjpeg8-dev \
    libxslt1-dev libfreetype6-dev

Under OS X, you need an installation of Xcode. It is also recommended
to install `Homebrew <http://brew.sh/>`_, and install the following
packages::

    brew install gettext
    brew install libxslt
    brew install libxml2
    brew install jpeg


Installation
------------

First, clone this repository to a folder of your choice and change
into the newly created directory::

    git clone $REPOSITORY $FOLDER
    cd $FOLDER

For example, if you want to play around with FeinCMS-in-a-Box::

    git clone git://github.com/matthiask/feincms-in-a-box.git
    cd feincms-in-a-box

The following command should get you up and running::

    fab setup


Alternative installation method
-------------------------------

Alternatively (or if ``fab setup`` fails) you can run the commands by hand.
First, set up the frontend development tools::

    cd box/static/box && npm install
    cd box/static/box && bower install

Then, the backend development toolsuite. If developing on OS X Mavericks,
set the following environment variables (otherwise the Pillow compilation
will fail)::

    export CFLAGS=-Qunused-arguments
    export CPPFLAGS=-Qunused-arguments

Create a virtualenv and install the development packages::

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements/dev.txt

Create a file ``box/local_settings.py`` with the following contents::

    SECRET_KEY = 'unsafe'
    RAVEN_CONFIG = {}

Run the following commands::

    ./manage.py syncdb --all
    ./manage.py migrate --all --fake
    fab dev

    open http://127.0.0.1:8000/admin/

    # OR xdg-open http://127.0.0.1:8000/admin/
