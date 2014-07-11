from __future__ import absolute_import, unicode_literals

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_name }}.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
