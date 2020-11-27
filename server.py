import socket
import struct
import sys
import threading
from threading import Thread
import time

# Thread que Envia Regularmente mensagens para os Outros Servidores
class EstouVivo(Thread):

    def __init__ (self, sock, id, multicast_group_server):
        Thread.__init__(self)
        self.sock = sock
        self.id = id
        self.multicast_group_server = multicast_group_server

    def run(self):
        while True:
            mensagem =  "DISPONIVEL " + str(self.id)
            self.sock.sendto(str(mensagem).encode(), self.multicast_group_server)
            time.sleep(0.3)


# Thread que Regurlamente LIMPA a Tabela de Servidores
class LimparTabela(Thread):

    def __init__ (self, servidores_disponiveis):
        Thread.__init__(self)
        self.servidores_disponiveis = servidores_disponiveis

    def run(self):
        while True:
            del self.servidores_disponiveis[:]
            time.sleep(1)

def imprimirMensagem(data, address):
    print("Recebi algo de: " + str(address))

def atualizarTabela(data, servidores_disponiveis, id):
    if "DISPONIVEL" in str(data):
        id_server = str(data)[11:]
        try:
            if int(id) == int(id_server):
                return
        except:
            pass
        if id_server not in servidores_disponiveis:
            servidores_disponiveis.append(id_server)

def exibirServidores(servidores_disponiveis):
    print("OUTROS SERVIDORES DISPONIVEIS: \n")
    for servidor in servidores_disponiveis:
        print("ID -> " + str(servidor))
        print("\n")
    print("\n")

def devoResponder(id, servidores_disponiveis):
    for id_server in servidores_disponiveis:
        if int(id_server) < int(id):
            return False
    return True

def validarID(id):
    try:
        int(id)
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
    entrada = input("Digite o ID do Servidor: ")

    if validarID(entrada):
        id = entrada
        break
    else:
        print("\n** ERRO ! O ID deve ser um Valor Inteiro.\n")


thread_one = EstouVivo(sock, id, multicast_group_server_address)
thread_one.start()
thread_two = LimparTabela(servidores_disponiveis)
thread_two.start()

while True:

    time.sleep(0.1)
    data, address = sock.recvfrom(1024)
    data = data.decode()

    ## SE a Mensagem for do Cliente
    if str(data)[:7] == "client ":
        imprimirMensagem(data, address)

        if devoResponder(id, servidores_disponiveis):
            expressao = data[7:]
            resposta = ""

            try:
                resposta = round(eval(expressao), 10)
            except:
                pass

            resposta_com_id = str(resposta) + "E" + str(id)
            sock.sendto(resposta_com_id.encode(), address)

    else:
        ## SE a Mensagem for de um SERVIDOR
        atualizarTabela(data, servidores_disponiveis, id)

sock.close()