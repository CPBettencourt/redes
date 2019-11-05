import socket
import select
import errno
import sys

HEADER_LENGTH = 10

host = '169.254.141.186'
port = 2000
addr = (host, port)
my_username = input("Choose your username: \n")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(addr)
client.setblocking(False)
#A funcao de recebimento nao sera bloqueada

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client.send(username_header + username)

while True:
    message = input(f'{my_username} > ')
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client.send(message_header + message)
    
    try:
        while True:
            username_header = client.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Server closed the connection")
                sys.exit()
            
            username_length = int(username_header.decode("utf-8".strip()))
            username = client.recv(username_length).decode("utf-8")
            
            message_header = client.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        
        continue
    
    except Exception as e:
        print('Genral error', str(e))
        sys.exit()
