from __future__ import unicode_literals

import re

from fabric.api import env


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
