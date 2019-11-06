#codigo para o servidor
#Os comentarios aqui adicionados sao para dar inicio ao relatorio

import socket
import select

reg = '' #Registro das mensagens da sessão
tam_cabe = 10 #Tamanho do cabecalho
host = '169.254.141.186' #Indica qualquer IP
port = 2000
end = (host, port)

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEend, 1)
#Criacao do mecanismo de socket para recebimento da conexao, AF_INET indica a familia 
#do protocolo e SOCK_STREAM indica que sera TCP/IP
#Zera o TIME_WAIT do Socket, caso contrario, se o programa estiver aguardando uma conexao e o usuario der CTRL+C para 
#interromper, o programa  sera fechado, porem o Socket continua na escuta e se a mesma porta nao podera ser 
#utilizada em outro programa

serv.bind(end)
#Aqui e definido de qual IP e porta o servidor deve esperar conexao

serv.listen()
#Define o limite de conexoes

sockets_lista = [serv]
#Lista de todos os sockets conectados a essa rede
clients = {}
#Inicia um dicionario de clientes (conexoes)

print(u"Aguardando conexão")

#Funcao que decodifica a mensagem
#Ela recebe o tamanho esperado da mensagem e depois retorna um dicionario da mensagem
#Fragmentada contendo o cabecalho e o conteudo da mensagem de fato
def receive_message(conn):
    try:
        cabe_mensagem = conn.recv(tam_cabe)

        if not len(cabe_mensagem):
            return False

        tam_mensagem = int(cabe_mensagem.decode('utf-8').strip())

        return {'cabecalho': cabe_mensagem, 'info': conn.recv(tam_mensagem)}

    except:
        return False

while True:
    sockets_lidos, _, sockets_excecoes = select.select(sockets_lista, [], sockets_lista)

    for socket_atual in sockets_lidos:
        if socket_atual == serv:
            conn, conn_end = server.accept()
            user = receive_message(conn)

            if user is False:
                continue

            sockets_lista.append(conn)
            clients[conn] = user

            print(f'Nova conexao aceita de: {user['data'].decode('utf-8')}')
            reg += f'Nova conexao aceita de: {user['data'].decode('utf-8')}' + '\n'
            
        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f'Conexao encerrada com: {clients[notified_socket]['data'].decode('utf-8')}')
                reg += f'Conexao encerrada com: {clients[notified_socket]['data'].decode('utf-8')}' + '\n'
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                continue

            user = clients[notified_socket]
            print(f'Mensagem recebida de {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            reg += f'{user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}' + '\n'

            for client in clients:

                if client != notified_socket:
                    client.send(user['header'] + user['data'] + message['header'] + message['data'])
                  
                  
log = open('messagem_log.txt', a+)
log.write(reg)
log.close()
