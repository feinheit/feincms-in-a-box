from __future__ import print_function, unicode_literals

import getpass
import os

from fabric.api import hide, prompt, settings, task
from fabric.colors import red
from fabric.contrib.console import confirm

from fabfile.config import CONFIG, local, local_raw


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
def add_live_remote():
    with settings(warn_only=True):
        local('git remote add -f live {server}:{domain}/')
