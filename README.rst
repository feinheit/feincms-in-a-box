================
FeinCMS in a Box
================


Instructions::

    git clone git://github.com/matthiask/feincms-in-a-box.git box
    cd box
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements/dev.txt
    echo "SECRET_KEY = 'unsafe'" > box/local_settings.py
    ./manage.py syncdb --all
    ./manage.py migrate --all --fake
    fab dev

    open http://127.0.0.1:8038/admin/

    # OR xdg-open http://127.0.0.1:8038/admin/
