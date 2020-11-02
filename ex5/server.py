import socket
import threading
import pickle
import datetime # pega a data e tempo atual
from time import sleep



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




        tempo_sec = conn.recv(HEADER)  # Dentro dos parenteses é colocado quantos bytes pode ser recebido no server... Lembrar de tratar no client
        # Verifica-se se há algo na msg.
        if tempo_sec:
            tempo_sec = pickle.loads(tempo_sec)
            while True:
                now = datetime.datetime.now()
                horario = f'O horário atual é: {now.hour}:{now.minute}:{now.second}:{now.microsecond}'
                conn.send(pickle.dumps(horario))
                sleep(tempo_sec)




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
