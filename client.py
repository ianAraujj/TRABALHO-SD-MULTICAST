import socket
import struct
import sys

# Tempo na qual o Cliente Espera, antes de reenviar a mensagem
TIMEOUT = 1
# Endereço do Multicast
multicast_group = ('224.3.29.71', 10000)

# Criando o SOCKET UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

# Definindo o TTL
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

def receberExpressao():
    mensagem = input('\nDigite a Expressão: ')    
    mensagem = "client " + str(mensagem)
    return mensagem

def enviarMensagem(sock, mensagem, multicast_group):
    print("Enviando ... \n")
    sock.sendto(str(mensagem).encode(), multicast_group)

while True:

    mensagem = receberExpressao()
    enviarMensagem(sock, mensagem, multicast_group)

    while True:
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            enviarMensagem(sock, mensagem, multicast_group)
        else:
            resposta = data.decode()
            
            resultado,id_server=resposta.split("E")
            if resultado == "":
                resultado = "Expressao Invalida !!"
            
            print("Resultado: " + str(resultado))
            print("Respondido pelo Servidor de ID: " + str(id_server))
            break

sock.close()