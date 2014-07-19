from __future__ import print_function, unicode_literals

from io import StringIO

from fabric.api import env, execute, hide, prompt, put, task
from fabric.colors import green, red

from fabfile.config import local, cd, run, get_random_string


@task(default=True)
def init():
    execute('setup_server.clone_repository')
    execute('setup_server.create_virtualenv')
    execute('setup_server.create_database_and_local_settings')
    execute('setup_server.nginx_vhost_and_supervisor')
    execute('deploy.styles')
    execute('setup_server.create_sso_user')
    print(green('Visit http://%(box_domain)s.%(box_server_name)s now!' % env))


@task
def clone_repository():
    print(green('We need the repository to initialize the server.'))
    with hide('running'):
        output = local('git config remote.origin.url', capture=True)
    repo = prompt('Repository', default=output)

    if not repo:
        print(red('Cannot continue without a repository.'))
        return 1

    env.box_repository_url = repo

    run('git clone %(box_repository_url)s %(box_domain)s')
    execute('versioning.add_live_remote')


@task
def create_virtualenv():
    with cd('%(box_domain)s'):
        run('virtualenv --python python2.7'
            ' --prompt "(venv:%(box_domain)s)" venv')
        run('venv/bin/pip install -U virtualenv pip wheel'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')
        run('venv/bin/pip install -U setuptools'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')
        run('venv/bin/pip install -r requirements/live.txt'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')


@task
def create_database_and_local_settings():
    env.box_sentry_dsn = prompt('Sentry DSN')
    env.box_oauth2_client_id = prompt('Google OAuth2 Client ID')
    env.box_oauth2_client_secret = prompt('Google OAuth2 Client Secret')

    env.box_database_pw = get_random_string(
        20, chars='abcdefghijklmopqrstuvwx01234567890')
    env.box_secret_key = get_random_string(50)

    run('psql -c "CREATE ROLE %(box_database_name)s WITH'
        ' ENCRYPTED PASSWORD \'%(box_database_pw)s\''
        ' LOGIN NOCREATEDB NOCREATEROLE NOSUPERUSER"')
    run('psql -c "GRANT %(box_database_name)s TO admin"')
    run('psql -c "CREATE DATABASE %(box_database_name)s WITH'
        ' OWNER %(box_database_name)s'
        ' TEMPLATE template0'
        ' ENCODING \'UTF8\'"')

    with cd('%(box_domain)s'):
        put(StringIO('''\
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%(box_database_name)s',
        'USER': '%(box_database_name)s',
        'PASSWORD': '%(box_database_pw)s',
        'HOST': 'localhost',
        'PORT': '',
    }
}
SECRET_KEY = '%(box_secret_key)s'
RAVEN_CONFIG = {
    'dsn': '%(box_sentry_dsn)s',  # noqa
}
ALLOWED_HOSTS = ['.%(box_domain)s', '.feinheit04.nine.ch']
# FORCE_DOMAIN = 'www.%(box_domain)s'  # ForceDomainMiddleware

DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID = '%(box_oauth2_client_id)s'
DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET = '%(box_oauth2_client_secret)s'

if all((
    DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID,
    DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET,
)):
    DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON = True
''' % env), '%(box_project_name)s/local_settings.py' % env)

        run('venv/bin/python manage.py migrate --noinput')


@task
def nginx_vhost_and_supervisor():
    run('sudo nine-manage-vhosts virtual-host create %(box_domain)s'
        ' --template=feinheit --relative-path=htdocs')

    with cd('%(box_domain)s'):
        run('mkdir media tmp')

    run('supervisor-create-conf %(box_domain)s wsgi'
        ' > supervisor/conf.d/%(box_domain)s.conf')
    run('sctl reload')


@task
def create_sso_user():
    env.box_domain = prompt('SSO Domain (leave empty to skip)', default='')
    if not env.box_domain:
        print(red('Cannot continue without a SSO Domain.'))
        return 1

    run('psql %(box_database_name)s -c "INSERT INTO auth_user VALUES'
        " (1, '', NOW(), TRUE, 'admin', '', '', '', TRUE, TRUE, NOW())\"")
    run('psql %(box_database_name)s -c "INSERT INTO admin_sso_assignment'
        " VALUES (1, 0, '', '%(box_domain)s', FALSE, 10, 1)\"")
