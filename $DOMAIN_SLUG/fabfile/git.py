from __future__ import unicode_literals

import getpass
import os

from fabric.api import env, hide, hosts, prompt, settings, task
from fabric.colors import red
from fabric.contrib.console import confirm
from fabric.utils import puts

from fabfile import run_local, require_env, step

import env as dotenv


@task
@hosts('')
def init_bitbucket():
    default_env = os.path.join(
        os.path.expanduser('~'),
        '.box.env',
    )
    if os.path.isfile(default_env):
        dotenv.read_dotenv(default_env)
    else:
        print(
            'Consider creating a ~/.box.env file containing values for'
            ' BITBUCKET_USERNAME and BITBUCKET_ORGANIZATION if you want'
            ' different defaults.')

    username = prompt(
        'Username',
        default=dotenv.env('BITBUCKET_USERNAME'))
    password = getpass.getpass('Password ')
    organization = prompt(
        'Organization',
        default=dotenv.env('BITBUCKET_ORGANIZATION'))
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
                ' -X POST -v -u %(box_auth)s'
                ' -H "content-type: application/json"'
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
