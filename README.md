# Integrantes do Projeto
- Haul Muller
- Christianny Santos

##### Desafio: https://codingchallenges.fyi/challenges/challenge-forward-proxy/

### Proxy HTTP/HTTPS com Bloqueio de Domínios e Palavras Proibidas

Este projeto é um servidor proxy que intercepta e filtra tráfego HTTP e HTTPS, bloqueando domínios e palavras proibidas.

#### Usos e Importância de um Proxy

Um servidor proxy atua como intermediário entre um cliente (como um navegador da web) e o servidor de destino. Aqui estão alguns usos e razões para utilizar um proxy:
- **Controle de Acesso**: Bloqueia o acesso a sites indesejados ou prejudiciais, garantindo que os usuários naveguem apenas em conteúdos permitidos.
- **Segurança**: Adiciona uma camada de segurança ao filtrar tráfego malicioso e prevenir ataques.
- **Privacidade**: Esconde o endereço IP dos usuários, protegendo suas identidades e atividades online.
- **Performance**: Pode armazenar em cache (cachear) respostas de servidores, melhorando o tempo de carregamento para solicitações repetidas.
- **Monitoramento**: Permite monitorar e registrar o tráfego da rede, útil para auditorias e controle de uso.

#### Requisitos #####
Python 3.x
##### Bibliotecas Python:
- socket
- threading
- select

#### Arquivos de Configuração
- forbidden_domains.txt: Lista de domínios proibidos.
- forbidden_words.txt: Lista de palavras proibidas.

#### Instalação
1. Clone o repositório:
```
git clone https://github.com/seu-usuario/projeto-sockets.git
```
```
cd projeto-sockets
```

2. Prepare os arquivos de configuração:
- Certifique-se de que os arquivos forbidden_domains.txt e forbidden_words.txt estejam no diretório do projeto.
3. Altere o caminho dos arquivos:
No código proxy_server.py, verifique e altere o caminho dos arquivos forbidden_domains.txt e forbidden_words.txt para o caminho correto onde esses arquivos estão localizados:
```python
forbidden_domains = load_forbidden_domains('caminho/para/forbidden_domains.txt')
forbidden_words = load_forbidden_words('caminho/para/forbidden_words.txt')
```

4. Verifique os domínios e palavras proibidas:
- Antes de iniciar o servidor, verifique o conteúdo dos arquivos forbidden_domains.txt e forbidden_words.txt, já existem alguns exemplos dentro dos arquivos, mas você pode adicionar os domínios ou palavras de sua preferência.

#### Execução
 1. Execute o servidor proxy:
```python
python proxy_server.py
```
 2. Opções para execução
#### Enviar nova requisição no Postman:
 1. Abra o Postman. Clique em Send New Request (Enviar nova requisição).
 2. Escolha a aba Settings que fica abaixo do espaço para a URL da
    requisição. 

	- Configurações de Proxy no Postman:
	- Abaixo do switch que ativa ou desativa as opções Enable SSL certificate verification e Automatically follow redirects, clique em Settings. 
    - Vai abrir um modal com opções no menu lateral. 
    - Escolha a opção Proxy. 
    - Configure com o Proxy Server 127.0.0.1 e porta 8989.

3. Teste no Postman:
	- Coloque a URL que deseja testar com o método GET.
	- Exemplo de URL: http://httpbin.org/get.
	- Clique em Send e verifique se a resposta é recebida corretamente.

#### Configuração do Proxy no Windows

1. Abra as Configurações do Windows (Windows + I).
2. Vá para Rede e Internet > Proxy.
3. Configurar o Proxy Manualmente:
	- Ative a opção Usar um servidor proxy.
	- No campo Endereço, insira 127.0.0.1.
	- No campo Porta, insira 8989.
	- Clique em Salvar.
4. Desativar Cache do Navegador:
Para garantir que o cache do navegador não interfira nos testes, limpe o cache do seu navegador.
5. Teste no Navegador:
	- Abra o navegador e insira a URL que deseja testar.
	- Exemplo de URL: http://httpbin.org/get.
	- Verifique se a resposta é recebida corretamente.

#### Atenção:
##### Após concluir os testes, lembre-se de desativar o uso do proxy configurado para o servidor:

> No Postman, limpe os campos com os dados do Proxy server.

> No windows, volte às configurações de Proxy e limpe os campos com dados do servidor;
> Em seguida, desative a opção Usar um servidor proxy e salve as mudanças.

### Testando
1. Teste uma requisição HTTP:
	- No Postman ou navegador, coloque a URL que deseja testar com o método GET.
	-  Exemplo de URL: http://httpbin.org/get.
	- Verifique a lista de domínios e palavras proibidas.
	- Após verificar, clique em Send (Postman) ou pressione Enter (navegador) e verifique se a resposta é recebida corretamente.

2. Teste uma requisição HTTPS:
	- No Postman ou navegador, coloque a URL que deseja testar com o método GET.
	- Exemplo de URL: https://httpbin.org/get.
	- Verifique a lista de domínios e palavras proibidas.
	-	Após verificar, clique em Send (Postman) ou pressione Enter (navegador) e verifique se a resposta é recebida corretamente.
3. Teste com um domínio proibido:
	- Adicione um domínio à lista forbidden_domains.txt, como httpbin.org.
	- No Postman ou navegador, coloque a URL http://httpbin.org/get e envie a requisição.
	- Verifique se o acesso será negado.
4. Teste com palavras proibidas:
	- Adicione uma palavra à lista forbidden_words.txt, como test.
	- No Postman ou navegador, coloque a URL http://httpbin.org/get?word=test e envie a requisição.
	- Verifique se a o acesso será negado.

> Durante a execução do servidor proxy, você pode acompanhar as atividades no terminal do VS Code.

> O servidor imprimirá mensagens sobre as requisições recebidas e erros encontrados.
> Isso ajuda a monitorar e depurar o funcionamento do proxy.

	
#### Explicação do Código
##### Estrutura Principal
- Leitura de arquivos proibidos:
	- load_forbidden_domains(file_path) e load_forbidden_words(file_path) lêem os arquivos forbidden_domains.txt e forbidden_words.txt e retornam listas de domínios e palavras proibidas.
- Verificação de domínios e palavras proibidas:
	- is_domain_forbidden(host) verifica se o domínio está na lista de proibidos.
	- contains_forbidden_words(content) verifica se o conteúdo contém palavras proibidas.
- Manipulação de requisições HTTP e HTTPS:
	- cliente_handler(client_socket) lida com requisições HTTP, verifica e bloqueia domínios ou palavras proibidas, e encaminha as requisições para o servidor de destino.
	- cliente_https_connect(client_socket, url) lida com requisições HTTPS, estabelece uma conexão segura com o servidor de destino, e verifica e bloqueia domínios ou palavras proibidas.
- Execução do servidor proxy:
	- main() inicia o servidor proxy, escutando conexões na porta 8989.

#### Execução
1. O servidor proxy escuta conexões de clientes.
2. Quando uma conexão é recebida, uma nova thread é criada para lidar com a requisição.
3. A thread verifica se a requisição é HTTP ou HTTPS e a processa adequadamente.
4. Se o domínio ou conteúdo é proibido, uma resposta 403 Forbidden é enviada ao cliente.
5. Caso contrário, a requisição é encaminhada para o servidor de destino e a resposta é enviada de volta ao cliente.
