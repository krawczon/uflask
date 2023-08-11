def parse_query_string(query_string):
    result = {}

    matches = re.findall(r'(\w+)=(\w+)', query_string)
    for key, value in matches:
        result[key] = value
    
    print(result)
    return result

