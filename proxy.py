#ALUNOS: CHRISTIANNY KELLY SILVA DOS SANTOS E HAUL MULLER

import socket
import threading
import select

BUFFER_SIZE = 4096

# Caminho para os arquivos com os domínios e palavras proibidas
forbidden_domains_path = r'C:\Users\haulm\Downloads\projeto-sockets-main\projeto-sockets-main\forbidden_domains.txt'
forbidden_words_path = r'C:\Users\haulm\Downloads\projeto-sockets-main\projeto-sockets-main\forbidden_words.txt'

# Funcao para ler o arquivo com  domínios proibidos
def load_forbidden_domains(file_path):
    try:
        with open(file_path, 'r') as file:
            forbidden_domains = file.read().splitlines()
            print(f'Domínios proibidos carregados: {forbidden_domains}')
            return forbidden_domains
    except Exception as e:
        print(f'Erro ao ler {file_path}: {e}')
        return []

# Funcao para ler o arquivo com as palavras proibidas
def load_forbidden_words(file_path):
    try:
        with open(file_path, 'r') as file:
            forbidden_words = file.read().splitlines()
            print(f'Palavras proibidas carregadas: {forbidden_words}')
            return forbidden_words
    except Exception as e:
        print(f'Erro ao ler {file_path}: {e}')
        return []

# Carregar domínios e palavras proibidas
forbidden_domains = load_forbidden_domains(forbidden_domains_path)
forbidden_words = load_forbidden_words(forbidden_words_path)

# verificar se um domínio está na lista de proibidos
def is_domain_forbidden(host):
    for domain in forbidden_domains:
        if domain in host:
            return True
    return False

# verificar se o conteúdo contém alguma daspalavras proibidas
def contains_forbidden_words(content):
    content_lower = content.lower()
    for word in forbidden_words:
        if word.lower() in content_lower:
            return True
    return False

def cliente_handler(client_socket):
    try:
        request = client_socket.recv(BUFFER_SIZE)  # Recebe a requisição do cliente
        print(f'Requisição: {request}')
        
        linhas_requisicao = request.split(b'\r\n')
        primeira_linha = linhas_requisicao[0].decode('utf-8')
        metodo = primeira_linha.split(' ')[0]
        url = primeira_linha.split(' ')[1]
        print(f'URL: {url}')

        # Verifica se a requisição é HTTPS ou não
        if metodo == "CONNECT":
            cliente_https_connect(client_socket, url)
            return

        posicao_protocolo = url.find('://')
        if posicao_protocolo != -1:
            url = url[posicao_protocolo+3:]

        posicao_porta = url.find(':')
        posicao_servidor = url.find('/')
        if posicao_servidor == -1:
            posicao_servidor = len(url)
        
        host_destino = ""
        porta_destino = -1
        if posicao_porta == -1 or posicao_porta > posicao_servidor:
            porta_destino = 80  # Porta padrão HTTP
            host_destino = url[:posicao_servidor]
        else:
            porta_destino = int(url[posicao_porta+1:posicao_servidor])
            host_destino = url[:posicao_porta]

        print(f'Host destino: {host_destino}')
        
        # Verifica se o domínio está na lista de proibidos
        if is_domain_forbidden(host_destino):
            print(f'Acesso proibido a {host_destino}')
            client_socket.send(b"HTTP/1.1 403 Forbidden\r\n\r\nAccess Forbidden")
            client_socket.close()
            return

        print(f'Conexão com {host_destino} na porta {porta_destino}')

        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket para o servidor de destino
        proxy_socket.connect((host_destino, porta_destino))

        proxy_socket.send(request)  # Envia a requisição para o servidor de destino

        response = b""
        while True:
            resposta = proxy_socket.recv(BUFFER_SIZE)
            if len(resposta) > 0:
                response += resposta
            else:
                break

        # Verifica se a resposta contém alguma das palavras proibidas
        if contains_forbidden_words(response.decode('utf-8', errors='ignore')):
            print(f'Conteúdo proibido encontrado em {url}')
            client_socket.send(b"HTTP/1.1 403 Forbidden\r\n\r\nContent Forbidden")
        else:
            client_socket.send(response)  # Envia a resposta para o cliente

        proxy_socket.close()
        client_socket.close()

    except Exception as e:
        print(f'Erro no cliente_handler: {e}')
        client_socket.close()

def cliente_https_connect(client_socket, url):
    try:
        posicao_porta = url.find(':')
        if posicao_porta == -1:
            host_destino = url
            porta_destino = 443  # Porta padrão HTTPS
        else:
            host_destino = url[:posicao_porta]
            porta_destino = int(url[posicao_porta + 1:])

        print(f'Host destino: {host_destino}')
        
        # Verifica se o domínio está na lista de proibidos
        if is_domain_forbidden(host_destino):
            print(f'Acesso proibido a {host_destino}')
            client_socket.send(b"HTTP/1.1 403 Forbidden\r\n\r\nAccess Forbidden")
            client_socket.close()
            return

        print(f'Conexão com {host_destino} na porta {porta_destino}')

        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket para o servidor de destino
        proxy_socket.connect((host_destino, porta_destino))

        client_socket.send(b'HTTP/1.1 200 Connection Established\r\n\r\n')  # Envia resposta de conexão estabelecida ao cliente

        sockets = [client_socket, proxy_socket]

        while True:
            ready_sockets, _, _ = select.select(sockets, [], [])  # Monitora os sockets para leitura
            for s in ready_sockets:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    return
                if s is client_socket:
                    proxy_socket.sendall(data)  # Envia dados do cliente para o servidor
                else:
                    client_socket.sendall(data)  # Envia dados do servidor para o cliente
                    # Verifica se a resposta contém palavras proibidas
                    if contains_forbidden_words(data.decode('utf-8', errors='ignore')):
                        print(f'Conteúdo proibido encontrado em {url}')
                        client_socket.send(b"HTTP/1.1 403 Forbidden\r\n\r\nContent Forbidden")
                        client_socket.close()
                        proxy_socket.close()
                        return

    except Exception as e:
        print(f'Erro ao conectar com o servidor: {e}')
        client_socket.close()
        return

def main():
    LOCAL_HOST = '127.0.0.1'
    LOCAL_PORT = 8989

    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket do proxy
        proxy_socket.bind((LOCAL_HOST, LOCAL_PORT))  # Vincula o socket ao endereço e porta local
        proxy_socket.listen(5)  # Configura o socket para escutar conexões
        print(f'[*] Escutando em {LOCAL_HOST}:{LOCAL_PORT}')

        while True:
            client_socket, addr = proxy_socket.accept()  # Aceita uma nova conexão
            print(f'[*] Conexão recebida de {addr[0]}:{addr[1]}')
            client_thread = threading.Thread(target=cliente_handler, args=(client_socket,))  # Cria uma nova thread para lidar com o cliente
            client_thread.start()

    except Exception as e:
        print(f'Erro no main: {e}')

if __name__ == '__main__':
    main()
