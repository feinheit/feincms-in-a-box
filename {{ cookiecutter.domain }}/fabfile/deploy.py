from __future__ import print_function, unicode_literals

from fabric.api import execute, task

from fabfile.config import local, cd, run


@task(default=True)
def deploy():
    local('flake8 .')
    execute('deploy.styles')
    execute('deploy.code')


@task
def styles():
    local('cd {sass} && grunt build')
    for part in ['bower_components', 'css']:
        local('rsync -avz {sass}/%s {server}:{domain}/{sass}/' % part)
    with cd('{domain}'):
        run('venv/bin/python manage.py collectstatic --noinput')


@task
def code():
    local('flake8 .')
    local('git push origin {branch}')
    with cd('{domain}'):
        run('git fetch')
        run('git reset --hard origin/{branch}')
        run('find . -name "*.pyc" -delete')
        run('venv/bin/pip install -r requirements/live.txt'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')
        run('venv/bin/python manage.py syncdb')
        run('venv/bin/python manage.py migrate')
        run('venv/bin/python manage.py collectstatic --noinput')
        run('sctl restart {domain}:*')
