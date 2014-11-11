from __future__ import unicode_literals

from multiprocessing import Process
import os
import subprocess

from fabric.api import env, hosts, task

from fabfile import local, require_services


@task(default=True)
@hosts('')
@require_services
def dev():
    """Runs the development server, SCSS watcher and backend services if they
    are not running already"""
    jobs = [
        lambda: local('venv/bin/python -Wall manage.py runserver'),
    ]

    if os.path.exists('gulpfile.js'):
        jobs.append(lambda: local('./node_modules/.bin/gulp'))
    elif os.path.exists('%(box_staticfiles)s/Gruntfile.js' % env):
        jobs.append(lambda: local('cd %(box_staticfiles)s && grunt'))
    elif os.path.exists('%(box_staticfiles)s/config.rb' % env):
        jobs.append(
            lambda: local('bundle exec compass watch %(box_staticfiles)s'))

    jobs = [Process(target=j) for j in jobs]
    [j.start() for j in jobs]
    [j.join() for j in jobs]


@task
@hosts('')
def makemessages():
    """Wrapper around the ``makemessages`` management command which excludes
    dependencies (virtualenv, bower components, node modules)"""
    local(
        'venv/bin/python manage.py makemessages -a'
        ' -i bower_components'
        ' -i node_modules'
        ' -i venv')


@task
@hosts('')
def kill():
    """Send SIGTERM to postgres and redis-server"""
    subprocess.call(
        "ps -ef | awk '/(postgres|redis)/ {print $2}' | xargs kill",
        shell=True)
