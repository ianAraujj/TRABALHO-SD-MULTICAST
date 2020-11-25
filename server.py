import socket
import struct
import sys
import threading
from threading import Thread
import time

# Thread que Envia Regurlamente mensagens para os Outros Servidores
class EstouVivo(Thread):

    def __init__ (self, sock, pin, multicast_group_server):
        Thread.__init__(self)
        self.sock = sock
        self.pin = pin
        self.multicast_group_server = multicast_group_server

    def run(self):
        while True:
            mensagem =  "DISPONIVEL " + str(self.pin)
            self.sock.sendto(str(mensagem).encode(), self.multicast_group_server)
            time.sleep(2)


# Thread que Regurlamente LIMPA a Tabela contendo Outros Servidores
class LimparTabela(Thread):

    def __init__ (self, servidores_disponiveis):
        Thread.__init__(self)
        self.servidores_disponiveis = servidores_disponiveis

    def run(self):
        while True:
            print("LIMPANDO ...")
            del self.servidores_disponiveis[:]
            time.sleep(3)

def imprimirMensagem(data, address):
    print("Recebi algo de: " + str(address))

def atualizarTabela(data, servidores_disponiveis, pin):
    if "DISPONIVEL" in str(data):
        pin_server = str(data)[11:]
        try:
            if int(pin) == int(pin_server):
                return
        except:
            pass
        if pin_server not in servidores_disponiveis:
            servidores_disponiveis.append(pin_server)

def exibirServidores(servidores_disponiveis):
    print("OUTROS SERVIDORES DISPONIVEIS: \n")
    for servidor in servidores_disponiveis:
        print("PIN -> " + str(servidor))
        print("\n")
    print("\n")

def devoResponder(pin, servidores_disponiveis):
    for pin_server in servidores_disponiveis:
        if int(pin_server) < int(pin):
            return False
    return True

def validarPIN(pin):
    try:
        int(pin)
        return True
    except:
        return False


# Multicast para comunicacao entre o Cliente e os Servidores
multicast_group = '224.3.29.71'

# Multicast para comunicacao exclusiva de Servidores
multicast_group_server_address = ('224.3.29.72', 10000)
multicast_group_server = '224.3.29.72'
server_address = ('', 10000)

# Criando o SOCKET UDP e Definindo o TTL
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
sock.bind(server_address)

#Registrar Primeiro Grupo de MUlticast
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

#Registrar Segundo Grupo de MUlticast
group = socket.inet_aton(multicast_group_server)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)



servidores_disponiveis = []

while True:
    entrada = input("Digite o PIN do Servidor: ")

    if validarPIN(entrada):
        pin = entrada
        break
    else:
        print("\n** ERRO ! O PIN deve ser um Valor Inteiro.\n")


thread_one = EstouVivo(sock, pin, multicast_group_server_address)
thread_one.start()
thread_two = LimparTabela(servidores_disponiveis)
thread_two.start()

while True:

    data, address = sock.recvfrom(1024)

    if str(data)[:7] == "client ":
        imprimirMensagem(data, address)

        if devoResponder(pin, servidores_disponiveis):
            resposta = ""
            if int(str(data)[7:]) % 2 == 0:
                resposta = "PAR!"
            else:
                resposta = "IMPAR!"

            sock.sendto(resposta.encode(), address)

    else:
        atualizarTabela(data.decode(), servidores_disponiveis, pin)
        exibirServidores(servidores_disponiveis)

sock.close()