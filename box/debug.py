# flake8: noqa
from __future__ import absolute_import, unicode_literals

import time
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.db import connection
from django.template import Context, Template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

TEMPLATE = """
<div id="debug" style="clear:both;">
<a href="#debugbox"
    onclick="this.style.display = 'none';
        document.getElementById('debugbox').style.display = 'block';
        return false;"
        style="font-size: small; color: red; text-decoration: none; display: block; margin: 12px;"
>+</a>

<div style="display: none;clear: both; border: 1px solid red; padding: 12px; margin: 12px; overflow: scroll; white-space: wrap;  background: #eee; font-size: 11px;" id="debugbox">

<p>Server-time taken: {{ server_time|floatformat:"5" }} seconds</p>
<p>View: <strong>{{view}}</strong></p>
<p>SQL executed:</p>
{% if sql %}
<ol>
{% for query in sql %}
    <li{{ query.style }}>{{ query.sql|linebreaksbr }}
        <p>took {{ query.time|floatformat:"3" }} seconds</p>{{ query.count }}</li>
{% endfor %}
</ol>
<p>Total SQL time: {{ sql_total }} in {{num_queries}} queries</p>
{% else %}
    None
{% endif %}
</div>
</div>
</body>
"""


class DebugFooter(object):
    def __init__(self):
        if not settings.DEBUG:
            raise MiddlewareNotUsed

    def process_request(self, request):
        self.time_started = time.time()
        self.contexts_used = []
        self.sql_offset_start = len(connection.queries)

    def process_response(self, request, response):
        if not (
                not request.is_ajax() and
                response.status_code == 200 and
                'text/html' in response['Content-Type']
                ):
            return response

        sql_queries = connection.queries[self.sql_offset_start:]
        # Reformat sql queries a bit
        sql_total = 0.0
        sql_counts = {}
        for query in sql_queries:
            raw_sql = query['sql']
            query['sql'] = reformat_sql(query['sql'])
            sql_total += float(query['time'])
            count = sql_counts.get(raw_sql,0) + 1
            sql_counts[raw_sql] = count
            if count > 1:
                query['style'] = mark_safe(' style="background:#ffdddd;"')
                query['count'] = mark_safe('<p>duplicate query count=%s</p>' % count)
            else:
                query['style'] = ''
                query['count'] = ''

        from django.core.urlresolvers import resolve
        view_func, args, kwargs = resolve(request.META['PATH_INFO']) #@UnusedVariable

        view =  '%s.%s' % (view_func.__module__, view_func.__name__)

        vf = view_func
        breaker = 10
        while not hasattr(vf, 'func_code'):
            if hasattr(vf, 'view_func'):
                vf = vf.view_func
            else:
                break  # something's wrong about the assumptions of the decorator
            breaker = breaker - 1
            if breaker < 0:
                break

        debug_content = Template(TEMPLATE).render(Context({
            'server_time': time.time() - self.time_started,
            'sql': sql_queries,
            'sql_total': sql_total,
            'num_queries' : len(sql_queries),
            'view': view
        }))

        content = response.content
        response.content = force_unicode(content).replace('</body>', debug_content)

        return response


def reformat_sql(sql):
    sql = sql.replace('`,`', '`, `')
    sql = sql.replace('` FROM `', '` \n  FROM `')
    sql = sql.replace('` WHERE ', '` \n  WHERE ')
    sql = sql.replace(' ORDER BY ', ' \n  ORDER BY ')
    return sql
