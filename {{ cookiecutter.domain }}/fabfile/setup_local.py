from __future__ import print_function, unicode_literals

import os
import platform

from fabric.api import env, execute, settings, task
from fabric.colors import green, red
from fabric.contrib.console import confirm

from fabfile.config import local, get_random_string


@task(default=True)
def initial_setup():
    # TODO(mk) Check whether postgres is up and running before starting?

    if os.path.exists('venv'):
        print(red('It seems that this project is already set up, aborting.'))
        return 1

    execute('setup_local.create_virtualenv')
    execute('setup_local.frontend_tools')
    execute('setup_local.create_local_settings')
    execute('setup_local.create_and_migrate_database')

    print(green(
        'Initial setup has completed successfully!', bold=True))
    print(green(
        'Next steps:'))
    print(green(
        '- Create a superuser: venv/bin/python manage.py createsuperuser'))
    print(green(
        '- Run the development server: fab dev'))
    print(green(
        '- Create a Bitbucket repository: fab versioning.init_bitbucket'))
    print(green(
        '- Configure %(box_server_name)s for this project: fab setup_server'))


@task
def setup_with_live_data():
    if os.path.exists('venv'):
        print(red('It seems that this project is already set up, aborting.'))
        return 1

    execute('setup_local.create_virtualenv')
    execute('setup_local.frontend_tools')
    execute('setup_local.create_local_settings')
    execute('setup_local.pull_database')
    execute('setup_local.pull_mediafiles')

    print(green(
        'Setup with live data has completed successfully!', bold=True))
    print(green(
        'Next steps:'))
    print(green(
        '- Create a superuser: venv/bin/python manage.py createsuperuser'))
    print(green(
        '- Run the development server: fab dev'))


@task
def create_virtualenv():
    local(
        'virtualenv --python python2.7'
        ' --prompt "(venv:%(box_domain)s)" venv')
    local('venv/bin/pip install -U wheel setuptools pip')
    if platform.system() == 'Darwin' and platform.mac_ver()[0] >= '10.9':
        local(
            'export CFLAGS=-Qunused-arguments'
            ' && export CPPFLAGS=-Qunused-arguments'
            ' && venv/bin/pip install -r requirements/dev.txt')
    else:
        local('venv/bin/pip install -r requirements/dev.txt')


@task
def frontend_tools():
    local('cd %(box_sass)s && npm install')
    local('cd %(box_sass)s && bower install')


@task
def create_local_settings():
    with open('%(box_project_name)s/local_settings.py' % env, 'w') as f:
        env.box_secret_key = get_random_string(50)
        f.write('''\
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%(box_database_name)s',
    }
}
SECRET_KEY = '%(box_secret_key)s'
RAVEN_CONFIG = {
    'dsn': '',  # Unused in local development.
}
ALLOWED_HOSTS = ['*']
''' % env)


@task
def create_and_migrate_database():
    local(
        'createdb %(box_database_name)s'
        ' --encoding=UTF8 --template=template0')
    local('venv/bin/python manage.py migrate')


@task
def pull_database():
    if not confirm('Completely replace the local database (if it exists)?'):
        return

    with settings(warn_only=True):
        local('dropdb %(box_database_name)s')

    local(
        'createdb %(box_database_name)s'
        ' --encoding=UTF8 --template=template0')
    local(
        'ssh %(box_server)s "source .profile &&'
        ' pg_dump %(box_database_name)s'
        ' --no-privileges --no-owner --no-reconnect"'
        ' | psql %(box_database_name)s')
    local(
        'psql %(box_database_name)s -c "UPDATE auth_user'
        ' SET password=\'pbkdf2_sha256\$12000\$owbr7vjRCspg\$PAo53Cbqvek3nMqS'
        'l+V+ubIlnZQ2Vj7ZVKcPhcXqWlY=\''
        ' WHERE password=\'\'"')
    print(green(
        'Users with empty passwords (for example SSO users) now have a'
        ' password of "password" (without quotes).'))


@task
def pull_mediafiles():
    if not confirm('Completely replace local mediafiles?'):
        return
    local('rsync -avz --delete %(box_server)s:%(box_domain)s/media .')
