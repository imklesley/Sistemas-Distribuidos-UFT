import socket
import threading
import pickle


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


# Parâmentros base para o funcionamento do server
HEADER = 2048
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT'

# Configuração e inicialização dos server com sockets
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_with_client(conn, addr):
    print(f'[NOVA CONEXÃO] {addr} conectado.\n')

    connected = True
    while connected:
        obj_quad = conn.recv(
            HEADER)  # Dentro dos parenteses é colocado quantos bytes pode ser recebido no server... Lembrar de tratar no client
        # Verifica-se se há algo na msg.
        if obj_quad:
            obj_quad = pickle.loads(obj_quad)
            obj_quad.indicatipoquadrilatero()
            obj_quad = pickle.dumps(obj_quad)
            conn.send(obj_quad)

    # Finaliza a conexão com o client
    print(f'[CONEXÃO ENCERRADA] {addr}')
    conn.close()


def start():
    server.listen()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_with_client, args=(conn, addr))
        thread.start()
        print(f'[CONEXÕES ATIVAS] {threading.active_count() - 1}')


if __name__ == '__main__':
    print('[INICIANDO]  Server está iniciando ...')
    print(F'[AGUARDANDO]  Server está aguardando nova conexão em {SERVER}...')
    start()
