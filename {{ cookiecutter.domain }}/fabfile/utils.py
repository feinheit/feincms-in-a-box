from __future__ import unicode_literals

import random


def get_random_string(length, chars=None):
    """Returns a random string; mostly used to generate passwords and
    the contents of SECRET_KEY"""
    rand = random.SystemRandom()
    if chars is None:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(rand.choice(chars) for i in range(50))
