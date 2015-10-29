from __future__ import unicode_literals

from multiprocessing import Process
import os
import subprocess

from fabric.api import env, hosts, task

from fabfile import run_local, require_services


@task(default=True)
@hosts('')
@require_services
def dev():
    """Runs the development server, SCSS watcher and backend services if they
    are not running already"""
    jobs = [
        lambda: run_local('venv/bin/python -Wall manage.py runserver'),
    ]
    if os.path.exists('gulpfile.js'):
        jobs.append(lambda: run_local('./node_modules/.bin/gulp'))
    elif os.path.exists('%(box_staticfiles)s/Gruntfile.js' % env):
        jobs.append(lambda: run_local('cd %(box_sass)s && grunt'))
    elif os.path.exists('%(box_staticfiles)s/config.rb' % env):
        jobs.append(
            lambda: run_local('bundle exec compass watch %(box_staticfiles)s'))
    elif os.path.exists('%(box_staticfiles)s/webpack.config.js' % env):
        jobs.append(
            lambda: run_local(
                './node_modules/.bin/webpack -d --watch'
                ' --config %(box_staticfiles)s/webpack.config.js'))

    jobs = [Process(target=j) for j in jobs]
    [j.start() for j in jobs]
    [j.join() for j in jobs]


@task
@hosts('')
def makemessages():
    """Wrapper around the ``makemessages`` management command which excludes
    dependencies (virtualenv, bower components, node modules)"""
    run_local(
        'venv/bin/python manage.py makemessages -a'
        ' -i bower_components'
        ' -i node_modules'
        ' -i venv')

    # uncomment this for Javascript i18n (requires django-statici18n)
    # run_local('venv/bin/python manage.py makemessages -d djangojs -a '
    #       '-e js -v 2 '
    #       '-i venv '
    #       ' -i bower_components'
    #       '-i node_modules'
    #       ' -i app/static/jsi18n')
    # run_local('venv/bin/python manage.py compilemessages')
    # run_local('venv/bin/python manage.py compilejsi18n')


@task
@hosts('')
@require_services
def services():
    """Starts all required background services"""
    pass


@task
@hosts('')
def kill():
    """Send SIGTERM to postgres and redis-server"""
    subprocess.call(
        "ps -ef | awk '/(postgres|redis)/ {print $2}' | xargs kill",
        shell=True)
