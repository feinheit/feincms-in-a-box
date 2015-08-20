from __future__ import unicode_literals

import re

from fabric.api import (
    env, execute, hide, hosts, run, runs_once, settings, task)
from fabric.colors import red
from fabric.utils import abort, puts

from fabfile import cd, confirm, run_local, require_env, require_services, step


def complain_on_failure(task, complaint):
    if not task.succeeded:
        puts(red(complaint))


@task(default=True)
@hosts('')
@runs_once
def check():
    """Runs coding style checks, and Django's checking framework"""
    step('Searching for debugging statements...')
    run_local(
        "! git --no-pager grep -n -C3 -E 'import i?pdb' -- '*.py'")
    run_local(
        "! git --no-pager grep -n -C3 -E 'console\.log' -- '*.html' '*.js'")
    run_local(
        "! git --no-pager grep -n -C3 -E '(^| )print( |\(|$)' -- '*.py'")

    step('Checking Python code with flake8...')
    run_local('venv/bin/flake8 .')

    step('Checking Javascript code...')
    run_local('./node_modules/.bin/jshint %(box_staticfiles)s/')

    step('Invoking Django\'s systems check framework...')
    run_local('venv/bin/python manage.py check')

    with settings(warn_only=True), hide('warnings'):
        # Remind the user about uglyness, but do not fail (there are good
        # reasons to use the patterns warned about here).
        step('Pointing to potential tasks...')
        run_local(
            "! git --no-pager grep -n -E '#.*noqa'"
            " -- '%(box_project_name)s/*.py'")
        run_local("! git --no-pager grep -n -E '(XXX|FIXME|TODO)'")
        complain_on_failure(
            run_local("! git --no-pager grep -n -E '^-e.+$' -- requirements/"),
            'Warning: Editable requirements found. Releases are preferred!')


@task
@runs_once
@require_env
def primetime():
    """Check whether this project is ready for prime time"""
    execute('check.check')
    execute('check.test')

    step('"noindex" should not hit production servers...')
    run_local(
        "! git --no-pager grep -n -C3 -E '^Disallow: /$' -- 'robots.txt'")
    run_local(
        "! git --no-pager grep -n -C3 -E 'meta.*robots.*noindex'"
        " -- %(box_project_name)s")

    step('Checking local settings on server...')
    # TODO:  check if OnlyStaffMiddleware is disabled
    with cd('%(box_domain)s'):
        output = run(
            "DJANGO_SETTINGS_MODULE=%(box_project_name)s.settings.production"
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
            gitgrep = run_local(
                "! git --no-pager grep '%s'" % output['sk'], capture=True)
            grep = run_local("! grep '%s' */*.py" % output['sk'], capture=True)
        if gitgrep or grep:
            puts(red(
                'Error: The remote value of SECRET_KEY also exists in local'
                ' files. Set a new value for SECRET_KEY in'
                ' .env on the server!'
                % env, bold=True))


@task
@runs_once
@require_env
def deploy():
    """Checks whether everything is ready for deployment"""

    step('Checking whether we are on the expected branch...')
    with settings(warn_only=True), hide('everything'):
        branch = run_local('git symbolic-ref -q --short HEAD', capture=True)

    if not branch:
        abort(red('No branch checked out, cannot continue.', bold=True))

    if branch != env.box_branch:
        puts(red(
            'Warning: The currently checked out branch is \'%s\', but'
            ' the environment \'%s\' runs on \'%s\'.' % (
                branch, env.box_environment, env.box_branch)))

        if not confirm('Continue deployment?', default=False):
            abort('Aborting.')

    execute('check.check')
    execute('check.test')
    # XXX Maybe even execute('check.primetime') if deploying to production?

    with cd('%(box_domain)s'):
        step('\nChecking for uncommitted changes on the server...')
        result = run('git status --porcelain')
        if result:
            abort(red('Uncommitted changes detected, aborting deployment.'))


@task
@runs_once
@hosts('')
@require_services
def test():
    step('Running backend testsuite...')
    run_local('venv/bin/python manage.py test')
    step('We do not have a frontend testsuite yet...')
    # run_local('./node_modules/.bin/gulp test')
