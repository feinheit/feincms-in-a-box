from __future__ import unicode_literals

import socket

from fabric.api import env, execute, hide, lcd, settings, task
from fabric.colors import cyan, red
from fabric.utils import puts

from fabfile.config import local


def _step(str):
    puts(cyan('\n%s' % str, bold=True))


def _coding_style_check(base, project_name):
    """Checks whether there are disallowed debugging statements, and whether
    static checking tools (currently only flake8) report any problems with
    a given project."""
    with lcd(base):
        _step('Searching "%s" for debugging statements...' % base)
        local("! git grep -n -C3 -E 'import i?pdb' -- '*.py'")
        local("! git grep -n -C3 -E 'console\.log' -- '*.html' '*.js'")
        local(
            "! git grep -n -C3 -E '(^| )print( |\(|$)'"
            " -- '%s/*py'" % project_name)

        _step('Checking Python code with flake8...')
        local('flake8 .')

        _step('Checking JavaScript code with JSHint...')
        local(
            "jshint $(git ls-files '*.js' | grep -vE '(%s)')"
            % env.box_check['exclude_from_jshint'])

        with settings(warn_only=True), hide('warnings'):
            # Remind the user about uglyness, but do not fail (there are good
            # reasons to use the patterns warned about here).
            _step('Pointing to potential tasks...')
            local("! git grep -n -E '#.*noqa' -- '%s/*.py'" % project_name)
            local("! git grep -n -E '(XXX|FIXME|TODO)'")


@task(default=True)
def check():
    """Runs coding style checks, and Django's checking framework"""
    if env.get('box_check_success'):
        _step('Second invocation of check, skipping...')
        return

    for base, project_name in env.box_check['coding_style']:
        _coding_style_check(base, project_name)

    _step('Invoking Django\'s systems check framework...')
    local('venv/bin/python manage.py check')

    env.box_check_success = True


@task
def ready():
    """Check whether this project is ready for production"""
    execute('check.check')

    _step('"noindex" should not hit production servers...')
    local(
        "! git grep -n -C3 -E '^Disallow: /$' -- 'robots.txt'")
    local(
        "! git grep -n -C3 -E 'meta.*robots.*noindex' -- %(box_project_name)s")


@task
def services():
    """Checks whether required services (postgres and redis) are up and
    running, and fails if not"""
    success = True

    try:
        socket.create_connection(('localhost', 5432), timeout=0.1).close()
    except socket.error:
        puts(red('postgres does not seem to be running!'))
        success = False

    try:
        socket.create_connection(('localhost', 6379), timeout=0.1).close()
    except socket.error:
        puts(red('redis does not seem to be running!'))
        success = False

    if not success:
        raise Exception('Some required services are not available.')
