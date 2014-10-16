from __future__ import unicode_literals

import re

from fabric.api import env


env.box_project_name = '{{ cookiecutter.project_name }}'

env.box_environments = {
    'production': {
        'shortcut': 'p',
        'domain': '{{ cookiecutter.domain }}',
        'branch': 'master',
        'server': 'www-data@feinheit04.nine.ch',
        'remote': 'production',
    },
    'staging': {
        'shortcut': 's',
        'domain': 'stage.{{ cookiecutter.domain }}',
        'branch': 'master',
        'server': 'www-data@feinheit04.nine.ch',
        'remote': 'staging',
    },
}

# Remove this for multi-env support
# env.box_hardwired_environment = 'production'


def derive_env_from_domain():
    env.update({
        'box_repository': re.sub(r'[^\w]+', '_', env.box_domain),
        'box_database': re.sub(r'[^\w]+', '_', env.box_domain),
        'box_database_local': re.sub(
            r'[^\w]+', '_', '{{ cookiecutter.domain }}'),
        'box_sass': '%(box_project_name)s/static/%(box_project_name)s' % env,
        'box_server_name': env.box_server.split('@')[-1],
        'forward_agent': True,
        'hosts': [env.box_server],
    })
