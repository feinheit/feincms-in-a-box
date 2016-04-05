"""
This file contains the configuration for the fabric scripts.
The scripts support multiple environments.

Within the fabric commands string formatting is applied with the env object
as argument.

The environment specific values are available as box_<key>
e.g. '%(box_branch)s'.

Usage::
    run('git clone -b %(box_branch)s %(box_repository_url)s %(box_domain)s')
"""

from __future__ import unicode_literals

from fabric.api import env

# env.box_environment contains the currently active environment.

# Default values available in all environments
env.box_project_name = '${PROJECT_NAME}'
env.box_domain = '${DOMAIN}'
env.box_database_local = '${DOMAIN_SLUG}'
env.box_staticfiles = '%(box_project_name)s/static/%(box_project_name)s' % env
env.box_static_src = 'assets'
env.box_python = '${PYTHON}'
env.forward_agent = True

# Remove this for multi-env support
env.box_hardwired_environment = 'production'

# Environment specific values.
env.box_environments = {
    'production': {
        'shortcut': 'p',
        'domain': '${DOMAIN}',
        'branch': 'master',
        'servers': [
            '${SERVER}',
        ],
        'remote': 'production',  # git remote alias for the server.
        'repository': '${DOMAIN_SLUG}',
        'database': '${DOMAIN_SLUG}',
    },
    'staging': {
        'shortcut': 's',
        'domain': 'stage.${DOMAIN}',
        'branch': 'develop',
        'servers': [
            '${SERVER}',
        ],
        'remote': 'staging',
        'repository': '${DOMAIN_SLUG}',
        'database': 'stage_${DOMAIN_SLUG}',
    },
}
