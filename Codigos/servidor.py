#----------Trabalho de Redes----------
#comunicação clinte servidor
#codigo para o servidor

#Os comentarios aqui adicionados sao para dar inicio ao relatorio

import socket

host = '' #Indica qualquer IP
port = 8080
addr = (host, port)

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Criacao do mecanismo de socket para recebimento da conexao, AF_INET indica a família 
#do protocolo e SOCK_STREAM indica que será TCP/IP

    #serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#Verificar a necessidade dessa linha
#Zera o TIME_WAIT do Socket, se o programa estiver aguardando uma conexão e o usuário der CTRL+C para 
#interromper, o programa  será fechado, porém o Socket continua na escuta e se a mesma porta não poderá ser 
#utilizada em outro programa

serv.bind(addr)
#Aqui e definido de qual IP e porta o servidor deve esperar conexao

serv.listen(10)
#Define o limite de conexoes
print("Agurdando conexao")

while True:
    conn, client = serv.accept()
    #Servidor aguarda conexoes
    with conn:
        print("Connected by ", client)
        while True:
            data = conn.recv(4096)
            #Aguarda um dado de até 4096 bytes

            if not data: 
                break
        conn.sendall(data)
    conn.close()
    print("Client disconnected")
