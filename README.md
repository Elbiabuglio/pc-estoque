# 📦 PC-Estoque

## 📄 Descrição

O PC-Estoque é um sistema de gerenciamento de estoque desenvolvido para oferecer uma solução simples, prática e eficiente no controle de produtos disponíveis em marketplaces. A aplicação permite realizar o cadastro de produtos, controlar entradas e saídas de estoque, atualizar quantidades disponíveis e visualizar informações em tempo real garantindo maior organização, segurança e agilidade nas operações comerciais.

## 👥 Equipe de Desenvolvimento

- Elbia Simone Buglio
- Laura Gabriely
- Felipe Andrade

## 💻 Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias principais:

- **Python 3.12**
- **FastAPI**: Framework web para a construção de APIs.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **Redis**: Banco de dados não relacional utilizado como cache.
- **Alembic**: Ferramenta para gerenciamento de migrações de banco de dados.
- **Docker & Docker Compose**: Para containerização da aplicação e seus serviços.
- **Pytest**: Para a execução dos testes automatizados.
- **Keycloak**: Para gerenciamento de identidade e acesso.
- **SonarQube**: Para análise de qualidade do código.


## 🤖 Chatbot Web

O PC-Estoque conta com uma interface web de chatbot para facilitar a interação com o sistema de estoque de forma simples e intuitiva.


### Como acessar

Você pode rodar o Chatbot Web diretamente pelo terminal:

```bash
cd "app/integrations/chatbot"
python run_web.py
```


Depois, acesse [http://localhost:8081](http://localhost:8081) no navegador e clique em "Acessar Chat" para abrir a interface do assistente.

> **Importante:** Para acessar o sistema, é necessário se identificar usando o comando:
>
> ```
> identificar admin
> ```
>
> O ID `admin` é o seller_id padrão para testes e acesso completo.

### Principais comandos disponíveis

- `identificar [seller_id]` — Faz login no sistema 
- `adicionar` — Adiciona um novo produto
- `consultar` — Consulta um produto específico
- `atualizar` — Atualiza a quantidade de um produto
- `remover` — Remove um produto
- `listar` — Lista todos os produtos
- `estoque-baixo` — Mostra produtos com estoque crítico
- `historico` — Exibe o histórico de movimentações
- `logout` — Encerra a sessão

---

## **SUMARIO**

- [🚀 Como Rodar o Projeto](#🚀-como-rodar-o-projeto)
- [🧪 Testes e Qualidade de Código](#🧪-testes-e-qualidade-de-código)
- [🤖 Como Rodar o Telegram-bot](#🤖-como-rodar-o-telegram-bot)
- [📖 Documentação da API](#📖-documentação-da-api)

## 🚀 Como Rodar o Projeto

### **Pré-requisitos**

- Python 3.12
- Docker
- Docker Compose

### **Clonando o Repositório**

```bash
git clone https://github.com/Elbiabuglio/pc-estoque.git
cd pc-estoque
```

### **Configuração do Ambiente**

1.  **Crie o ambiente virtual:**

    ```bash
    # No Linux
    make build-venv

    # No Windows
    python -m venv venv
    ```

2.  **Ative o ambiente virtual:**

    ```bash
    #Linux
    source venv/bin/activate

    #Windows
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**

    ```bash
    # No Linux
    make requirements-dev

    # No Windows
    pip install -r requirements/develop.txt
    ```

4.  **Copie o arquivo de ambiente:** Este arquivo contém as configurações necessárias para a aplicação, como a URL do banco de dados.

    ```bash
    # No Linux
    chmod +x devtools/scripts/push-env
    make load-dev-env

    # No Windows
    cp ./devtools/dotenv.dev .env
    ```

### **Configurando Banco de Dados**

1. **Subindo o Container do PostgreSQL e Keycloak:** Este comando irá iniciar os contêineres da aplicação e do banco de dados PostgreSQL e o Keycloak, alem de realizar a migração do banco de dados e carregar o estoque inicial.

```bash
  # No Linux
  make docker-up

  # No Windows
  docker-compose up -d
```

**OBS: Comandos para descer os contêineres**

```bash
  # No Linux
  make docker-down

  # No Windows
  docker-compose down
```

3.  **Ajuste o arquivo `.env`:** Abra o arquivo `.env` recém-criado e altere a variável `APP_DB_URL` para apontar para o seu banco de dados PostgreSQL local. O formato é: `postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE_NAME`.

4.  **Aplique as migrações do banco de dados:** Para criar as tabelas necessárias, execute o Alembic.

    ```bash
    # No Linux
    make migration

    # No Windows
    alembic upgrade head
    ```

### **Executando a Aplicação**

Com o ambiente virtual ativado, inicie o servidor da API:

```bash
# No Linux
make run-dev

# No Windows
uvicorn app.api_main:app --reload
```

e o Worker para notificação de estoque baixo:

```bash
#No Linux
make notification

#No Windows
python -m app.worker.main
```

## 🤖 Como Rodar o Telegram-bot

- [Documentação do Telegram-bot](/devtools/bot/TELEGRAM_BOT_README.md)

### **Pré-requisitos**

- [Aplicação em execução](#🚀-Como-Rodar-o-Projeto)

### **Configurando o Telegram-bot**

1. **Criar um bot no Telegram:**

   - Converse com [@BotFather](https://t.me/BotFather) no Telegram
   - Use o comando `/newbot`
   - Escolha um nome e username para seu bot
   - Copie o token fornecido

2. **Configurar variáveis de ambiente:**

   Edite o arquivo `.env` e adicione seu token do bot:

   ```bash
   TELEGRAM_BOT_TOKEN=seu_token_aqui
   ```

3. **Executar o bot:**

   ```bash
   # No Linux
   make telegram

   # No Windows
   python bot_main.py
   ```

## 🧪 Testes e Qualidade de Código

O projeto está configurado com um conjunto de ferramentas para garantir a qualidade e a consistência do código.

### **Pré-requisitos**

- Python 3.12
- Docker
- Docker Compose

### **Clonando o Repositório**

```bash
git clone https://github.com/Elbiabuglio/pc-estoque.git
cd pc-estoque
```

### **Configuração do Ambiente**

1.  **Crie o ambiente virtual:**

    ```bash
    # No Linux
    make build-venv

    # No Windows
    python -m venv venv
    ```

2.  **Ative o ambiente virtual:**

    ```bash
    #Linux
    source venv/bin/activate

    #Windows
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**

    ```bash
    # No Linux
    make requirements-dev

    # No Windows
    pip install -r requirements.txt
    ```

4.  **Copie o arquivo de ambiente:** Este arquivo contém as configurações necessárias para a aplicação, como a URL do banco de dados.

    ```bash
    # No Linux
    chmod +x devtools/scripts/push-env
    make load-test-env

    # No Windows
    cp ./devtools/dotenv.test .env
    ```

5.  **Ajuste o arquivo `.env`:** Abra o arquivo `.env` recém-criado e altere a variável `APP_DB_URL` para apontar para o seu banco de dados PostgreSQL local. O formato é: `postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE_NAME`.

### **Executando os Testes**

Para rodar a suíte de testes unitários e de integração, utilize o Pytest:

```bash
# No Linux
make test

# No Windows
ENV=test PYTHONPATH=. pytest
```

Para gerar um relatório de cobertura de testes, execute:

```bash
# No Linux
make coverage

# No Windows
ENV=test PYTHONPATH=. pytest --cov=app --cov-report=term-missing --cov-report=xml tests --cov-fail-under=90 --durations=5
```

### **Análise com SonarQube**

O projeto está configurado para análise com o SonarQube.

1.  **Inicie o SonarQube:**

    ```bash
    docker-compose -f docker-compose-sonar.yml up -d
    ```

2- **Gerando o Arquivo coverage.xml:**

```bash
coverage xml
```

2.  **Execute o Scanner:** Após rodar os testes e gerar o `coverage.xml`, execute o scanner do Sonar para enviar os resultados para o servidor. Você precisará de um token de autenticação.
    ```bash
    docker run --rm \
     -e SONAR_HOST_URL=http://localhost:9000 \
     -e SONAR_TOKEN="SEU_TOKEN_AQUI" \
     -v "$(pwd)":/usr/src \
     sonarsource/sonar-scanner-cli
    ```


## 📚 Documentação da API do Chatbot Web

A API do Chatbot Web permite a integração e automação de interações com o assistente de estoque via requisições HTTP. Abaixo estão os principais endpoints disponíveis:

### Base URL

```
http://localhost:8081
```

### Endpoints

#### `POST /api/chat`

Envia uma mensagem para o chatbot e recebe a resposta.

**Request:**

```
POST /api/chat
Content-Type: application/json
```

**Body:**

```
{
  "message": "<mensagem>",
  "session_id": "<id_da_sessao>"
}
```

- `message` (string): Mensagem a ser enviada ao chatbot (ex: "listar").
- `session_id` (string, opcional): Identificador da sessão do usuário. Se não informado, uma nova sessão será criada.

**Response:**

```
{
  "response": "<resposta_do_chatbot>",
  "session_id": "<id_da_sessao>"
}
```

- `response` (string): Resposta do chatbot.
- `session_id` (string): Identificador da sessão (use este valor para manter o contexto em conversas futuras).

**Exemplo de requisição usando curl:**

```bash
curl -X POST http://localhost:8081/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "listar"}'
```

#### `GET /api/health`

Verifica se o serviço do Chatbot Web está online.

**Request:**

```
GET /api/health
```

**Response:**

```
{
  "status": "ok"
}
```

---

## 📖 Documentação da API

Após iniciar a aplicação (localmente ou com Docker), você pode acessar a documentação interativa da API nos seguintes endereços:

- **Swagger UI:** [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- **ReDoc:** [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

## 📫 Contribuições

O projeto está aberto a contribuições. O fluxo para contribuição é o seguinte:

1.  Realize um **fork** do repositório.
2.  Crie uma **branch** descritiva para a sua feature ou correção.
3.  Submeta um **Pull Request**.
4.  Aguarde o **Code Review** pela equipe de desenvolvimento.
5.  Após a aprovação, sua alteração será integrada ao código principal.
