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
        
        
        if usuario