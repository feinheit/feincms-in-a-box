from __future__ import unicode_literals

import re

from fabric.api import (
    env, execute, hide, hosts, run, runs_once, settings, task)
from fabric.colors import red
from fabric.utils import abort, puts

from fabfile import cd, local, require_env, step


def complain_on_failure(task, complaint):
    if not task.succeeded:
        puts(red(complaint))


@task(default=True)
@hosts('')
@runs_once
def check():
    """Runs coding style checks, and Django's checking framework"""
    step('Searching for debugging statements...')
    local("! git grep -n -C3 -E 'import i?pdb' -- '*.py'")
    local("! git grep -n -C3 -E 'console\.log' -- '*.html' '*.js'")
    local(
        "! git grep -n -C3 -E '(^| )print( |\(|$)'"
        " -- '%(box_project_name)s/*py'")

    step('Checking Python code with flake8...')
    local('flake8 .')

    step('Checking frontend code...')
    local('./node_modules/.bin/gulp check')

    step('Invoking Django\'s systems check framework...')
    local('venv/bin/python manage.py check')

    with settings(warn_only=True), hide('warnings'):
        # Remind the user about uglyness, but do not fail (there are good
        # reasons to use the patterns warned about here).
        step('Pointing to potential tasks...')
        local("! git grep -n -E '#.*noqa' -- '%(box_project_name)s/*.py'")
        local("! git grep -n -E '(XXX|FIXME|TODO)'")
        complain_on_failure(
            local("! git grep -n -E '^-e[^@]*$' -- requirements/"),
            'Warning: Editable and unpinned requirements found!')


@task
@runs_once
@require_env
def primetime():
    """Check whether this project is ready for prime time"""
    execute('check.check')

    step('"noindex" should not hit production servers...')
    local(
        "! git grep -n -C3 -E '^Disallow: /$' -- 'robots.txt'")
    local(
        "! git grep -n -C3 -E 'meta.*robots.*noindex' -- %(box_project_name)s")

    step('Checking local settings on server...')
    with cd('%(box_domain)s'):
        output = run(
            "DJANGO_SETTINGS_MODULE=%(box_project_name)s.settings"
            " venv/bin/python -c \""
            "from django.conf import settings as s;"
            "print('fd:%%s\\ndsn:%%s\\nsso:%%s\\ndebug:%%s\\nsk:%%s' %% ("
            "getattr(s, 'FORCE_DOMAIN', '-'),"
            "getattr(s, 'RAVEN_CONFIG', {}).get('dsn', ''),"
            "bool(getattr(s, 'DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON', False)),"
            "bool(s.DEBUG),"
            "s.SECRET_KEY,"
            "))\"" % env, quiet=True).strip()

        output = dict(
            row.strip().split(':', 1) for row in re.split(r'[\r\n]+', output))

        if output['fd'] == '':
            puts(red('Warning: FORCE_DOMAIN is empty.'))
        elif output['fd'] == '-':
            puts(red('Warning: FORCE_DOMAIN is not defined.'))

        if output['dsn'] == '':
            puts(red(
                'Warning: Sentry is not configured, fill in RAVEN_CONFIG.'))

        if output['sso'] != 'True':
            puts(red(
                'Warning: SSO authentication for the administration is not'
                ' configured.'))

        if output['debug'] == 'True':
            puts(red(
                'Error: DEBUG = True!?', bold=True))

        with settings(warn_only=True), hide('everything'):
            gitgrep = local("! git grep '%s'" % output['sk'], capture=True)
            grep = local("! grep '%s' */*.py" % output['sk'], capture=True)
        if gitgrep or grep:
            puts(red(
                'Error: The remote value of SECRET_KEY also exists in local'
                ' files. Set a new value for SECRET_KEY in'
                ' %(box_project_name)s/local_settings.py on the server!'
                % env, bold=True))


@task
@runs_once
@require_env
def deploy():
    """Checks whether everything is ready for deployment"""

    execute('check.check')
    execute('check.test')
    # XXX Maybe even execute('check.primetime') if deploying to production?

    with cd('%(box_domain)s'):
        step('\nChecking for uncommitted changes on the server...')
        result = run('git status --porcelain')
        if result:
            abort(red('Uncommitted changes detected, aborting deployment.'))


@task
@hosts('')
def test():
    execute('check.test_backend')
    execute('check.test_frontend')


@task
@hosts('')
def test_backend():
    step('Running backend testsuite...')
    local('venv/bin/python manage.py test')


@task
@hosts('')
def test_frontend():
    step('Running frontend testsuite...')
    # local('./node_modules/.bin/gulp test')
