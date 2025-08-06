# Etapa de build: cria o ambiente virtual e instala dependências
FROM python:3.12-slim AS build

WORKDIR /app

# Copia apenas os arquivos necessários para instalar dependências
COPY requirements.txt .
COPY requirements ./requirements/

# Instala git (necessário para algumas dependências)
RUN apt-get update && apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Cria o virtualenv e instala os pacotes
RUN python -m venv venv && \
    ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt && \
    ./venv/bin/pip install --no-cache-dir -r requirements/develop.txt

# Imagem final (produção)
FROM python:3.12-slim

WORKDIR /pc-estoque

# Instala apenas as dependências essenciais do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia o ambiente virtual do estágio anterior
COPY --from=build /app/venv /app/venv

# Copia o código da aplicação
COPY . .

# Compila os arquivos .py para melhor performance
RUN python -m compileall app

# Define o PATH para usar o venv copiado
ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONPATH="/pc-estoque"

# Cria usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /pc-estoque
USER appuser

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uvicorn", "app.api_main:app", "--host", "0.0.0.0", "--port", "8000"]
