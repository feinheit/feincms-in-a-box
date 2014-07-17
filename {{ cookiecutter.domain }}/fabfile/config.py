from functools import wraps
import random
import re

from fabric.api import (
    env,
    cd as cd_raw,
    local as local_raw,
    run as run_raw)


CONFIG = {
    'project_name': '{{ cookiecutter.project_name }}',
    'domain': '{{ cookiecutter.domain }}',
    'server': '{{ cookiecutter.server }}',
    'branch': 'master',
}

CONFIG.update({
    'repository_name': re.sub(r'[^\w]+', '_', CONFIG['domain']),
    'database_name': re.sub(r'[^\w]+', '_', CONFIG['domain']),
    'sass': '{project_name}/static/{project_name}'.format(**CONFIG),
    'server_name': CONFIG['server'].split('@')[-1],
})


env.forward_agent = True
env.hosts = [CONFIG['server']]


def get_random_string(length, chars=None):
    rand = random.SystemRandom()
    if chars is None:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(rand.choice(chars) for i in range(50))


def format_with_config(fn):
    @wraps(fn)
    def _dec(string, *args, **kwargs):
        return fn(string.format(**CONFIG), *args, **kwargs)
    return _dec


local = format_with_config(local_raw)
cd = format_with_config(cd_raw)
run = format_with_config(run_raw)
