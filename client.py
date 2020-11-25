import socket
import struct
import sys

# Tempo na qual o Cliente Espera, antes de reenviar a mensagem
TIMEOUT = 1.0

multicast_group = ('224.3.29.71', 10000)

# Criando o SOCKET UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

# Definindo o TTL
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

def receberEntrada():
    mensagem = input('Digite um Inteiro: ')
    mensagem = "client " + str(mensagem)
    return mensagem

def enviarMensagem(sock, mensagem, multicast_group):
    print("Enviando ... ")
    sock.sendto(str(mensagem).encode(), multicast_group)

while True:

    mensagem = receberEntrada()
    sock.sendto(str(mensagem).encode(), multicast_group)
    #enviarMensagem(sock, mensagem, multicast_group)

    while True:
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out')
            sock.sendto(str(mensagem).encode(), multicast_group)
            #enviarMensagem(sock, mensagem, multicast_group)
        else:
            print("Mensagem Recebida: " + str(data) + ", de " + str(server))
            break

sock.close()