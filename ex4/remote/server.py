import socket
import threading
import pickle
import os

# Parâmentros base para o funcionamento do server
HEADER = 1000000
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT'

# Configuração e inicialização dos server com sockets
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_with_client(conn, addr):
    directory = os.path.abspath(__file__)
    print(f'[NOVA CONEXÃO] {addr} conectado.\n')
    connected = True
    while connected:

        data = conn.recv(
            HEADER)  # Dentro dos parenteses é colocado quantos bytes pode ser recebido no server... Lembrar de tratar no client
        # Verifica-se se há algo na msg.
        if data:
            data = pickle.loads(data)
            if len(data) == 3:
                acao, file_name, file_content = data
            else:
                acao, file_name = data

            if acao == '1':  # Local to Remote
                # Mini gambiarra pra fazer funcionar. Não estava conseguindo usar o caminho relativo
                directory = directory.replace('server.py', r'received\\')
                file = open(directory + file_name, 'wb')
                file.write(file_content)
                file.close()
                conn.send('Envio Concluído Com Sucesso!'.encode(FORMAT))
            else:
                directory = directory.replace('server.py', rf'files\\')

                file = open(directory + file_name, 'rb')
                file_content = file.read()
                file.close()
                file_content = pickle.dumps(file_content)
                conn.send(file_content)

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
