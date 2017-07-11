def run_raw_sql(query_template, params):
    query_template = Template(query_template)
    query = query_template.render(Context(params))

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = dictfetchall(cursor)

    return result
