import socket
import select

HEADER_LENGTH = 10

host = '169.254.141.186'
port = 2000
addr = (host, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)

server.listen(10)

sockets_list = [server]

clients = {}

print(f'Listening for connections on {host}:{port}...')

# Handles message receiving
def receive_message(client):

    try:
        message_header = client.recv(HEADER_LENGTH)
        
        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client.recv(message_length)}

    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server:
            client, client_address = server.accept()
            user = receive_message(client)

            if user is False:
                continue

            sockets_list.append(client)
            clients[client] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        else:
            message = receive_message(notified_socket)

            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                continue

            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client in clients:

                if client != notified_socket:
                    client.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
