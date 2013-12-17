================
FeinCMS in a Box
================

Prerequisites
-------------

An up-to-date installation of compass and zurb-foundation 4.3.2::

    (sudo) gem install compass
    (sudo) gem install zurb-foundation --version '=4.3.2'

Under Debian-derivatives, you need the following libraries::

    sudo apt-get install build-essential python-dev libjpeg8-dev\
    libxslt1-dev libfreetype6-dev

Under OS X, you need an installation of Xcode. It is also recommended
to install `Homebrew <http://brew.sh/>`_, and install the following
packages::

    brew install gettext
    brew install libxslt
    brew install libxml2
    brew install jpeg


Installattion
-------------

The following commands should get you up and running::

    git clone git://github.com/matthiask/feincms-in-a-box.git box
    cd box
    git remote rm origin
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements/dev.txt
    echo "SECRET_KEY = 'unsafe'" > box/local_settings.py
    ./manage.py syncdb --all
    ./manage.py migrate --all --fake
    fab dev

    open http://127.0.0.1:8038/admin/

    # OR xdg-open http://127.0.0.1:8038/admin/
