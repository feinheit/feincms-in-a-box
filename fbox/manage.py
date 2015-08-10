#!/usr/bin/env python
import env
import os
import sys

if __name__ == "__main__":
    env.read_dotenv()
    if 'test' in sys.argv:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "${PROJECT_NAME}.settings.test"
        )
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              env.env("DJANGO_SETTINGS_MODULE",
                                      "${PROJECT_NAME}.settings.local"))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
