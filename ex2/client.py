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


class Quadrilatero:

    def ledados(self):
        self.lado1 = input('Insira o valor do lado 1: ')
        self.lado2 = input('Insira o valor do lado 2: ')
        self.lado3 = input('Insira o valor do lado 3: ')
        self.lado4 = input('Insira o valor do lado 4: ')

    def indicatipoquadrilatero(self):
        lados = [self.lado1, self.lado2, self.lado3, self.lado4]
        lados.sort()

        if lados[0] == lados[1] == lados[2] == lados[3]:
            self.tipo = 'Quadrado'
        elif (lados[0] == lados[1]) and (lados[2] == lados[3]):
            self.tipo = 'Retângulo'
        else:
            self.tipo = 'Quadrilátero'

    def mostradados(self):
        print('--------- Dados do Objeto ---------')
        print(f'Lado1: {self.lado1}')
        print(f'Lado2: {self.lado2}')
        print(f'Lado3: {self.lado3}')
        print(f'Lado4: {self.lado4}')
        print(f'Tipo Quadrilátero: {self.tipo}')


def send(msg):
    client.send(msg)


if __name__ == '__main__':
    while True:
        # Instancia-se um objeto da classe Quadrilátero
        q = Quadrilatero()

        # Realiza-se a leitura dos lados
        q.ledados()

        # "Picota-se" esse objeto em uma string de bytes
        msg = pickle.dumps(q)
        # envia-se para o servidor
        send(msg)

        # Resposta do servidor
        q = pickle.loads(client.recv(HEADER))
        q.mostradados()
        print('-----------------------------------\n\n')
