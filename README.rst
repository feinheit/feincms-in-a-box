=================================
FeinCMS in a Box for cookiecutter
=================================

Prerequisites
-------------

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

Node.js and npm are also required::

    sudo apt-get install npm  # On Debian-derivatives
    brew install npm  # On OS X

You also need an up-to-date installation of
`foundation <http://foundation.zurb.com>`_::

    [sudo] gem install foundation
    [sudo] npm install -g bower grunt-cli

`pip <http://www.pip-installer.org/>`_,
`virtualenv <http://www.virtualenv.org/>`_,
`Fabric <http://fabfile.org>`_ and
`cookiecutter <https://pypi.python.org/pypi/cookiecutter/>`_::

    sudo pip install -U pip virtualenv fabric cookiecutter

If ``pip`` is missing on your system, you can install it using
``easy_install``.  That's also the one and only occasion when ``easy_install``
should be used::

    sudo easy_install pip

Also, you need `PostgreSQL <http://www.postgresql.org/>`_ up and running.

On Debian-derivatives::

    sudo apt-get install postgresql

On OS X::

    brew install postgresql   # On OS X
    echo "export PGDATA=/usr/local/var/postgres" >> .profile
    source ~/.profile
    postgres


Installation
------------

Ensure that postgres and redis-server are running. Run cookiecutter and follow
the instructions on-screen::

    cookiecutter https://github.com/matthiask/cookiecutter-feincms-in-a-box

Enjoy!
