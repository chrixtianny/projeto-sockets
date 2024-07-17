import socket
import threading
import select

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8989
BUFFER_SIZE = 4096

def cliente_handler(client_socket):
    try:
        request = client_socket.recv(BUFFER_SIZE)
        print(f'Requisição: {request}')

        linhas_requisicao = request.split(b'\r\n')
        primeira_linha = linhas_requisicao[0].decode('utf-8')
        url = primeira_linha.split(' ')[1]
        metodo = primeira_linha.split(' ')[0]

        if metodo == 'CONNECT':
            print('HTTPS request')
            cliente_https_connect(client_socket, url)
        else:
            print(f'URL: {url}')

            posicao_protocolo = url.find('://')
            if posicao_protocolo != -1:
                url = url[posicao_protocolo + 3:]

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
                porta_destino = int(url[(posicao_porta + 1):posicao_servidor])
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

    except Exception as e:
        print(f'Erro no cliente_handler: {e}')
        client_socket.close()

def cliente_https_connect(client_socket, url):
    try:
        posicao_porta = url.find(':')
        if posicao_porta == -1:
            host_destino = url
            porta_destino = 443
        else:
            host_destino = url[:posicao_porta]
            porta_destino = int(url[posicao_porta + 1:])

        print(f'Conexão com {host_destino} na porta {porta_destino}')

        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((host_destino, porta_destino))

        client_socket.send(b'HTTP/1.1 200 Connection Established\r\n\r\n')

        sockets = [client_socket, proxy_socket]

        while True:
            ready_sockets, _, _ = select.select(sockets, [], [])
            for s in ready_sockets:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    return
                if s is client_socket:
                    proxy_socket.sendall(data)
                else:
                    client_socket.sendall(data)

    except Exception as e:
        print(f'Erro ao conectar com o servidor: {e}')
        client_socket.close()
        return

def main():
    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.bind((LOCAL_HOST, LOCAL_PORT))
        proxy_socket.listen(5)
        print(f'[*] Escutando em {LOCAL_HOST}:{LOCAL_PORT}')

        while True:
            client_socket, addr = proxy_socket.accept()
            print(f'[*] Conexão recebida de {addr[0]}:{addr[1]}')
            client_thread = threading.Thread(target=cliente_handler, args=(client_socket,))
            client_thread.start()

    except Exception as e:
        print(f'Erro no main: {e}')

if __name__ == '__main__':
    main()
1