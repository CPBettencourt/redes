#Codigo para o servidor
#Os comentarios aqui adicionados sao para dar inicio ao relatorio

import socket
import select

reg = open('message_log.txt', 'a+') #Arquivo txt registrando as mensagens da sessão
tam_cabe = 10 #Tamanho do cabecalho
host = '' #Indica o IP
port = 2000
end = (host, port)

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Criacao do mecanismo de socket para recebimento da conexao, AF_INET indica a familia 
#do protocolo e SOCK_STREAM indica que sera TCP/IP
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
#Apos cada print, as informacoes serao registradas no arquivo de texto
reg.write(u'Aguardando conexão' + '\n')

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
    #Aqui os sockets que estão sendo lidos e algumas excecoes são incluidas em uma lista
    #de sockets, enquanto os outros são colocados em uma lista vazia

    for socket_atual in sockets_lidos:
        if socket_atual == serv:
            #Isso acontece quando um novo usuario se conecta, então o servidor o aceita
            #e o usuario envia seu nome
            conn, conn_end = serv.accept()
            user = receive_message(conn)

            if user is False:
                #Caso ele tenha se desconectado
                continue

            sockets_lista.append(conn)
            #Adiciona o socket na lista
            clients[conn] = user
            #Salva o nome e o cabecalho do usuario

            print('Nova conexao aceita de: {}'.format(user['info'].decode('utf-8')))
            reg.write('Nova conexao aceita de: {} \n'.format(user['info'].decode('utf-8')))
            
        else:
            message = receive_message(socket_atual)

            if message is False:
                #Usuario desconectado
                print('Conexao encerrada com: {}'.format(clients[socket_atual]['info'].decode('utf-8')))
                reg.write('Conexao encerrada com: {} \n'.format(clients[socket_atual]['info'].decode('utf-8')))
                #Socket e usuario sao deletados
                sockets_lista.remove(socket_atual)
                del clients[socket_atual]
                
                if len(sockets_lista) == 1:
                    break

                continue

            #Descobrimos o usuario a partir do socket atual
            user = clients[socket_atual]
            print('Mensagem recebida de {}: {}'.format(user["info"].decode("utf-8"), message["info"].decode("utf-8")))
            reg.write('{}: {}'.format(user["info"].decode("utf-8"), message["info"].decode("utf-8")) + '\n')

            #Estabelecendo conexao entre os clientes
            for client in clients:
                #E enviando a mensagem para todos, menos para quem enviou
                if client != socket_atual:
                    client.send(user['cabecalho'] + user['info'] + message['cabecalho'] + message['info'])
    if len(sockets_lista) == 1:
        break

reg.write('Servidor encerrado')
reg.close()
serv.close()
