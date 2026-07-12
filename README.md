# GerenciamentoLivros
Sistema para gerenciamento de livros

Siga os passos abaixo para executar a aplicação

1- Para poder executar a aplicaçao é necessário instalar o MySql. Após a instalação do MySql executar o script que se encontra na pasta "src\dados".

2- Crie o arquivo .env e preencha as configurações do banco de dados

DB_HOST => Host do banco
DB_USER => Usuário do banco de dados
DB_PASSWORD => Senha do banco de dados
DB_DATABASE => Base que será utilizada

3- Configure o servidor de SMTP no arquivo .env. Caso não tenha um servidor utilizar as seguintes configurações:

MAIL_DEFAULT_SENDER=no-reply@test-p7kx4xwe3w2g9yjr.mlsender.net
MAIL_SERVER=smtp.mailersend.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=MS_0TNcZ8@test-p7kx4xwe3w2g9yjr.mlsender.net
MAIL_PASSWORD=mssp.7NaCz9V.7dnvo4dx9kng5r86.iOzTkqL

4- Crie o ambiente virtual do python rodando o seguinte comando:
    >> python -m venv .venv
    
5- Ativar o ambiente virtual executando o Script abaixo
    >> .\.venv\Scripts\Activate.ps1

6- Instale as bibliotecas utilizadas no projeto rodando o comando abaixo:
    >> pip install -r requirements.txt

7- Execute a aplicação rodando o seguinte comando:
    >> python .\src\main.py
