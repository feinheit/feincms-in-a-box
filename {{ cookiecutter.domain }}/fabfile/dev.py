from __future__ import unicode_literals

from multiprocessing import Process
import os
import socket

from fabric.api import env, hosts, task

from fabfile import local


def _service_processes():
    jobs = []
    try:
        socket.create_connection(('localhost', 5432), timeout=0.1).close()
    except socket.error:
        jobs.append(lambda: local('postgres'))
    try:
        socket.create_connection(('localhost', 6379), timeout=0.1).close()
    except socket.error:
        jobs.append(lambda: local('redis-server'))
    return jobs


@task(default=True)
@hosts('')
def dev():
    """Runs the development server, SCSS watcher and backend services if they
    are not running already"""
    jobs = [
        lambda: local('venv/bin/python -Wall manage.py runserver'),
    ]

    if os.path.exists('%(box_sass)s/bower.json' % env):
        jobs.append(lambda: local('cd %(box_sass)s && grunt'))
    elif os.path.exists('%(box_sass)s/config.rb' % env):
        jobs.append(lambda: local('bundle exec compass watch %(box_sass)s'))

    jobs.extend(_service_processes())
    jobs = [Process(target=j) for j in jobs]
    [j.start() for j in jobs]
    [j.join() for j in jobs]


@task
@hosts('')
def services():
    """Runs the backend services if they are not running already"""
    jobs = _service_processes()
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
