from __future__ import unicode_literals

from feincms_cleanse import Cleanse

# Site-wide patch of cleanse settings
# -----------------------------------

Cleanse.allowed_tags['a'] += ('id', 'name')  # Allow anchors
Cleanse.allowed_tags['hr'] = ()  # Allow horizontal rules
Cleanse.allowed_tags['h1'] = ()  # Allow H1
Cleanse.empty_tags += ('hr',)
cleanse_html = Cleanse().cleanse
