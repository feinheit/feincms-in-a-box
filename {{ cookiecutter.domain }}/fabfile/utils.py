from __future__ import unicode_literals

import random

from fabric.api import env, task

from fabfile.config import derive_env_from_domain


def get_random_string(length, chars=None):
    """Returns a random string; mostly used to generate passwords and
    the contents of SECRET_KEY"""
    rand = random.SystemRandom()
    if chars is None:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(rand.choice(chars) for i in range(50))


@task(alias='p')
def production():
    """Configures the environment for deploying or initializing production"""
    env.box_domain = env.box_domain_production
    env.box_env = 'production'
    derive_env_from_domain()


@task(alias='s')
def staging():
    """Configures the environment for deploying or initializing staging"""
    env.box_domain = env.box_domain_staging
    env.box_env = 'staging'
    derive_env_from_domain()
