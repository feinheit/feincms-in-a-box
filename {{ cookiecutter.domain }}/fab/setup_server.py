from __future__ import print_function, unicode_literals

from io import StringIO

from fabric.api import execute, hide, prompt, put, settings, task
from fabric.colors import green, red

from fab.config import CONFIG, local, cd, run, get_random_string


@task(default=True)
def init():
    execute('setup_server.clone_repository')
    execute('setup_server.create_virtualenv')
    execute('setup_server.create_database_and_local_settings')
    execute('setup_server.nginx_vhost_and_supervisor')
    execute('deploy.styles')
    execute('setup_server.create_sso_user')
    print(green('Visit http://{domain}.{server_name} now!'.format(**CONFIG)))


@task
def clone_repository():
    print(green('We need the repository to initialize the server.'))
    with hide('running'):
        output = local('git config remote.origin.url', capture=True)
    repo = prompt('Repository', default=output)

    if not repo:
        print(red('Cannot continue without a repository.'))
        return 1

    CONFIG['repository_url'] = repo

    run('git clone {repository_url} {domain}')
    execute('versioning.add_live_remote')


@task
def create_virtualenv():
    with cd('{domain}'):
        run('virtualenv --python python2.7 --prompt "(venv:{domain})" venv')
        run('venv/bin/pip install -U virtualenv pip wheel'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')
        run('venv/bin/pip install -U setuptools'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')
        run('venv/bin/pip install -r requirements/live.txt'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')


@task
def create_database_and_local_settings():
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
def nginx_vhost_and_supervisor():
    run('sudo nine-manage-vhosts virtual-host create {domain}'
        ' --template=feinheit --relative-path=htdocs')

    with cd('{domain}'):
        run('mkdir media tmp')

    run('supervisor-create-conf {domain} wsgi'
        ' > supervisor/conf.d/{domain}.conf')
    run('sctl reload')


@task
def create_sso_user():
    domain = prompt('SSO Domain (leave empty to skip)', default='')
    if not domain:
        print(red('Cannot continue without a SSO Domain.'))
        return 1

    run('psql {database_name} -c "INSERT INTO auth_user VALUES'
        " (1, '', NOW(), TRUE, 'admin', '', '', '', TRUE, TRUE, NOW())\"")
    run('psql {database_name} -c "INSERT INTO admin_sso_assignment VALUES'
        " (1, 0, '', '%s', FALSE, 10, 1)\"" % domain)
