def parse_query_string(query_string):
    data = {}
    pairs = query_string.split()[-1].split('&')
    for pair in pairs:
        key, value = pair.split('=')
        data[key] = value
    return data
