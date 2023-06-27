#import usocket as socket
import socket
import time
#import tools
import render_template 

# Dictionary to store route handlers
route_handlers = {}

def route(path):
    # Decorator to register a route handler
    def decorator(func):
        route_handlers[path] = func
        return func
    return decorator

def run(hostname = '0.0.0.0', port = 5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((hostname, port))
    server_socket.listen(5)

    # Set the server socket to non-blocking mode
    server_socket.setblocking(False)

    print("Let's try")

    counter = 1
    clients = []

    while True:
        try:
            # Accept new client connections
            client_socket, client_address = server_socket.accept()
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
#                print(request)
#                print(counter)
                print(clients)

                # Parse the request to extract the path
                path = parse_request_path(request)

                # Find the corresponding route handler
                handler = route_handlers.get(path)

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

def parse_request_path(request):
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


@route('/test')
def test():
    print(route_handlers)
    counter = 0
    response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nok {counter}'
    counter += 1
    return response + ' tescik'

@route('/home')
def home():
    print(route_handlers)
    counter = 0
    response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nok {counter} <h1>asdasd</h1>'
    counter += 1
    return response


@route('/index')
def index():
    print(route_handlers)
    response = render_template.run('index.html')
    return make_response(render_template('index.html'))

if __name__ == '__main__':
    run()
