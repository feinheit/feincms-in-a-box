from __future__ import print_function, unicode_literals

from fabric.api import task

from fabfile.config import local


@task(default=True)
def check():
    local('flake8 .')
    local('venv/bin/python manage.py check')
