from __future__ import absolute_import, unicode_literals
import env
import os
env.read_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "${PROJECT_NAME}.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
