from __future__ import unicode_literals

from functools import wraps
from os import chmod
from os.path import dirname, exists, join
from subprocess import Popen, PIPE

from fabric.api import env, cd, local, run, task
from fabric.contrib.console import confirm

from fabfile import config


__all__ = (
    'check',
    'config',
    'dev',
    'deploy',
    'setup_local',
    'setup_server',
    'versioning',
)


# Production vs staging -----------------------------------------------------

def _create_setup_task_for_env(environment):
    def _setup():
        for key, value in env.box_environments[environment].items():
            env['box_%s' % key] = value
        config.derive_env_from_domain()
    return _setup


if env.box_staging_enabled:
    # Create a task for all environments, and use the first character as alias
    g = globals()
    for environment in env.box_environments:
        g[environment] = task(alias=environment[0])(
            _create_setup_task_for_env(environment))
        __all__ += (environment,)

else:
    _create_setup_task_for_env('production')()


# Fabric commands with environment interpolation ----------------------------
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


# Git pre-commit hook which always runs "fab check" -------------------------
def ensure_pre_commit_hook_installed():
    """
    Ensures that ``git commit`` fails if ``fab check`` returns any errors.
    """
    p = Popen('git rev-parse --git-dir'.split(), stdout=PIPE)
    git_dir = p.stdout.read().strip()
    project_dir = dirname(git_dir)

    if not any(exists(join(project_dir, name)) for name in (
            'fabfile.py', 'fabfile')):
        # Does not look like a Django project.
        # Additionally, "fab check" wouldn't work anyway.
        return

    pre_commit_hook_path = join(git_dir, 'hooks', 'pre-commit')
    if not exists(pre_commit_hook_path):
        with open(pre_commit_hook_path, 'w') as hook:
            hook.write('''\
#!/bin/sh
fab check
''')
        chmod(pre_commit_hook_path, 0o755)


# Run this each time the fabfile is loaded
ensure_pre_commit_hook_installed()


# Import other fabfile mods, now that interpolate_with_env has been run -----
from fabfile import (
    check, dev, deploy, setup_local, setup_server, versioning)
