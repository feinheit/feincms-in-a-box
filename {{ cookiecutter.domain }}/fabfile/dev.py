from __future__ import print_function, unicode_literals

from multiprocessing import Process
import socket

from fabric.api import task

from fabfile.config import local


@task(default=True)
def dev():
    jobs = [Process(target=fn) for fn in [
        lambda: local('cd %(box_sass)s && grunt'),
        lambda: local('venv/bin/python -Wall manage.py runserver'),
    ]]
    try:
        socket.create_connection(('localhost', 5432), timeout=0.1).close()
    except socket.error:
        jobs.append(Process(target=lambda: local('postgres')))
    try:
        socket.create_connection(('localhost', 6379), timeout=0.1).close()
    except socket.error:
        jobs.append(Process(target=lambda: local('redis-server')))
    [j.start() for j in jobs]
    [j.join() for j in jobs]


@task
def makemessages():
    local(
        'venv/bin/python manage.py makemessages -a'
        ' -i bower_components'
        ' -i node_modules'
        ' -i venv')
