from __future__ import print_function, unicode_literals

import socket
from threading import Thread

from fabric.api import task

from fab.config import local


@task(default=True)
def dev():
    jobs = [Thread(target=fn) for fn in [
        lambda: local('cd {sass} && grunt'),
        lambda: local('venv/bin/python -Wall manage.py runserver'),
    ]]
    try:
        socket.create_connection(('localhost', 5432), timeout=0.1).close()
    except socket.error:
        jobs.append(Thread(target=lambda: local('postgres')))
    try:
        socket.create_connection(('localhost', 6379), timeout=0.1).close()
    except socket.error:
        jobs.append(Thread(target=lambda: local('redis-server')))
    [j.start() for j in jobs]
    [j.join() for j in jobs]
