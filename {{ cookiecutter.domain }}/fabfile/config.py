from __future__ import unicode_literals

from functools import wraps
import re

from fabric.api import env, cd, local, run
from fabric.contrib.console import confirm


env.box_staging_enabled = False
env.box_project_name = '{{ cookiecutter.project_name }}'
env.box_domain_production = '{{ cookiecutter.domain }}'
env.box_domain_staging = 'stage.{{ cookiecutter.domain }}'
env.box_server = '{{ cookiecutter.server }}'
env.box_branch = 'master'

env.box_check = {
    'coding_style': [
        ('.', env.box_project_name),
        # ('venv/src/???', '???'),
    ],
    'exclude_from_jshint': 'ckeditor/|lightbox',
}


def derive_env_from_domain():
    env.box_repository_name = re.sub(r'[^\w]+', '_', env.box_domain)
    env.box_database_name = re.sub(r'[^\w]+', '_', env.box_domain)
    env.box_sass = '%(box_project_name)s/static/%(box_project_name)s' % env
    env.box_server_name = env.box_server.split('@')[-1]

    env.forward_agent = True
    env.hosts = [env.box_server]


if not env.box_staging_enabled:
    env.box_domain = env.box_domain_production
    env.box_env = 'production'
    derive_env_from_domain()


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
