# 📚 GerenciamentoLivros

Sistema para gerenciamento de livros, com backend em **FastAPI** (Python) e autenticação via **JWT** (access token + refresh token).

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Backend](#backend)
- [Frontend](#frontend)
- [Testando a API](#testando-a-api)
- [Debug](#debug)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Problemas comuns](#problemas-comuns)

---

## Pré-requisitos

Antes de começar, tenha instalado:

- [Python 3.11+](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/) com a extensão [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (necessária para o debug — veja a seção [Debug](#debug))
- [Bruno](https://www.usebruno.com/) ou [Postman](https://www.postman.com/) (opcional, para testar os endpoints — veja a seção [Testando a API](#testando-a-api))
- Git (opcional, para clonar o repositório)

---

## Backend

### 1. Configurar o banco de dados

Instale o MySQL e, em seguida, execute o script SQL localizado na pasta `dados/` para criar as tabelas necessárias.

### 2. Criar o arquivo `.env`

Na raiz do **backend**, crie um arquivo `.env` com as variáveis abaixo.

**Configurações do banco de dados:**

| Variável | Descrição |
|---|---|
| `DB_HOST` | Host do banco de dados |
| `DB_USER` | Usuário do banco de dados |
| `DB_PASSWORD` | Senha do banco de dados |
| `DB_DATABASE` | Nome da base de dados que será utilizada |

**Configurações de SMTP (envio de e-mail):**

Caso não tenha um servidor SMTP próprio, você pode usar as configurações de teste abaixo:

```env
MAIL_DEFAULT_SENDER=no-reply@test-p7kx4xwe3w2g9yjr.mlsender.net
MAIL_SERVER=smtp.mailersend.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=MS_0TNcZ8@test-p7kx4xwe3w2g9yjr.mlsender.net
MAIL_PASSWORD=mssp.7NaCz9V.7dnvo4dx9kng5r86.iOzTkqL
```

**Configurações de autenticação (JWT):**

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave usada para assinar/validar o access token |
| `ALGORITHM` | Algoritmo de criptografia utilizado (recomendado: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do access token, em minutos |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Tempo de expiração do refresh token, em dias |

> ⚠️ **Importante:** nunca versione o arquivo `.env` no Git. Adicione-o ao `.gitignore` e mantenha um `.env.example` (sem valores reais) para referência de quem for configurar o projeto. As credenciais de SMTP acima são de um servidor de teste — se este README for compartilhado publicamente, vale a pena rotacionar essa senha.

### 3. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Executar a aplicação

```bash
fastapi dev .\backend\app\main.py
```

A API estará disponível em `http://127.0.0.1:8000`, e a documentação interativa (Swagger) em `http://127.0.0.1:8000/docs`.

---

## Frontend

O frontend é uma aplicação Flask que consome a API do backend exclusivamente via HTTP — ele não acessa o banco de dados diretamente.

### 1. Criar o arquivo `.env`

Na raiz do **frontend**, crie um arquivo `.env` com as variáveis abaixo.

| Variável | Descrição |
|---|---|
| `BASE_URL_BACK` | URL base da API do backend (ex: `http://127.0.0.1:8000`) |
| `MARGEM_SEGURANCA_SEGUNDOS` | Margem de segurança (em segundos) para renovar o token antes dele expirar de fato |

Exemplo:
```env
BASE_URL_BACK=http://127.0.0.1:8000
MARGEM_SEGURANCA_SEGUNDOS=30
```

### 2. Executar a aplicação

```bash
python .\src\main.py
```

A aplicação estará disponível em `http://127.0.0.1:8080`.

---

## Testando a API

A pasta `client_rest/` contém uma coleção com todos os endpoints do backend, pronta pra testar sem precisar montar as requisições manualmente. Foi criada originalmente no **Bruno**, mas exportada num formato compatível também com o **Postman**.

### Bruno

1. Abra o Bruno
2. **Open Collection** → selecione a pasta `client_rest/`
3. As requisições já vêm organizadas por recurso (livros, usuários, auth, settings)
4. O `/auth/login` tem um script que captura o token da resposta e preenche automaticamente a variável usada pelos demais endpoints — basta rodar o login uma vez e seguir testando os endpoints protegidos sem precisar copiar/colar o token manualmente.

### Postman

1. Abra o Postman
2. **File → Import** → selecione a pasta `client_rest/` (ou o arquivo de coleção dentro dela)
3. O Postman importa as requisições preservando pastas e nomes
4. ⚠️ **O script de captura automática do token não é compatível com o Postman** — a sintaxe de scripts pós-resposta do Bruno (`bru`) é diferente da do Postman (`pm`). Depois de importar, é preciso reescrever esse script na aba **Tests** (ou **Post-response Scripts**, dependendo da versão) da requisição de login, algo como:
   ```javascript
   const response = pm.response.json();
   pm.environment.set("token", response.access_token);
   ```
   Sem esse ajuste, o token não é preenchido automaticamente no Postman — será necessário copiar o `access_token` da resposta do login e colar manualmente na variável de ambiente antes de testar os endpoints protegidos.

> Em ambas as ferramentas, lembre de rodar o `/auth/login` primeiro para obter o token, e configurar a variável de ambiente correspondente (ex: `token` ou `access_token`, conforme o nome usado nas requisições da coleção) antes de testar os endpoints protegidos.

---

## Debug

O projeto já tem uma configuração de debug pronta em `.vscode/launch.json`, cobrindo backend e frontend — inclusive rodando **os dois ao mesmo tempo**, cada um com sua própria sessão de debug (dá pra colocar breakpoint num controller do backend e num service do frontend simultaneamente).

### Configuração (`.vscode/launch.json`)

Se o arquivo ainda não existir no seu clone do projeto, crie-o com o conteúdo abaixo:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI: Debug",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload", "--port", "8000"],
      "cwd": "${workspaceFolder}/backend/app",
      "python": "${workspaceFolder}/.venv/Scripts/python.exe",
      "jinja": true,
      "justMyCode": true
    },
    {
      "name": "Flask: Debug",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/frontend/src/main.py",
      "cwd": "${workspaceFolder}/frontend/src",
      "python": "${workspaceFolder}/.venv/Scripts/python.exe",
      "jinja": true,
      "justMyCode": true
    }
  ],
  "compounds": [
    {
      "name": "Debug Backend + Frontend",
      "configurations": ["FastAPI: Debug", "Flask: Debug"],
      "stopAll": true
    }
  ]
}
```

> No Linux/macOS, troque `"python": "${workspaceFolder}/.venv/Scripts/python.exe"` por `"python": "${workspaceFolder}/.venv/bin/python"` (caminho do interpretador dentro da venv muda entre sistemas operacionais).

### Como debugar

1. Abra a pasta raiz do projeto no VS Code
2. Coloque breakpoints nos arquivos que quiser inspecionar (clique à esquerda do número da linha)
3. Vá na aba **Run and Debug** (`Ctrl+Shift+D`)
4. No dropdown do topo, selecione uma das opções:
   - **"FastAPI: Debug"** — roda só o backend
   - **"Flask: Debug"** — roda só o frontend
   - **"Debug Backend + Frontend"** — roda os dois juntos
5. Aperte `F5`

Quando a execução passar por um breakpoint, ela pausa e você pode inspecionar variáveis, avançar linha a linha (`F10`/`F11`) e usar o **Debug Console** para testar expressões na hora.

> Rodando o compound (**"Debug Backend + Frontend"**), `Shift+F5` encerra as duas aplicações de uma vez, graças ao `"stopAll": true`.

---

## Estrutura do projeto

```
GerenciamentoLivros/
├── .vscode/
│   └── launch.json          # configurações de debug (backend, frontend e ambos)
├── backend/
│   └── app/
│       ├── main.py
│       ├── config/          # configurações (settings, variáveis de ambiente)
│       ├── controllers/     # rotas/endpoints da API
│       ├── models/          # schemas Pydantic
│       ├── repositories/    # acesso ao banco de dados
│       └── database/        # conexão com o MySQL
├── dados/                   # scripts SQL de criação do banco
├── client_rest/             # coleção de requisições (Bruno, exportada também para Postman) usada para testar os endpoints do backend
├── frontend/
│   └── src/
│       ├── main.py
│       ├── routes/          # rotas Flask (ex: UsuarioRoute.py, PrincRoute.py)
│       ├── services/        # consumo da API do backend (ex: UsuarioServices.py, TokenServices.py)
│       └── model/           # schemas Pydantic usados no frontend (ex: UsuarioModel.py)
├── requirements.txt
└── .env                     # não versionado (um em backend/, outro em frontend/)
```

---

## Problemas comuns

**Erro ao ativar o ambiente virtual no PowerShell (`não é possível carregar o arquivo... políticas de execução`)**
Rode o PowerShell como administrador e execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Erro de conexão com o banco (`Access denied` ou `Can't connect to MySQL server`)**
Confira se o MySQL está rodando e se os dados em `DB_HOST`, `DB_USER`, `DB_PASSWORD` e `DB_DATABASE` no `.env` estão corretos.

**Endpoints protegidos retornando 401**
Verifique se você está enviando o header `Authorization: Bearer <token>` e se o access token não expirou. Se tiver expirado, use o endpoint `/auth/refresh` com o refresh token para obter um novo access token, sem precisar fazer login de novo.

**Rota `/algo/{id}` "roubando" uma rota mais específica (ex: `/algo/ativos`)**
No FastAPI, rotas são resolvidas na ordem em que são declaradas. Sempre declare rotas fixas (`/ativos`, `/me`, etc.) **antes** de rotas com parâmetro dinâmico (`/{id}`) que compartilhem o mesmo prefixo.

**Debug não inicia / erro `No module named 'uvicorn'` (ou similar) ao dar F5**
Confira se a chave `"python"` no `launch.json` está apontando para o interpretador correto dentro da `.venv` (veja a seção [Debug](#debug)), e se as dependências já foram instaladas nela (`pip install -r requirements.txt`).