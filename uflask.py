import usocket as socket
import time
import tools

print('Usage: call run method with hostname and port as arguments')

def run(hostname, port):
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
                print(request)
                print(counter)

                if 'GET /home' in request:
                    response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nok {counter}'
                    counter += 1

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

