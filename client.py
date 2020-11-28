import socket
import struct
import sys
import time

# Tempo na qual o Cliente Espera, antes de reenviar a mensagem
TIMEOUT = 5
# Endereço do Multicast
multicast_group = ('224.3.29.71', 10000)

# Criando o SOCKET UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

# Definindo o TTL
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

def receberExpressao(num_sequencia):
    mensagem = input('\nDigite a Expressão: ')    
    mensagem = "client " + str(mensagem) + "num_seq=" + str(num_sequencia)
    return mensagem

def enviarMensagem(sock, mensagem, multicast_group):
    print("Calculando ... um momento\n")
    time.sleep(0.7)
    sock.sendto(str(mensagem).encode(), multicast_group)


num_sequencia = 0

while True:

    num_sequencia += 1
    mensagem = receberExpressao(num_sequencia)
    
    enviarMensagem(sock, mensagem, multicast_group)

    while True:
        try:
            data, server = sock.recvfrom(1024)
        except socket.timeout:
            enviarMensagem(sock, mensagem, multicast_group)
        else:
            resposta = data.decode()
        
            payload,header=resposta.split("server_id=")
            id_server, num_sequencia_recebido = header.split("num_seq=")


            if int(num_sequencia_recebido) == int(num_sequencia):
                if payload == "FALHA":
                    resultado = "Expressao Invalida !!"
                else:
                    resultado = str(payload)

                print("Resultado: " + str(resultado))
                print("Respondido pelo Servidor de ID: " + str(id_server))
                
                break

sock.close()