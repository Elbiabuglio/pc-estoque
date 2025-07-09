# 📦 PC-Estoque

## 📄 Descrição

O PC-Estoque é um sistema de gerenciamento de estoque desenvolvido para oferecer uma solução simples, prática e eficiente no controle de produtos disponíveis em marketplaces. A aplicação permite realizar o cadastro de produtos, controlar entradas e saídas de estoque, atualizar quantidades disponíveis e visualizar informações em tempo real — garantindo maior organização, segurança e agilidade nas operações comerciais.

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
git clone https://github.com/projeto-carreira-luizalabs-2025/pc-estoque.git
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
git clone https://github.com/projeto-carreira-luizalabs-2025/pc-estoque.git
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
