#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals

from fnmatch import fnmatch
import io
import os
import re
import shutil
from string import Template
import subprocess
import sys

try:
    raw_input
except NameError:
    raw_input = input


def readline(prompt, default=None, required=True):
    """
    Prompts the user for the value described in ``prompt``.

    If ``required`` is set to ``True`` ensures that a non-empty value is
    returned (which might also be the default value if the default was
    non-empty).
    """
    if default:
        prompt += ' [%s]' % default
    prompt += ': '

    while True:
        value = raw_input(prompt.encode(sys.stdout.encoding))
        if not required:
            return value or default
        elif value:
            return value
        elif default:
            return default

        print(color('This value is required.', 'red'))


def read_output(command):
    output = subprocess.check_output(command)
    return output.decode(sys.stdin.encoding).strip()


def ask_for_context():
    """
    Ask nicely for a few details regarding the project we are about to
    generate.
    """
    default_context = [
        ('NICE_NAME', ''),
        ('DOMAIN', ''),
        ('PROJECT_NAME', 'box'),
        ('SERVER', 'www-data@feinheit04.nine.ch'),
        ('USER_NAME', read_output(['git', 'config', 'user.name'])),
        ('USER_EMAIL', read_output(['git', 'config', 'user.email'])),
    ]

    context = dict((
        key,
        readline(key, default=default)) for key, default in default_context)

    context.update({
        'NICE_NAME': context['NICE_NAME'].replace('\'', '\\\''),
        'DOMAIN_SLUG': re.sub(r'[^\w]+', '_', context['DOMAIN']),
        'SERVER_NAME': context['SERVER'].split('@')[-1],
    })
    return context


def copy_file_to(from_, to_, context):
    """
    Copies the file at path ``from_`` to the path ``to_``, while also
    substituting variables in the context if the contents of the file can be
    decoded as UTF-8. Otherwise, simply copies the file (which is what we want
    for example for binary files).
    """
    try:
        with io.open(from_, 'r', encoding='utf-8') as handle:
            contents = handle.read()

    except ValueError:  # Unicode and stuff, handle as binary
        shutil.copy(from_, to_)

    else:
        contents = Template(contents).safe_substitute(context)
        with io.open(to_, 'w+', encoding='utf-8') as handle:
            handle.write(contents)


def walker(base, context):
    """
    Walks over all files in ``base`` while substituting the contents of
    ``context`` inside paths and file contents. Skips over anything which
    matches a line inside ``.gitignore``.
    """
    with io.open('.gitignore', 'r', encoding='utf-8') as gitignore:
        gitignore_patterns = [
            line for line in gitignore.read().splitlines() if line]

    base_dir = os.path.join(
        os.path.dirname(__file__),
        'build',
    )
    project_dir = os.path.join(
        base_dir,
        context['DOMAIN_SLUG'],
    )

    if os.path.exists(project_dir):
        print(color(
            'Project directory %s exists already, cannot continue.'
            % project_dir,
            'red', True))
        return

    print(color(
        'Generating the project inside %s.' % project_dir,
        'cyan', True))

    for dirpath, dirnames, filenames in os.walk(base):
        dir = os.path.join(
            base_dir,
            Template(dirpath).safe_substitute(context),
        )
        os.makedirs(dir)
        for fn in filenames:
            if any(fnmatch(fn, pattern) for pattern in gitignore_patterns):
                continue

            copy_file_to(
                os.path.join(dirpath, fn),
                os.path.join(dir, fn),
                context,
            )

    os.chdir(project_dir)
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'add', '-A'])
    subprocess.call(['git', 'commit', '-q', '-m', 'Initial commit'])

    print(color(
        'Successfully initialized the project in %s.' % project_dir,
        'cyan', True))
    print(color(
        'Run "fab local.setup" inside the project folder to continue.',
        'green', True))


def color(str, color=None, bold=False):
    color = {
        'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'magenta': 35,
        'cyan': 36, 'white': 37,
    }.get(color)
    if color:
        return '\033[%s%sm%s\033[0m' % ('1;' if bold else '', color, str)
    return str


if __name__ == '__main__':
    print(color('Welcome to FeinCMS-in-a-Box', 'cyan', True))
    print(color('===========================', 'cyan', True))

    context = ask_for_context()
    walker('$DOMAIN_SLUG', context)
