from __future__ import print_function, unicode_literals

from fabric.api import task

from fabfile.config import local


@task(default=True)
def check():
    local("! git grep -n -C3 -E 'import i?pdb' -- '*.py'")
    local("! git grep -n -C3 -E 'console\.log' -- '*.html' '*.js'")
    local("! git grep -n -C3 -E 'print' -- '%(box_project_name)s/*py'")
    local('flake8 .')
    local('venv/bin/python manage.py check')
