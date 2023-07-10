def get_method(request):
    if 'GET' in request:
        method = 'GET'
        return method
    if 'POST' in request:
        method = 'POST'
        return method
