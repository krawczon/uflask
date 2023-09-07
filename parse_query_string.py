def parse_query_string(query_string):
    result = {}

    matches = re.findall(r'(\w+)=(\w+)', query_string)
    for key, value in matches:
        result[key] = value
    
    print(result)
    return result


def parse_query_string_test(query_string):
    result = {}

    pairs = query_string.split('&')
    for pair in pairs:
        key_value = pair.split('=')
        if len(key_value) == 2:
            key, value = key_value
            result[key] = value

    print(result)
    return result
