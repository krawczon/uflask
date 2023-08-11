try:
    import usocket as socket
except ModuleNotFoundError:
    print('can not import usocket library')
finally:
    import socket
import time
import select
import re

def make_response(*args, **kwargs):
    response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    return response + args[0]

def get_method(request):
    if 'GET' in request:
        method = 'GET'
        return method
    if 'POST' in request:
        method = 'POST'
        return method

class Request():
    def __init__(self):

        self.method = ['None']
        self.form = 1

def parse_query_string(query_string):
    result = {}

    matches = re.findall(r'(\w+)=(\w+)', query_string)
    for key, value in matches:
        result[key] = value
    
    print(result)
    return result

def render_template(template_name, **context):
    template_path = f'templates/{template_name}'

    with open(template_path, 'r') as file:
        template_content = file.read()

    rendered_content = template_content

    for key, value in context.items():
        placeholder = f'{{{{ {key} }}}}'
        rendered_content = rendered_content.replace(placeholder, str(value))

    return f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'+rendered_content

request = Request()

class uFlask():
    def __init__(self, __name__, request=request):

        self.__name__ = __name__
        self.route_handlers = {}
        self.host = '0.0.0.0'
        self.port = 5000
        self.clients = []
        self.request = request

    def route(self, path, methods=['GET']):
        # Decorator to register a route handler
        def decorator(func):
            self.route_handlers[path] = {'path': path, 'func': func, 'methods': tuple(methods)}
            return func
        return decorator

    def run(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(False)
        self.quit = False
        self.run = True
        print(host, port)

        while self.run:
            try:
                # Use select to monitor sockets for incoming data
                readable_sockets, _, _ = select.select([self.server_socket] + self.clients, [], [], 0.01)

                for sock in readable_sockets:
                    if sock == self.server_socket:
                        # Accept new client connections
                        client_socket, client_address = self.server_socket.accept()
                        self.clients.append(client_socket)
                    else:
                        # Receive data from connected clients
                        try:
                            request = sock.recv(1024)
                            request = request.decode()
                            print(request)
                            self.request.method = get_method(request)
                            self.request.form = parse_query_string(request)

                            # Parse the request to extract the path
                            path = self.parse_request_path(request)
                            # Find the corresponding route handler
                            handler = self.route_handlers.get(path, {}).get('func')
                            methods = self.route_handlers.get(path, {}).get('methods')

                            if handler and self.request.method in methods:
                                # Call the route handler
                                response = handler()
                                sock.send(response.encode('utf-8'))
                            else:
                                message = '''HTTP/1.1 404 Not Found\r\n
                                Content-Type: text/html\r\n\r\n
                                not ok'''.encode('utf-8')
                                sock.send(message)

                            # Close the client connection
                            sock.close()
                            self.clients.remove(sock)

                        except OSError:
                            # Client disconnected
                            sock.close()
                            self.clients.remove(sock)

                if self.quit:
                    self.terminate()

            except OSError:
                pass

    def terminate(self):
        for client_socket in self.clients:
            client_socket.close()
            self.clients.remove(client_socket)

        self.run = False
        self.server_socket.close()
        print('uflask terminated')

    def parse_request_path(self, request):
        # Parse the request to extract the path
        lines = request.split('\r\n')
        if lines:
            # First line of the request should contain the method and path
            parts = lines[0].split(' ')
            if len(parts) >= 2:
                return parts[1]
        return ''

