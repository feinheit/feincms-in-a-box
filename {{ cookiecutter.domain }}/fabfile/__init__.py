from __future__ import unicode_literals

from os import chmod
from os.path import dirname, exists, join
from subprocess import Popen, PIPE

from fabfile import (
    check, config, dev, deploy, setup_local, setup_server, versioning)


__all__ = (
    'check',
    'config',
    'dev',
    'deploy',
    'setup_local',
    'setup_server',
    'versioning',
)


if config.env.box_staging_enabled:
    from fabfile.utils import production, staging
    __all__ += (
        'production',
        'staging',
    )
else:
    from fabfile.utils import production
    production()


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
