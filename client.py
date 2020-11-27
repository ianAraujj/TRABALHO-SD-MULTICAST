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

def receberExpressao():
    mensagem = input('\nDigite a Expressão: ')    
    mensagem = "client " + str(mensagem)
    return mensagem

def enviarMensagem(sock, mensagem, multicast_group):
    print("Calculando ... um momento\n")
    time.sleep(0.7)
    sock.sendto(str(mensagem).encode(), multicast_group)

def verificarDuplicatas(historico, resultado, id_server, expressao):
    for i in historico:
        if i[0] == resultado and i[1] != id_server and i[2] != expressao:
            return True
    return False


historico = []


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
            
            
            if verificarDuplicatas(historico, str(resultado), str(id_server), str(mensagem)):
                ## Mensagem Duplicata ou Atrasada
                print("recalculando ....")
            else:
                historico.append((str(resultado), str(id_server), str(mensagem)))

                print("Resultado: " + str(resultado))
                print("Respondido pelo Servidor de ID: " + str(id_server))
                break

sock.close()