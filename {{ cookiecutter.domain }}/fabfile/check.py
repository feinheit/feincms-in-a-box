from __future__ import print_function, unicode_literals

from fabric.api import task

from fabfile.config import local


_invalid_contents = [
    (r'import i?pdb', '*.py'),
    (r'console.log', '*.js'),
    (r'console.log', '*.html'),
]


@task(default=True)
def check():
    for row in _invalid_contents:
        local('! git grep -n -C3 -E \'%s\' -- \'%s\'' % row)

    local('flake8 .')
    local('venv/bin/python manage.py check')
