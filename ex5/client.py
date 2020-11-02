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

print('- - - - - - - H O R Á R I O  A T U A L - - - - - - -\n')
if __name__ == '__main__':

    tempo = float(input('Qual a frequência em segundos vc deseja receber o horário do servidor? '))
    client.send(pickle.dumps(tempo))
    while True:
        horario = client.recv(HEADER)
        horario = pickle.loads(horario)
        print(horario)










