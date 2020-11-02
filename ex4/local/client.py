import socket
import pickle
import os

HEADER = 1000000
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT'
# SERVER = "192.168.0.13"
SERVER = "192.168.0.24"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Realiza a conexão com o server
client.connect((SERVER, PORT))

print('- - - - - - - FTP - - - - - - -\n')
if __name__ == '__main__':
    while True:
        # Mini gambiarra pra fazer funcionar. Não estava conseguindo usar o caminho relativo
        caminho = os.path.abspath(__file__)

        acao = input('Escolha a função! 1-Enviar, 2-Receber: ')

        file_name = input('Informe o nome do arquivo que deseja com extensão(ex.: nome.txt): ')

        if acao == '1':
            caminho = caminho.replace('client.py', r'files\\')

            # Abre o arquivo
            try:
                file = open(caminho+file_name, 'rb')
            except FileNotFoundError:
                print('Arquivo não existe. Crie o arquivo que deseja enviar e tente novamente!')
                break

            file_content = file.read()  # Pega os dados
            file.close()  # Fecha o arquivo após a operação
            data = [acao, file_name, file_content]
            client.send(pickle.dumps(data))
            print(client.recv(HEADER).decode(FORMAT))
        else:
            caminho = caminho.replace('client.py', r'received\\')

            data = [acao, file_name]
            client.send(pickle.dumps(data))
            file_content = client.recv(HEADER)
            file_content = pickle.loads(file_content)

            # Abre o arquivo
            try:
                file = open(caminho+file_name, 'wb')
            except FileNotFoundError:
                print('Arquivo não existe. Crie o arquivo que deseja enviar e tente novamente!')
                break

            file.write(file_content)  # Pega os dados
            print('Arquivo recebido com sucesso!')
            file.close()  # Fecha o arquivo após a operação
