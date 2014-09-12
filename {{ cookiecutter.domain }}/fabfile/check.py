from __future__ import print_function, unicode_literals

from fabric.api import env, lcd, task

from fabfile.config import local


def _coding_style_check(base, project_name):
    with lcd(base):
        local("! git grep -n -C3 -E 'import i?pdb' -- '*.py'")
        local("! git grep -n -C3 -E 'console\.log' -- '*.html' '*.js'")
        local(
            "! git grep -n -C3 -E '(^| )print( |\(|$)'"
            " -- '%s/*py'" % project_name)
        local('flake8 .')


@task(default=True)
def check():
    _coding_style_check('.', env.box_project_name)
    # _coding_style_check('venv/src/???', '???')
    local('venv/bin/python manage.py check')


@task
def ready():
    """Check whether this project is ready for production"""
    local("! git grep -n -C3 -E '^Disallow: /$' -- 'robots.txt'")
    with lcd(env.box_project_name):
        local("! git grep -n -C3 -E 'meta.*robots.*noindex'")
        local("! git grep -n -C3 -E '(XXX|FIXME|TODO)'")
