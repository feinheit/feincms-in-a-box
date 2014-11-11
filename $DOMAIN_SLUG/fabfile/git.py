from __future__ import unicode_literals

import getpass
import os

from fabric.api import env, hide, hosts, prompt, settings, task
from fabric.colors import red
from fabric.contrib.console import confirm
from fabric.utils import puts

from fabfile import run_local, require_env, step


@task
@hosts('')
def init_bitbucket():
    username = prompt('Username', default=os.environ.get('USER', ''))
    password = getpass.getpass('Password ')
    organization = prompt('Organization', default='feinheit')
    repository = prompt(
        'Repository',
        default=env.box_repository)

    if not confirm(
        'Initialize repository at https://bitbucket.org/%s/%s?' % (
            organization, repository)):

        puts(red('Bitbucket repository creation aborted.'))
        return 1

    if username and password and organization and repository:
        env.box_auth = '%s:%s' % (username, password)
        env.box_repo = '%s/%s' % (organization, repository)

        with hide('running'):
            run_local(
                'curl'
                ' -X POST -u %(box_auth)s -H "content-type: application/json"'
                ' https://api.bitbucket.org/2.0/repositories/%(box_repo)s'
                ' -d \'{"scm": "git", "is_private": true,'
                ' "forking_policy": "no_public_forks"}\'')

        with hide('everything'):
            with settings(warn_only=True):
                run_local('git remote rm origin')

        run_local('git remote add origin git@bitbucket.org:%(box_repo)s.git')
        run_local('git push -u origin master')


@task
@hosts('')
@require_env
def add_remote():
    with settings(warn_only=True):
        run_local(
            'git remote add -f %(box_remote)s %(box_server)s:%(box_domain)s/')


@task
@hosts('')
@require_env
def fetch_remote():
    step('Updating git remote...')
    with settings(warn_only=True):
        run_local('git fetch %(box_remote)s')
