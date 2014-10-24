#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals

from fnmatch import fnmatch
import io
import os
import re
import shutil
from string import Template
import subprocess

try:
    raw_input
except NameError:
    raw_input = input


DEFAULT_CONTEXT = [
    ('NICE_NAME', 'This isn\'t a nice name'),
    ('DOMAIN', 'test.406.ch'),
    ('PROJECT_NAME', 'box'),
    ('SERVER', 'www-data@feinheit04.nine.ch'),
]


def readline(prompt, default=None, required=True):
    if default:
        prompt += ' [%s]' % default
    prompt += ': '

    while True:
        value = raw_input(prompt)
        if not required:
            return value or default
        elif value:
            return value
        elif default:
            return default


def ask_for_context():
    context = dict((
        key,
        readline(key, default=default)) for key, default in DEFAULT_CONTEXT)

    context.update({
        'NICE_NAME': context['NICE_NAME'].replace('\'', '\\\''),
        'DOMAIN_SLUG': re.sub(r'[^\w]+', '_', context['DOMAIN']),
        'SERVER_NAME': context['SERVER'].split('@')[-1],
    })
    return context


class FilterIgnored(object):
    def __init__(self, patterns):
        self.patterns = patterns

    def __call__(self, iterable):
        for item in iterable:
            if any(fnmatch(item, pattern) for pattern in self.patterns):
                continue
            yield item


def copy_file_to(from_, to_, context):
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
    with io.open('.gitignore', 'r', encoding='utf-8') as gitignore:
        filter_ignored = FilterIgnored(
            [line for line in gitignore.read().splitlines() if line])

    base_dir = os.path.join(
        os.path.dirname(__file__),
        'build',
    )
    project_dir = os.path.join(
        base_dir,
        context['DOMAIN'],
    )

    if os.path.exists(project_dir):
        print(
            'Project directory %s exists already, cannot continue.'
            % project_dir)
        return

    for dirpath, dirnames, filenames in os.walk(base):
        dir = os.path.join(
            base_dir,
            Template(dirpath).safe_substitute(context),
        )
        os.makedirs(dir)
        for filename in filter_ignored(filenames):
            copy_file_to(
                os.path.join(dirpath, filename),
                os.path.join(dir, filename),
                context,
            )

    os.chdir(project_dir)
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'add', '-A'])
    subprocess.call(['git', 'commit', '-m', 'Initial commit'])


if __name__ == '__main__':
    context = ask_for_context()
    from pprint import pprint
    pprint(context)
    walker('$DOMAIN', context)
