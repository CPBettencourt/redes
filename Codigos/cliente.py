#codigo para o cliente

#Os comentarios aqui adicionados sao para dar inicio ao relatorio

import socket
import select
import errno
import sys

tam_cabe = 10 #Tamanho do cabecalho
host = '169.254.141.186'
port = 2000
end = (host, port)
nome = input("Escolha seu nome de usuario: \n")

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Criacao do mecanismo de socket para estabelecimento de conexao; AF_INET indica uso do
#protocolo IPv4, SOCK_STREAM indica uso do protocolo TCP

conn.connect(end)
#Estabelecimento da conexao ao servidor atraves do host e porta pre-definidos
conn.setblocking(False)

usuario = nome.encode('utf-8')
usuario_cabe = f'{len(nome):<{tam_cabe}}'.encode('utf-8')
conn.send(usuario_cabe + usuario)

while True:
	mensagem = input(f'{nome} > ')
	if mensagem:
		mensagem = mensagem.encode('utf-8')
		mensagem_cabe = f'{len(mensagem):<{tam_cabe}}'.encode('utf-8')
		conn.send(mensagem_cabe + mensagem)
	
	try:
		while True:
			usuario_cabe = conn.recv(tam_cabe)
			if not len(usuario_cabe):
				print('A conexão foi encerrada pelo servidor.')
				sys.exit()
			
			tam_usuario = int(usuario_cabe.decode('utf-8').strip())
			usuario = conn.recv(usuario_cabe).decode('utf-8')
			
			mensagem_cabe = conn.recv(tam_cabe)
			tam_mensagem = int(mensagem_cabe.decode('utf-8').strip())
			mensagem = conn.recv(tam_mensagem).decode('utf-8')
			
			print(f'{usuario} > {mensagem}')
	
	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != EWOULDBLOCK:
			print('Erro de leitura', str(e))
			sys.exit()
		continue
	
	except Exception as e:
		print('Erro generalizado', str(e))
		sys.exit()
