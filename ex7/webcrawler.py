from threading import Thread,active_count
from urllib import request, error
import re
import json
from time import sleep

ARQUIVO_RESULTADOS = 'resultados.json'
ARQUIVO_URLS = 'lista_urls.txt'
ARQUIVO_PALAVRAS = 'lista_palavras.txt'


def add_urls(url_encontradas):  # Adiciona urls no final do arquivo de urls

    with open(ARQUIVO_URLS, 'a', encoding='utf-8') as file:
        for url in url_encontradas:
            file.write(f'{url}\n')


def read_urls(qtd: int):  # Realiza-se leitura do problema
    file = open(ARQUIVO_URLS, 'r',encoding='utf-8')

    data = file.read().split('\n')
    # usuário está pedindo mais urls do que existem
    if qtd > len(data):
        print(
            'Não há quantidade de urls solicitada no seu arquivo. \nExecute a aplicação novamente e coloque um valor válido!')
        exit(0)

    lista_urls = []
    for i in data:
        if len(lista_urls) < qtd:
            lista_urls.append(i)
    return lista_urls


def read_palavras():
    file = open(ARQUIVO_PALAVRAS, 'r',encoding='utf-8')
    lista = []

    lista = file.read().split('\n')

    return lista


def save_result(results):
    with open(ARQUIVO_RESULTADOS, 'w',encoding='utf-8') as file:
        json.dump(results, file, indent=4)


def scrapping(url, palavras, results):  # Realiza o scrapping desejado
    print(F'[ ATUANDO EM URL ] {url}')

    # requisita na url e recebe o text em html
    html = ''
    try:
        html = request.urlopen(url).read().decode('utf-8')
    except:
        return

    # Dicionário para guardar os resultados das buscas
    dict_result_search = {}

    # para cada palavra a ser pesquisada faça
    for palavra in palavras:
        r = re.findall(palavra,
                       html)  # Procura todas as palavras. A cada match adiciona o padrão encontrado na lista e por fim retorna a lista
        frequencia = len(r)
        # Caso encontrou alguma palavra adiciona a palavra e o valor da frequencia de encontros
        if frequencia > 0:
            dict_result_search[palavra] = frequencia
            # A url da vez se é adicionado o dicionário que contém a palavra procurada e quantas foram encontradas
            results[url] = dict_result_search


    # Busca em todo site outras urls, caso exista coleta
    urls_on_page = re.findall(r'(?P<url>https?://[^\s]+)', html)  # regex que representa uma url
    # Adiciona as urls coletados no nonal do arquivo
    add_urls(urls_on_page)

    print(f'[ SCRAPPING EM URL FINALIZADO ] {url}')


if __name__ == '__main__':
    print('--------------------  W  E  B  C  R  A  W  L  E  R --------------------\n\n')

    # Guarda os resultados. {'url':{'palavra':frequencia}}
    results = {}

    max_urls = int(input('Quantas urls deseja que o Webcrawler realize? '))
    qtd_threads = int(input('Quantas threads vc deseja que operem no Webcrawler? '))


    print('[ INICIALIZANDO WEBCRAWLER ]\n')
    sleep(1)
    # Chama a função que realiza a leitura dos dados do arquivo que contém as urls
    urls = read_urls(max_urls)
    palavras = read_palavras()

    threading_list = []

    print('[ ATRIBUINDO URLS A THREADS ]\n')
    # Aqui é criado n threads e é chamado o método que irá realizar o scrapping da url passada
    for url in urls:
        if len(threading_list) < qtd_threads: #só realiza scrapping pela quantidade de qtd_threads
            t = Thread(target=scrapping, args=(url, palavras, results))
            t.start()
            threading_list.append(t)
        else:
            #Enquanto a quantidade de threads ativas for maior que o desejado fica num loop aguardando alguma finalizar
            while active_count()-1 > qtd_threads:
                # print('Aguardando...')
                continue

            t = Thread(target=scrapping, args=(url, palavras, results))
            t.start()
            threading_list.append(t)


    for thread in threading_list:
        thread.join()  # antes de voltar pra main tem que esperar as threads finalizarem o job



    # Após finalizar todas as threads é salvo os resultados no arquivo results.json
    save_result(results)
    print('[ SCRAPPING  FINALIZADO ]')

# Lembrar de verficar quais urls estão na página, salvar numa lista e adicionar ao arquivo de listas de url
