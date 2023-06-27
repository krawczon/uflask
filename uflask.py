try:
    import usocket as socket
except ModuleNotFoundError:
    print('can not import usocket library')
    print('This is propably becouse is not on micropython enviroment')
    print('importting socket instead')
finally:
    import socket
import time

# Dictionary to store route handlers

class uFlask():
    def __init__(self):
        self.route_handlers = {}

    def route(self, path):
        # Decorator to register a route handler
        def decorator(func):
            self.route_handlers[path] = func
            return func
        return decorator

    def run(self, hostname = '0.0.0.0', port = 5000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((hostname, port))
        self.server_socket.listen(5)

        print('Running server '+hostname, 'on port ',str(port))

        # Set the server socket to non-blocking mode
        self.server_socket.setblocking(False)

        clients = []
        
        run = True

        while True:
            try:
                # Accept new client connections
                client_socket, client_address = self.server_socket.accept()
                clients.append(client_socket)
                print("New client connected:", client_address)
            except OSError:
                pass

            # Iterate over connected clients
            for client_socket in clients:
                try:
                    # Receive data from the client
                    request = client_socket.recv(1024)
                    request = str(request)
                    print('request ------------------------------------')
                    print(request)
                    print('clietns ------------------------------------')
                    print(clients)

                    # Parse the request to extract the path
                    path = self.parse_request_path(request)

                    # Find the corresponding route handler
                    handler = self.route_handlers.get(path)

                    if handler:
                        # Call the route handler
                        response = handler()
                        client_socket.send(response.encode('utf-8'))
                    else:
                        client_socket.send('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\nnot ok'.encode('utf-8'))

                    # Close the client connection
                    client_socket.close()
                    clients.remove(client_socket)
                except OSError:
                    pass

            # Add a small delay to prevent high CPU usage
            time.sleep(0.01)

    def parse_request_path(self, request):
        # Parse the request to extract the path
        lines = request.split('\r\n')
        if lines:
            # First line of the request should contain the method and path
            parts = lines[0].split(' ')
            if len(parts) >= 2:
                return parts[1]
        return ''

def make_response(*args, **kwargs):
    response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    return response + args[0]

def render_template(*args, **kwargs):
    file = open(args[0], "r")
    content = file.read()
    formated_content = content.format(**kwargs)
    file.close()
    return formated_content

