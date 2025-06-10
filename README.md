# 📦 PC-Estoque

## 📄 Descrição
O PC-Estoque é um sistema de gerenciamento de estoque desenvolvido para oferecer uma solução simples, prática e eficiente no controle de produtos disponíveis em marketplaces. A aplicação permite realizar o cadastro de produtos, controlar entradas e saídas de estoque, atualizar quantidades disponíveis e visualizar informações em tempo real — garantindo maior organização, segurança e agilidade nas operações comerciais.


## 👥 Equipe de Desenvolvimento

- Elbia Simone Buglio

- Fabio Romero

- Laura Gabriely

- Victor Teixeira


## ⚙️ Configuração do Ambiente Local

- Python 3.12
- FastAPI
- Uvicorn
- Make (para automação de tarefas no Linux)
- Outras dependências listadas em requirements

## 📦 Clonando o Repositório

git clone https://github.com/projeto-carreira-luizalabs-2025/pc-estoque/tree/v1

cd pc-estoque

## 📑 Configuração no Linux 🐧

Crie o ambiente virtual:
make build-venv

Ative o ambiente virtual:
source ./venv/bin/activate

Instale as dependências do projeto:
make requirements-dev

⚠️ A partir deste ponto, todos os comandos deverão ser executados dentro do ambiente virtual ativado.

## 📑 Configuração no Windows 🪟

### **📌 1️⃣ Instalar o make via MSYS2 (se ainda não instalado)**

- Baixe o instalador do MSYS2:
  
👉 https://www.msys2.org/
- Após instalar, abra o terminal MSYS2 MSYS e execute:
pacman -Syu

pacman -S make
- Depois de instalado, você poderá usar o make no terminal MSYS2 ou adicionar o caminho do make.exe no PATH para uso em outros terminais.

### **📌 2️⃣ Criar o ambiente virtual:**

python -m venv venv

**Ativar o ambiente virtual:**

venv\Scripts\activate

**Instalar as dependências do projeto:**

pip install -r requirements\develop.txt

📌 Obs: As dependências estão organizadas na pasta requirements

## 📌 Observações
Confirme a versão do Python instalada:

python --version
- No Linux, este projeto utiliza make para automação de tarefas.
- No Windows, os comandos são executados manualmente (a não ser que você instale o make via MSYS2 como descrito acima).
  
⚠️ Certifique-se de ativar o ambiente virtual antes de executar qualquer comando relacionado ao projeto.

## ▶️ Execução

**1️⃣ Configurar as variáveis de ambiente**

Copie o arquivo de variáveis de desenvolvimento:

- **Linux**
cp devtools/dotenv.dev .env
- **Windows**
copy devtools\dotenv.dev .env

**2️⃣ Subir a API**

Com o ambiente virtual ativado e as variáveis configuradas, execute:

make run-dev

ou, se preferir executar manualmente:

uvicorn app.api_main:app --reload

## 📖 Acesse a documentação interativa da API:

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc


## 🐳 Docker Compose

Para facilitar a configuração e execução do ambiente, este projeto também possui um arquivo docker-compose.yml que permite subir a aplicação e o SonarQube via containers Docker.

### 📑 docker-compose.yml

version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: devtools/Dockerfile
    container_name: pc-estoque
    ports:
      - "8000:8000"
    environment:
      - ENV=dev
    env_file:
      - devtools/dotenv.dev
    working_dir: /pc-estoque
    command: ["uvicorn", "app.api_main:app", "--host", "0.0.0.0", "--port", "8000"]
    restart: unless-stopped

  sonarqube:
    image: sonarqube:latest
    container_name: pc-sonarqube
    ports:
      - "9000:9000"
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_extensions:/opt/sonarqube/extensions
    restart: unless-stopped

volumes:
  sonarqube_data:
  sonarqube_logs:
  sonarqube_extensions:


### ▶️ Comandos Docker Compose

⚠️ Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

Subir todos os serviços (aplicação + SonarQube):

docker-compose up -d --build

Subir apenas o SonarQube:

docker-compose up -d sonarqube

Subir apenas a aplicação:

docker-compose up -d --build app

Parar todos os containers:

docker-compose stop

## 📬 Contribuições e Atualizações  

**Fluxo para contribuição:**

1. Realize um **fork** do repositório.
2. Crie uma **branch descritiva** para a sua feature ou correção.
3. Submeta via **Pull Request**.
4. Aguarde o **Code Review** pela equipe de desenvolvimento.
5. Após aprovação, a alteração será integrada ao código principal.
