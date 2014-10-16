#!/usr/bin/env python
import env
import os
import sys

if __name__ == "__main__":
    env.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.project_name }}.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
