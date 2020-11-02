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


def atualiza_estoque(estoque, produto, qtd):
    if produto in estoque:
        if qtd < 0: # Saida
            if estoque[produto] >= abs(qtd):
                estoque[produto] += qtd
                return f'Estoque atualizado e quantidade de {estoque[produto]}'
            else:
                return 'Não é possível fazer a saída de estoque – quantidade menor que o valor desejado'
        else:#Entra
            if estoque[produto] >= qtd:
                estoque[produto] += qtd
                return 1  # Atualização foi um sucesso
            else:
                return 'Não é possível fazer a saída de estoque – quantidade menor que o valor desejado'
    else:
        if qtd <= 0:
            return "Produto inexistente"
        else:
            estoque[produto] = qtd
            return 'Produto Cadastrado Com Sucesso'



def handle_with_client(conn, addr):
    print(f'[NOVA CONEXÃO] {addr} conectado.\n')
    estoque = {'Arroz': 2}
    connected = True
    while connected:
        elem = conn.recv(
            HEADER)  # Dentro dos parenteses é colocado quantos bytes pode ser recebido no server... Lembrar de tratar no client
        # Verifica-se se há algo na msg.
        if elem:
            elem = pickle.loads(elem)
            produto, qtd = elem.split()
            qtd =  int(qtd)
            if produto == 'terminar':
                conn.send(pickle.dumps(DISCONNECT_MESSAGE))
                break
            else:
                resultado = atualiza_estoque(estoque, produto, qtd)
                conn.send(pickle.dumps(resultado))

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
