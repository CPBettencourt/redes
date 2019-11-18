#comunicação peer to peer

import os
import socket
import sys
from threading import Thread
import time

tam_cabe = 5

def udp_chat():
    global nome 
    global transm_socket
    global atual

    while True:
        #Le o caractere que indica o tipo de mensagem
        recebido = transm_socket.recv(1024).decode('utf-8')

        if not len(recebido):
            tam_usuario = int(recebido[:tam_cabe].strip())
            usuario = recebido[tam_cabe:tam_cabe+tam_usuario]
        
        #Se for uma mensagem
        if usuario[:1] == 'm':
            cabe_mensagem = recebido[tam_cabe+tam_usuario:tam_cabe+tam_usuario+tam_cabe]

            #Verifica se a mesangem esta vazia
            if not len(cabe_mensagem):
                return False

            tam_mensagem = int(cabe_mensagem.strip())
            mensagem = recebido[tam_cabe+tam_usuario+tam_cabe:tam_cabe+tam_usuario+tam_cabe+tam_mensagem]

            print(usuario[1:]+">>"+mensagem)

        #Se for um aviso da presenca do usuario na rede
        elif usuario[:1] == 'o':
            if not (usuario[1:] in atualmente_conectado):
                atualmente_conectado.append(usuario[1:])
                print("Nova conexao aceita de " + usuario[1:])
                print("Total de usuarios conectados: " + str(len(atualmente_conectado)))
            
        #Se for um aviso de saida da rede
        elif usuario[:1] == 's':
            if (usuar[1:] in atualmente_conectado):
                atualmente_conectado.remove(usuario[1:])
                print("Conexao encerrada com " + usuario[1:])
                print("Total de usuarios conectados: " + str(len(atualmente_conectado)))
        
def envia_mensagem_trasmissao():
    global nome
    global enviar_socket
    enviar_socket.setblocking(False)

    while True:
        #Usuario envia mensagem
        data = input(nome + ">>")

        #Verifica se o usuario quer se desconectar
        if data == 'Exit()':
            usuario = ('s'+nome).encode('utf-8')
            cabe_usuario = f"{len(usuario):<{tam_cabe}}".encode('utf-8')
            enviar_socket.sendto(cabe_usuario+usuario, ('255.255.255.255', 2000))
            os._exit(1)
        
        #Se a mensagem nao estiver vazia
        elif