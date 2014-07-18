from functools import wraps
import random
import re

from fabric.api import env, cd, local, run


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
    rand = random.SystemRandom()
    if chars is None:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(rand.choice(chars) for i in range(50))


def interpolate_with_env(fn):
    @wraps(fn)
    def _dec(string, *args, **kwargs):
        return fn(string % env, *args, **kwargs)
    return _dec


local = interpolate_with_env(local)
cd = interpolate_with_env(cd)
run = interpolate_with_env(run)
