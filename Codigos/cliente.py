#Codigo para o cliente
#Os comentarios aqui adicionados sao para dar inicio ao relatorio

import socket
import select
import errno
import sys

tam_cabe = 10  #Tamanho do cabecalho
host = '146.164.57.143'
port = 2000
end = (host, port)
nome = input("Escolha seu nome de usuario: \n")

#Criacao do mecanismo de socket para estabelecimento de conexao; AF_INET indica uso do
#protocolo IPv4, SOCK_STREAM indica uso do protocolo TCP
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Estabelecimento da conexao ao servidor atraves do host e porta pre-definidos
conn.connect(end)
#Estabele a conexao para ocorrer bloqueio
conn.setblocking(False)

#Codifica o nome do usuario em bytes, prepara o cabecalho e envia os dados
usuario = nome.encode('utf-8')
usuario_cabe = f'{len(nome):<{tam_cabe}}'.encode('utf-8')
conn.send(usuario_cabe + usuario)

while True:
    #Inicia o loop para envio de mensagens
	mensagem = input(f'{nome} > ')
	if mensagem:
    	#Se a mensagem nao estiver vazia, a codificacao e realizada e os
		#dados enviados
		mensagem = mensagem.encode('utf-8')
		mensagem_cabe = f'{len(mensagem):<{tam_cabe}}'.encode('utf-8')
		conn.send(mensagem_cabe + mensagem)
	
	try:
		while True:
    		#Inicia o loop para recebimento de mensagens
			usuario_cabe = conn.recv(tam_cabe)

			if not len(usuario_cabe):
    			#Caso nao receba dado
				print('A conexão foi encerrada pelo servidor.')
				sys.exit()

			#Recebe e converte o cabecalho em um valor inteiro e recebe e decodifica o nome do usuario
			
			tam_usuario = int(usuario_cabe.decode('utf-8').strip())
			usuario = conn.recv(usuario_cabe).decode('utf-8')
			
			#Faz o mesmo para o conteudo da mensagem
			mensagem_cabe = conn.recv(tam_cabe)
			tam_mensagem = int(mensagem_cabe.decode('utf-8').strip())
			mensagem = conn.recv(tam_mensagem).decode('utf-8')
			
			print(f'{usuario} > {mensagem}')
	
	#Para prevencao de erros em conexoes sem bloqueio
	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Erro de leitura', str(e))
			sys.exit()
		continue
	
	except Exception as e:
		print('Erro generalizado', str(e))
		sys.exit()
