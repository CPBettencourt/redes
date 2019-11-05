#comunicacao clinte servidor
#codigo para o cliente

#Os comentarios aqui adicionados sao para dar inicio ao relatorio

import socket

host = '192.168.10'
port = 1234
addr = (host, port) 

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Criacao do mecanismo de socket para estabelecimento de conexao; AF_INET indica uso do
#protocolo IPv4, SOCK_STREAM indica uso do protocolo TCP

conn.connect(addr)
#Estabelecimento da conexao ao servidor atraves do host e porta pre-definidos

while True:
	line = input()
	conn.send(line)
	#Entrada de dados e envio ao servidor
	
	data = conn.recv(4096)
	#Recebimento de dado do servidor de ate 4096 bytes
	if not data:
		break
	print (data)

conn.close()
