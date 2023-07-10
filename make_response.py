def make_response(*args, **kwargs):
    response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    return response + args[0]
