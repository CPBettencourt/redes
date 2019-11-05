#----------Trabalho de Redes----------
#comunicação clinte servidor
#codigo para o cliente

#Os comentários aqui adicionados são para dar início ao relatório

import socket

host = ''
port = 8080
addr = (host, port)

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Criação do mecanismo de socket para estabelecimento de conexão; AF_INET indica uso do
#protocolo IPv4, SOCK_STREAM indica uso do protocolo TCP

conn.connect(addr)
#Estabelecimento da conexão ao servidor através do host e porta pré-definidos

while True:
	line = input()
	conn.send(line)
	#Entrada de dados e envio ao servidor
	
	data = conn.recv(4096)
	#Recebimento de dado do servidor de até 4096 bytes
	if not data:
		break
	print (data)

conn.close()
