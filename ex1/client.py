import socket
import pickle

HEADER = 2048
PORT = 8080
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT'
SERVER = "192.168.0.13"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Realiza a conexão com o server
client.connect((SERVER, PORT))


def send(msg):
    client.send(msg)


if __name__ == '__main__':
    while True:
        lista = []
        #Lê-se trÊs valores e os coloca dentro de uma lista
        for i in range(3):
            lista.append(input(f'Insira o {i+1}º número: '))

        #"Picoto" essa lista em uma string de bytes
        msg = pickle.dumps(lista)
        #envia-se para o servidor
        send(msg)

        #Resposta do servidor
        response = pickle.loads(client.recv(HEADER))
        if response == DISCONNECT_MESSAGE:
            print('Primeiro Número Enviado Foi Negativo. Conexão Encerrada!')
            break
        else:
            print(response)
        print('-----------------------------------\n\n')

    client.close()