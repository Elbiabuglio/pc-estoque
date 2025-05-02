📦 PC-Estoque

📄 Descrição

O PC-Estoque é um sistema de gerenciamento de estoque desenvolvido para oferecer uma solução simples, prática e eficiente no controle de produtos disponíveis em marketplaces. A aplicação permite realizar o cadastro de produtos, controlar entradas e saídas de estoque, atualizar quantidades disponíveis e visualizar informações em tempo real — garantindo maior organização, segurança e agilidade nas operações comerciais.

👥 Equipe de Desenvolvimento

- Elbia Simone Buglio

- Fabio Romero

- Laura Gabriely

- Victor Teixeira

#

⚙️ Configuração do Ambiente Local
Este projeto foi desenvolvido utilizando Python 3.12. Antes de iniciar, confirme se essa versão está instalada em sua máquina.

📦 Clonando o Repositório

git clone <https://github.com/projeto-carreira-luizalabs-2025/pc-estoque/tree/v1>

```sh
cd pc-estoque
```

📑 Configuração no Linux 🐧

Crie o ambiente virtual:

```sh
make build-venv
```

Ative o ambiente virtual:

```sh
source ./venv/bin/activate
```

Instale as dependências do projeto:

```sh
make requirements-dev
```

⚠️ A partir deste ponto, todos os comandos deverão ser executados dentro do ambiente virtual ativado.

📑 Configuração no Windows 🪟

Crie o ambiente virtual:

```
python -m venv venv
```

Ative o ambiente virtual:

```
venv\Scripts\activate
```

⚠️ A partir deste ponto, todos os comandos deverão ser executados dentro do ambiente virtual ativado.

Instale as dependências do projeto:

```sh
pip install -r requirements.txt
```

Crie o arquivo .env na raiz do projeto com o seguinte conteudo:

```sh
ENV=dev
```

Comando para subir a API:

```sh
uvicorn app.api_main:app --reload
```

📌 Observações
Confirme a versão do Python instalada:

```sh
python --version
```

No Linux, este projeto utiliza make para automação de tarefas.
No Windows, os comandos são executados manualmente.

Certifique-se de ativar o ambiente virtual antes de executar qualquer comando relacionado ao projeto.
