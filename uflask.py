try:
    import usocket as socket
except ModuleNotFoundError:
    print('can not import usocket library')
finally:
    import socket
import time
from render_template import render_template
from make_response import make_response
from request import Request
from get_method import get_method
from parse_query_string import parse_query_string
        
request = Request()

class uFlask():
    def __init__(self,__name__, request = request):

        self.__name__ = __name__
        self.route_handlers = {}
        self.host = '0.0.0.0'
        self.port = 5000
        self.clients = []
        self.request = request

    def route(self, path, methods = ['GET']):
        # Decorator to register a route handler
        def decorator(func):
#            self.route_handlers['routes'] = {path, func, methods}
            self.route_handlers[path] = {'path': path,'func': func, 'methods': tuple(methods)}
            return func
        return decorator

    def run(self, host = '0.0.0.0', port = 5000, debug = False):
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
                # Accept new client connections
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
            except OSError:
                pass

            # Iterate over connected clients
            for client_socket in self.clients:
                try:
                    # Receive data from the client
                    request = client_socket.recv(1024)
                    request = request.decode()
                    self.request.method = get_method(request)
                    self.request.form = parse_query_string(request)
                    print('request ------------------------------------')
                    print(request)
                    print(self.request.method)

                    # Parse the request to extract the path
                    path = self.parse_request_path(request)
                    # Find the corresponding route handler
                    print(self.route_handlers)
                    handler = self.route_handlers.get(path, {}).get('func')
                    methods = self.route_handlers.get(path, {}).get('methods')
                    

                    if handler and self.request.method in methods:
                        # Call the route handler
                        response = handler()
                        client_socket.send(response.encode('utf-8'))
                    else:
                        message = '''HTTP/1.1 404 Not Found\r\n
                        Content-Type: text/html\r\n\r\n
                        not ok'''.encode('utf-8')
                        client_socket.send(message)

                    # Close the client connection
                    client_socket.close()
                    self.clients.remove(client_socket)

                    if self.quit:
                        self.terminate()

                except OSError:
                    pass

            # Add a small delay to prevent high CPU usage
            time.sleep(0.01)

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
