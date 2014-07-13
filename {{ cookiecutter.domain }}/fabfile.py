from __future__ import print_function, unicode_literals

from functools import wraps
import getpass
from io import StringIO
import os
import platform
import random
import re

from fabric.api import (
    env, execute, hide, prompt, put, settings, task,
    cd as cd_raw,
    local as local_raw,
    run as run_raw)
from fabric.colors import green, red
from fabric.contrib.console import confirm


CONFIG = {
    'project_name': '{{ cookiecutter.project_name }}',
    'domain': '{{ cookiecutter.domain }}',
    'server': '{{ cookiecutter.server }}',
    'branch': 'master',
}


CONFIG.update({
    'repository_name': re.sub(r'[^\w]+', '_', CONFIG['domain']),
    'database_name': re.sub(r'[^\w]+', '_', CONFIG['domain']),
    'sass': '{project_name}/static/{project_name}'.format(**CONFIG),
    'server_name': CONFIG['server'].split('@')[-1],
})


env.forward_agent = True
env.hosts = [CONFIG['server']]


def format_with_config(fn):
    @wraps(fn)
    def _dec(string, *args, **kwargs):
        return fn(string.format(**CONFIG), *args, **kwargs)
    return _dec


local = format_with_config(local_raw)
cd = format_with_config(cd_raw)
run = format_with_config(run_raw)


def get_random_string(length, chars=None):
    rand = random.SystemRandom()
    if chars is None:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(rand.choice(chars) for i in range(50))


@task
def dev():
    import socket
    from threading import Thread
    jobs = [
        Thread(target=lambda: execute('watch_styles')),
        Thread(target=lambda: execute('runserver')),
    ]
    try:
        socket.create_connection(('localhost', 6379), timeout=0.1).close()
    except socket.error:
        jobs.append(Thread(target=lambda: local('redis-server')))
    [j.start() for j in jobs]
    [j.join() for j in jobs]


@task(alias='ws')
def watch_styles():
    local('cd {sass} && grunt')


@task(alias='rs')
def runserver(port=8000):
    local('venv/bin/python -Wall manage.py runserver 0.0.0.0:{}'.format(port))


@task
def deploy_styles():
    local('cd {sass} && grunt build')
    for part in ['bower_components', 'css']:
        local('rsync -avz {sass}/%s {server}:{domain}/{sass}/' % part)
    with cd('{domain}'):
        run('venv/bin/python manage.py collectstatic --noinput')


@task
def deploy_code():
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


@task
def deploy():
    local('flake8 .')
    execute('deploy_styles')
    execute('deploy_code')


@task
def setup():
    if os.path.exists('venv'):
        print(red('It seems that this project is already set up, aborting.'))
        return 1

    local('virtualenv venv')
    if platform.system() == 'Darwin' and platform.mac_ver()[0] >= '10.9':
        local(
            'export CFLAGS=-Qunused-arguments'
            ' && export CPPFLAGS=-Qunused-arguments'
            ' && venv/bin/pip install -r requirements/dev.txt')
    else:
        local('venv/bin/pip install -r requirements/dev.txt')

    with open('{{ cookiecutter.project_name }}/local_settings.py', 'w') as f:
        CONFIG['secret_key'] = get_random_string(50)
        f.write('''\
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%(database_name)s',
    }
}
SECRET_KEY = '%(secret_key)s'
RAVEN_CONFIG = {
    'dsn': '',  # Unused in local development.
}
ALLOWED_HOSTS = ['*']
''' % CONFIG)

    local('cd {sass} && npm install')
    local('cd {sass} && bower install')

    local('createdb {database_name} --encoding=UTF8 --template=template0')
    local('venv/bin/python manage.py syncdb --noinput')
    local('venv/bin/python manage.py migrate --noinput medialibrary')
    local('venv/bin/python manage.py migrate --noinput elephantblog')
    local('venv/bin/python manage.py migrate --noinput form_designer')
    local('venv/bin/python manage.py migrate --noinput page')
    local('venv/bin/python manage.py migrate --noinput')

    print(green('Initial setup has completed successfully!', bold=True))
    print(green('Next steps:'))
    print(green(
        '- Create a superuser: venv/bin/python manage.py createsuperuser'))
    print(green('- Run the development server: fab dev'))
    print(green(
        '- Create a Bitbucket repository: fab init_bitbucket'))
    print(green('- Configure {server_name} for this project: fab init_server'))


@task
def pull_database():
    if not confirm('Completely replace the local database (if it exists)?'):
        return

    with settings(warn_only=True):
        local('dropdb {database_name}')

    local('createdb {database_name} --encoding=UTF8 --template=template0')
    local(
        'ssh {server} "source .profile &&'
        ' pg_dump {database_name} --no-privileges --no-owner --no-reconnect"'
        ' | psql {database_name}')


@task
def pull_mediafiles():
    if not confirm('Completely replace local mediafiles?'):
        return
    local('rsync -avz --delete {server}:{domain}/media .')


@task
def init_bitbucket():
    username = prompt('Username', default=os.environ.get('USER', ''))
    password = getpass.getpass('Password ')
    organization = prompt('Organization', default='feinheit')
    repository_name = prompt(
        'Repository',
        default=CONFIG['repository_name'])

    if not confirm(
        'Initialize repository at https://bitbucket.org/%s/%s?' % (
            organization, repository_name)):

        print(red('Bitbucket repository creation aborted.'))
        return 1

    if username and password and organization and repository_name:
        with hide('running'):
            local_raw(
                'curl -X POST -u %s:%s -H "content-type: application/json"'
                ' https://api.bitbucket.org/2.0/repositories/%s/%s'
                ' -d \'{"scm": "git", "is_private": true,'
                ' "forking_policy": "no_public_forks"}\'' % (
                    username,
                    password,
                    organization,
                    repository_name))

        with settings(warn_only=True):
            local('git remote rm origin')

        local('git remote add origin git@bitbucket.org:%s/%s.git' % (
            organization,
            repository_name))

        local('git push -u origin master')


@task
def init_server():
    execute('init_server_step1_clone_repository')
    execute('init_server_step2_create_virtualenv')
    execute('init_server_step3_create_database_and_local_settings')
    execute('init_server_step4_nginx_vhost_and_supervisor')
    execute('deploy_styles')
    print(green('Visit http://{domain}.{server_name} now!'.format(**CONFIG)))
    print(green('Create a SSO user: fab create_sso_user'))


@task
def init_server_step1_clone_repository():
    print(green('We need the repository to initialize the server.'))
    with hide('running'):
        output = local('git config remote.origin.url', capture=True)
    repo = prompt('Repository', default=output)

    if not repo:
        print(red('Cannot continue without a repository.'))
        return 1

    CONFIG['repository_url'] = repo

    run('git clone {repository_url} {domain}')
    with settings(warn_only=True):
        local('git remote add -f live {server}:{domain}/')


@task
def init_server_step2_create_virtualenv():
    with cd('{domain}'):
        run('virtualenv --python python2.7 --prompt "(venv:{domain})" venv')
        run('venv/bin/pip install -U virtualenv pip wheel'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')
        run('venv/bin/pip install -U setuptools'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')
        run('venv/bin/pip install -r requirements/live.txt'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')


@task
def init_server_step3_create_database_and_local_settings():
    print('\nProvide a few details and secrets for the installation, please:')
    CONFIG['sentry_dsn'] = prompt('Sentry DSN')
    CONFIG['oauth2_client_id'] = prompt('Google OAuth2 Client ID')
    CONFIG['oauth2_client_secret'] = prompt('Google OAuth2 Client Secret')

    CONFIG['database_pw'] = get_random_string(
        20, chars='abcdefghijklmopqrstuvwx01234567890')
    CONFIG['secret_key'] = get_random_string(50)

    run('psql -c "CREATE ROLE {database_name} WITH'
        ' ENCRYPTED PASSWORD \'{database_pw}\''
        ' LOGIN NOCREATEDB NOCREATEROLE NOSUPERUSER"')
    run('psql -c "GRANT {database_name} TO admin"')
    run('psql -c "CREATE DATABASE {database_name} WITH'
        ' OWNER {database_name}'
        ' TEMPLATE template0'
        ' ENCODING \'UTF8\'"')

    with cd('{domain}'):
        put(StringIO('''\
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%(database_name)s',
        'USER': '%(database_name)s',
        'PASSWORD': '%(database_pw)s',
        'HOST': 'localhost',
        'PORT': '',
    }
}
SECRET_KEY = '%(secret_key)s'
RAVEN_CONFIG = {
    'dsn': '%(sentry_dsn)s',  # noqa
}
ALLOWED_HOSTS = ['.%(domain)s', '.feinheit04.nine.ch']

DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID = '%(oauth2_client_id)s'
DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET = '%(oauth2_client_secret)s'

if all((
    DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID,
    DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET,
)):
    DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON = True
''' % CONFIG), '%(project_name)s/local_settings.py' % CONFIG)

        run('venv/bin/python manage.py syncdb --noinput')
        run('venv/bin/python manage.py migrate --noinput medialibrary')
        run('venv/bin/python manage.py migrate --noinput elephantblog')
        run('venv/bin/python manage.py migrate --noinput form_designer')
        run('venv/bin/python manage.py migrate --noinput page')
        run('venv/bin/python manage.py migrate --noinput')


@task
def init_server_step4_nginx_vhost_and_supervisor():
    run('sudo nine-manage-vhosts virtual-host create {domain}'
        ' --template=feinheit --relative-path=htdocs')

    with cd('{domain}'):
        run('mkdir media tmp')

    run('supervisor-create-conf {domain} wsgi'
        ' > supervisor/conf.d/{domain}.conf')
    run('sctl reload')


@task
def create_sso_user():
    domain = prompt('SSO Domain', default='feinheit.ch')
    run('psql {database_name} -c "INSERT INTO auth_user VALUES'
        " (1, '', NOW(), TRUE, 'admin', '', '', '', TRUE, TRUE, NOW())\"")
    run('psql {database_name} -c "INSERT INTO admin_sso_assignment VALUES'
        " (1, 0, '', '%s', FALSE, 10, 1)\"" % domain)
