from __future__ import print_function, unicode_literals

from functools import wraps
import random
import re
import socket

from fabric.api import env, cd, local, run, task
from fabric.colors import red
from fabric.contrib.console import confirm


env.box_project_name = '{{ cookiecutter.project_name }}'
env.box_domain = '{{ cookiecutter.domain }}'
env.box_server = '{{ cookiecutter.server }}'
env.box_branch = 'master'

env.box_repository_name = re.sub(r'[^\w]+', '_', env.box_domain)
env.box_database_name = re.sub(r'[^\w]+', '_', env.box_domain)
env.box_sass = '%(box_project_name)s/static/%(box_project_name)s' % env
env.box_server_name = env.box_server.split('@')[-1]

env.forward_agent = True
env.hosts = [env.box_server]


def get_random_string(length, chars=None):
    """Returns a random string; mostly used to generate passwords and
    the contents of SECRET_KEY"""
    rand = random.SystemRandom()
    if chars is None:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(rand.choice(chars) for i in range(50))


def interpolate_with_env(fn):
    """Wrapper which extends a few Fabric API commands to fill in values from
    Fabric's environment dictionary"""
    @wraps(fn)
    def _dec(string, *args, **kwargs):
        return fn(string % env, *args, **kwargs)
    return _dec


local = interpolate_with_env(local)
cd = interpolate_with_env(cd)
run = interpolate_with_env(run)
confirm = interpolate_with_env(confirm)


@task
def check_services():
    """Checks whether required services (postgres and redis) are up and
    running, and fails if not"""
    success = True

    try:
        socket.create_connection(('localhost', 5432), timeout=0.1).close()
    except socket.error:
        print(red('postgres does not seem to be running!'))
        success = False

    try:
        socket.create_connection(('localhost', 6379), timeout=0.1).close()
    except socket.error:
        print(red('redis does not seem to be running!'))
        success = False

    if not success:
        raise Exception('Some required services are not available.')
