from django.db import connection
from django.template import Context, Template

def run_raw_sql(query_template, params):
    query_template = Template(query_template)
    query = query_template.render(Context(params))

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = dictfetchall(cursor)

    return result


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
