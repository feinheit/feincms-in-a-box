from __future__ import absolute_import, unicode_literals

import logging

from django.http import UnreadablePostError


class SkipUnreadablePostError(logging.Filter):
    """
    Skip errors which are caused by aborted POST requests.
    """
    def filter(self, record):
        if (record.exc_info
                and isinstance(record.exc_info[1], UnreadablePostError)):
            return False
        return True
