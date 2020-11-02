import socket
import threading

# Parâmentros base para o funcionamento do server
HEADER = 64
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
        msg_length = conn.recv(HEADER).decode(
            FORMAT)  # Dentro dos parenteses é colocado quantos bytes pode ser recebido no server... Lembrar de tratar no client
        # Verifica-se se há algo na msg.
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:  # Verifica-se a msg enviada pelo client foi a definida como desconexão da rede
                break

            print(f'[{addr}] {msg}')

            """
            resolver problema

            """

            conn.send('Msg recebida'.encode(FORMAT))

    # Finaliza a conexão com o client
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
