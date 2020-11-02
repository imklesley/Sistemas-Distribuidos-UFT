import socket
import threading
import pickle

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
        msg = conn.recv(
            HEADER)  # Dentro dos parenteses é colocado quantos bytes pode ser recebido no server... Lembrar de tratar no client
        # Verifica-se se há algo na msg.
        if msg:
            lista = pickle.loads(msg)

            if int(lista[
                       0]) < 0:  # Se o primeiro número recebido pelo servidor for negativo, o mesmo deve ser finalizado.
                conn.send(pickle.dumps(DISCONNECT_MESSAGE))
                break
            else:
                lista.sort(key=int)

            conn.send(f'O menor valor é: {lista[0]}\nO maior valor é: {lista[2]}\n'.encode(FORMAT))

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











