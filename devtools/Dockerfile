# PRimeira etapa: instalar os pacotes do Python
# Monstar a estrutura de arquivos da aplicacão

# --- ESTÁGIO DE CONSTRUÇÃO ---
# Objetivo: Instalar dependências em um ambiente temporário.
FROM python:3.12-slim AS construtor

# Define o shell para garantir que os comandos funcionem corretamente
SHELL ["/bin/bash", "-c"]

# Define o diretório de trabalho no container
WORKDIR /PC-Estoque

# Copia os requirements para o container
COPY requirements ./requirements

# Atualiza o pip e instala as dependências de desenvolvimento
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/base.txt

# Define a variável de ambiente para o Python encontrar os módulos
ENV PYTHONPATH=/PC-Estoque

# Copia o código da aplicação
COPY app /PC-Estoque/app

# Copia o arquivo de requirements base
COPY requirements/base.txt .

# Copia o arquivo de variáveis de ambiente
COPY devtools/dotenv.dev ./.env

# Compila os arquivos Python para bytecode (.pyc) para melhor desempenho
RUN python -m compileall app

# Expõe a porta que o Uvicorn irá utilizar.
EXPOSE 8000

# Comando para rodar a aplicaçãotainer.
CMD ["uvicorn", "app.main_api:app", "--host", "0.0.0.0", "--port", "8000"]

# Se quiser versionar:r
    #docker build -t pc-estoque .
    #docker run -p 8000:8000 pc-estoque:0.0.1
