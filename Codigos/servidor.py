#----------Trabalho de Redes----------
#comunicação clinte servidor
#codigo para o servidor

#Os comentarios aqui adicionados sao para dar inicio ao relatorio

import socket

host = '' #Indica qualquer IP
port = 8080
addr = (host, port) 

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Criacao do mecanismo de socket para recebimento da conexao, AF_INET indica a família do protocolo e SOCK_STREAM indica que será TCP/IP

serv.bind(addr)
#Aqui e definido de qual IP e porta o servidor deve esperar conexao

serv.listen(10)
#Define o limite de conexoes
