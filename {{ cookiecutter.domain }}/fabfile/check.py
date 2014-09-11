from __future__ import print_function, unicode_literals

from fabric.api import task
from fabric.utils import abort

from fabfile.config import local


_invalid_contents = [
    (r'import i?pdb', '*.py'),
]


@task(default=True)
def check():
    for row in _invalid_contents:
        output = local(
            'git grep -n -C3 -E \'%s\' -- \'%s\' ; echo $?' % row,
            capture=True)
        if output.strip().endswith('\n0'):
            abort('Invalid file contents, aborting.')

    local('flake8 .')
    local('venv/bin/python manage.py check')
