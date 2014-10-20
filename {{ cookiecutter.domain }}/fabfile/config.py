from __future__ import unicode_literals

import re

from fabric.api import env


env.box_project_name = '{{ cookiecutter.project_name }}'
env.box_domain = '{{ cookiecutter.domain }}'
env.box_database_local = re.sub(r'[^\w]+', '_', env.box_domain)
env.box_sass = '%(box_project_name)s/static/%(box_project_name)s' % env
env.forward_agent = True

# Remove this for multi-env support
env.box_hardwired_environment = 'production'

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
        'branch': 'develop',
        'server': 'www-data@feinheit04.nine.ch',
        'remote': 'staging',
    },
}

for e in env.box_environments.values():
    e.update({
        'repository': re.sub(r'[^\w]+', '_', e['domain']),
        'database': re.sub(r'[^\w]+', '_', e['domain']),
        'server_name': e['server'].split('@')[-1],
    })
