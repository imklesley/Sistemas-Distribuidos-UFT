import socket
import pickle

HEADER = 64
PORT = 8080
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT'
SERVER = "192.168.0.13"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Realiza a conexão com o server
client.connect((SERVER, PORT))


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # Preenche-se quanto
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    print(client.recv(2048).decode(FORMAT))


if __name__ == '__main__':
    while True:
        lista = []
        # Lê-se trÊs valores e os coloca dentro de uma lista
        for i in range(3):
            lista.append(input(f'Insira o 1º número: '))

        # "Picoto" essa lista em uma string de bytes
        msg = pickle.dumps(lista)
        # envia-se para o servidor
        send(msg)
