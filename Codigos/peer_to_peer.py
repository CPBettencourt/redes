#comunicação peer to peer

import os
import socket
import sys
from threading import Thread
import time

reg = open('message_log_p2p.txt', 'a+')
tam_cabe = 5

#Essa funcao recebe as mensagens UDP
def udp_chat():
    global nome 
    global transm_socket
    global atualmente_conectado

    while True:
        #Le o caractere que indica o tipo de mensagem
        recebido = transm_socket.recv(1024).decode('utf-8')

        if not len(recebido):
            tam_usuario = int(recebido[:tam_cabe].strip())
            usuario = recebido[tam_cabe:tam_cabe+tam_usuario]
        
        #Se for uma mensagem
        if usuario[:1] == 'm' and usuario[1:] != nome:
            cabe_mensagem = recebido[tam_cabe+tam_usuario:tam_cabe+tam_usuario+tam_cabe]

            #Verifica se a mensagem esta vazia
            if not len(cabe_mensagem):
                return False

            tam_mensagem = int(cabe_mensagem.strip())
            mensagem = recebido[tam_cabe+tam_usuario+tam_cabe:tam_cabe+tam_usuario+tam_cabe+tam_mensagem]

            print(usuario[1:] + ">>" + mensagem + '\n')

        #Se for um aviso da presenca do usuario na rede
        elif usuario[:1] == 'o' and usuario != nome:
            if not (usuario[1:] in atualmente_conectado):
                atualmente_conectado.append(usuario[1:])
                print("Nova conexao aceita de " + usuario[1:])
                print("Total de usuarios conectados: " + str(len(atualmente_conectado)))
                reg.write('Nova conexao aceita de ' + usuario[1:] + '\n')
            
        #Se for um aviso de saida da rede
        elif usuario[:1] == 's':
            if (usuario[1:] in atualmente_conectado):
                atualmente_conectado.remove(usuario[1:])
                print("Conexao encerrada com " + usuario[1:])
                print("Total de usuarios conectados: " + str(len(atualmente_conectado)))
                reg.write('Conexao encerrada com ' + usuario[1:] + '\n')
        
def envia_mensagem():
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
        elif data != '':
            usuario = ('m'+nome).encode('utf-8')
            cabe_usuario = f"{len(usuario):<{tam_cabe}}".encode('utf-8')
            mensagem = data.encode('utf-8')
            cabe_mensagem = f"{len(mensagem):<{tam_cabe}}".encode('utf-8')
            enviar_socket.sendto(cabe_usuario+usuario+cabe_mensagem+mensagem, ('255.255.255.255', 2000))

#Mantem o envio do nome do usuario para a rede
def envia_status():
    global nome
    global enviar_socket
    enviar_socket.setblocking(False)
    usuario = ('o'+nome).encode('utf-8')
    cabe_usuario = f"{len(usuario):<{tam_cabe}}".encode('utf-8')
    while True:
        time.sleep(1)
        enviar_socket.sendto(cabe_usuario+usuario, ('255.255.255.255', 2000))

def main():
    global transm_socket

    transm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      
    transm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
    transm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   
    transm_socket.bind(('0.0.0.0', 2000))

    global enviar_socket

    enviar_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)           
    enviar_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

    print("Bem-vindo ao Chat P2P \nPara sair digite: Exit()")

    #Escolha do nome de usuario
    global nome
    nome = ''
    while True:
        if not nome:
            nome = input('Usuario: ')
            if not nome:
                print('Insira um nome de usuario valido')
            else:
                break
    print('*************************************************')  

    global recebe_thread
    recebe_thread = Thread(target=udp_chat)               
    global enviar_msg_thread
    enviar_msg_thread = Thread(target=envia_mensagem)  
    global atualmente_conectado
    atualmente_conectado = []                                         
    global enviar_online_thread
    enviar_online_thread = Thread(target=envia_status) 
    recebe_thread.start()                                          
    enviar_msg_thread.start()                                       
    enviar_online_thread.start()                                    
    recebe_thread.join()                                           
    enviar_msg_thread.join()                                        
    enviar_online_thread.join()                                     

if __name__ == '__main__':
    main()