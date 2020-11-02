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

print('- - - - - - - E  S  T  O  Q  U  E - - - - - - -\n\n')

if __name__ == '__main__':
    while True:
        #Solicito o produto e o quantitativo
        produto = input('Insira o nome do produto: ')
        qtd = input('Insira a quantidade: ')

        #Fiz uma string unindo o valor do produto e o valor da variável qtd, isso pra separar lá no server e fazer as análises
        elem = pickle.dumps(f'{produto} {qtd}') #"Picota-se" o objeto em string de bytes para enviar pro server
        client.send(elem)#envia pro server
        response = pickle.loads(client.recv(HEADER))

        if response == DISCONNECT_MESSAGE:
            print('Conexão Encerrada')
            client.close()
            break
        else:
            print(f'*** {response} ***')
        print('\n\n- - - - - - - E  S  T  O  Q  U  E - - - - - - -\n\n')




