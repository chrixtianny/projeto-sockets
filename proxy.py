import socket
import threading

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8989
BUFFER_SIZE = 4096

def cliente_handler(client_socket):
    request = client_socket.recv(BUFFER_SIZE)
    print(f'Requisição: {request}')
    
    linhas_requisicao = request.split(b'\r\n')
    primeira_linha = linhas_requisicao[0].decode('utf-8')
    url = primeira_linha.split(' ')[1]
    print(f'URL: {url}')

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
        porta_destino = 80
        host_destino = url[:posicao_servidor]
    else:
        porta_destino = int(url[posicao_porta+1:posicao_servidor])
        host_destino = url[:posicao_porta]
    
    print(f'Conexão com {host_destino} na porta {porta_destino}')

    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.connect((host_destino, porta_destino))

    proxy_socket.send(request)

    while True:
        resposta = proxy_socket.recv(BUFFER_SIZE)
        if len(resposta) > 0:
            client_socket.send(resposta)
        else:
            break

    proxy_socket.close()
    client_socket.close()

def main():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((LOCAL_HOST, LOCAL_PORT))
    proxy_socket.listen(5)
    print(f'[*] Escutando em {LOCAL_HOST}:{LOCAL_PORT}')

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f'[*] Conexão recebida de {addr[0]}:{addr[1]}')
        client_thread = threading.Thread(target=cliente_handler, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    main()
