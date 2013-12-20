================
FeinCMS in a Box
================

Prerequisites
-------------

An up-to-date installation of `bundler <http://bundler.io/>`_::

    sudo gem install bundler

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

Set up the frontend development tools::

    bundle install --path vendor/bundle

The following commands should get you up and running::

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements/dev.txt
    echo "SECRET_KEY = 'unsafe'" > box/local_settings.py
    ./manage.py syncdb --all
    ./manage.py migrate --all --fake
    fab dev

    open http://127.0.0.1:8000/admin/

    # OR xdg-open http://127.0.0.1:8000/admin/
