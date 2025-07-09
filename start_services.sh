#!/bin/bash
echo "🚀 Iniciando serviços do PC-Estoque Bot..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker primeiro."
    exit 1
fi

# Iniciar PostgreSQL e Redis
echo "📦 Iniciando PostgreSQL e Redis..."
docker-compose up -d

# Aguardar os serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 10

# Verificar se os serviços estão rodando
if docker ps | grep -q "pc-postgres"; then
    echo "✅ PostgreSQL iniciado com sucesso"
else
    echo "❌ Falha ao iniciar PostgreSQL"
fi

if docker ps | grep -q "redis"; then
    echo "✅ Redis iniciado com sucesso"
else
    echo "❌ Falha ao iniciar Redis"
fi

echo ""
echo "🤖 Agora você pode executar o bot:"
echo "python bot_simples.py"
echo ""
echo "📱 Use /start e depois /identificar seu_seller_id para começar"
