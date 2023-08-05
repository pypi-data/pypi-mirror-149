def dictify_query(query_string):
    query = {}
    if query_string == '':
        return query
    for param in query_string.split("&"):
        key, value = param.split("=")
        query.update({key: value})
    return query