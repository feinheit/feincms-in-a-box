from __future__ import unicode_literals

from fabric.api import env


env.box_project_name = '${PROJECT_NAME}'
env.box_domain = '${DOMAIN}'
env.box_database_local = '${DOMAIN_SLUG}'
env.box_staticfiles = '%(box_project_name)s/static/%(box_project_name)s' % env
env.forward_agent = True

# Remove this for multi-env support
env.box_hardwired_environment = 'production'

env.box_environments = {
    'production': {
        'shortcut': 'p',
        'domain': '${DOMAIN}',
        'branch': 'master',
        'server': 'www-data@feinheit04.nine.ch',
        'remote': 'production',
        'repository': '${DOMAIN_SLUG}',
        'database': '${DOMAIN_SLUG}',
        'server_name': '${SERVER_NAME}',
    },
    'staging': {
        'shortcut': 's',
        'domain': 'stage.${DOMAIN}',
        'branch': 'develop',
        'server': 'www-data@feinheit04.nine.ch',
        'remote': 'staging',
        'repository': '${DOMAIN_SLUG}',
        'database': '${DOMAIN_SLUG}',
        'server_name': '${SERVER_NAME}',
    },
}
