#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals

import argparse
import env
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


def read_output(command, fail_silently=False):
    """
    Runs the command and returns the output
    """
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError:
        if fail_silently:
            return ''
        raise

    output = output.decode(sys.stdin.encoding)
    return output.strip()


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
        shutil.copymode(from_, to_)


def walker(base, base_dir, context):
    """
    Walks over all files in ``base`` while substituting the contents of
    ``context`` inside paths and file contents. Skips over anything which
    matches a line inside ``.gitignore``.
    """
    with io.open('.gitignore', 'r', encoding='utf-8') as gitignore:
        gitignore_patterns = [
            line for line in gitignore.read().splitlines() if line]

    print(color(
        'Generating the project inside %s.' % base_dir,
        'cyan', True))

    for dirpath, dirnames, filenames in os.walk(base):
        dir = os.path.join(
            base_dir,
            # Cut away "fbox/" when generating the target path.
            Template(dirpath[5:]).safe_substitute(context),
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

    os.chdir(base_dir)
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'add', '-A'])
    subprocess.call([
        'git', 'commit', '-q',
        '--author', 'FeinCMS-in-a-Box <box@feincms.org>',
        '-m', 'Initial commit'])

    print(color(
        'Successfully initialized the project in %s.' % base_dir,
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

    default_env = os.path.join(
        os.path.expanduser('~'),
        '.box.env',
    )
    if os.path.isfile(default_env):
        env.read_dotenv(default_env)

    class validate(object):
        @staticmethod
        def domain(string):
            if not re.match(r'^([-\w]+\.)+\w{2,}$', string):
                raise argparse.ArgumentTypeError(
                    '\'%s\' is not a valid domain' % string)
            return string

        @staticmethod
        def nice_name(string):
            if not re.match(r'^[-\.\w\s]+$', string):
                raise argparse.ArgumentTypeError(
                    'Please do not use any special chars for nice_name')
            return string

        @staticmethod
        def project_name(string):
            if not re.match(r'^\w{3,}$', string):
                raise argparse.ArgumentTypeError(
                    '\'%s\' does not look like a valid Python module name'
                    % string)
            return string

        @staticmethod
        def server(string):
            if not re.match(r'^[-\w]+@([-\w]+\.)+\w{2,}$', string):
                raise argparse.ArgumentTypeError(
                    'Please provide a server login of the form'
                    ' \'user@server.example.tld\'')
            return string

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'domain',
        type=validate.domain,
        help='Domain name')
    parser.add_argument(
        'nice_name',
        type=validate.nice_name,
        help='Nice name')
    parser.add_argument(
        '-p', '--project-name',
        type=validate.project_name,
        help='Python module for the project [%(default)s]',
        default='box')
    parser.add_argument(
        '-s', '--server',
        type=validate.server,
        help='Server [%(default)s]',
        default=env.env('SERVER'))
    parser.add_argument(
        '-d', '--destination',
        type=str,
        help='The destination path for the project [./build/$DOMAIN_SLUG]')
    parser.add_argument(
        '--charge',
        action='store_true',
        help='Charge ahead, do not ask for confirmation')
    args = parser.parse_args()

    if not args.server:
        print(color(
            'Either specify a server using --server or add a default value'
            ' for SERVER in ~/.box.env', 'red', True))
        sys.exit(1)

    if not args.destination:
        args.destination = os.path.join(
            os.path.dirname(__file__),
            'build',
            re.sub(r'[^\w]+', '_', args.domain),
        )
    args.destination = os.path.abspath(args.destination)

    if os.path.exists(args.destination):
        print(color(
            'Destination \'%s\' already exists, cannot continue.'
            % args.destination,
            'red', True))
        sys.exit(1)

    context = {
        'DESTINATION': args.destination,
        'DOMAIN': args.domain,
        'DOMAIN_SLUG': re.sub(r'[^\w]+', '_', args.domain),
        'NICE_NAME': args.nice_name,
        'PROJECT_NAME': args.project_name,
        'SERVER': args.server,
        'SERVER_NAME': args.server.split('@')[-1],
        'USER_NAME': read_output(
            ['git', 'config', 'user.name'],
            fail_silently=True),
        'USER_EMAIL': read_output(
            ['git', 'config', 'user.email'],
            fail_silently=True),
    }

    if not args.charge:
        print(color('Do those settings look correct?', 'cyan', True))
        print('\n'.join(
            '%s: %s' % row for row in sorted(context.items())
        ).encode(sys.stdout.encoding))
        print(color('If not, abort using Ctrl-C now.', 'cyan', True))
        raw_input()

    walker('fbox', args.destination, context)
