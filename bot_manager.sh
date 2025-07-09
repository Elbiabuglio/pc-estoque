#!/bin/bash

# Script para facilitar o desenvolvimento do bot

echo "🤖 Bot do Telegram - PC Estoque"
echo "================================"

# Função para mostrar o menu
show_menu() {
    echo ""
    echo "Escolha uma opção:"
    echo "1. Executar o bot"
    echo "2. Instalar dependências"
    echo "3. Verificar configurações"
    echo "4. Executar testes"
    echo "5. Sair"
    echo ""
}

# Função para instalar dependências
install_deps() {
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
    echo "✅ Dependências instaladas!"
}

# Função para verificar configurações
check_config() {
    echo "🔍 Verificando configurações..."
    
    if [ ! -f ".env" ]; then
        echo "❌ Arquivo .env não encontrado!"
        echo "📝 Criando arquivo .env a partir do exemplo..."
        cp .env.example .env
        echo "✅ Arquivo .env criado! Edite-o com suas configurações."
        return 1
    fi
    
    if ! grep -q "TELEGRAM_BOT_TOKEN=" .env; then
        echo "❌ TELEGRAM_BOT_TOKEN não encontrado no .env"
        return 1
    fi
    
    token=$(grep "TELEGRAM_BOT_TOKEN=" .env | cut -d '=' -f2)
    if [ "$token" = "SEU_TOKEN_DO_BOT_AQUI" ] || [ -z "$token" ]; then
        echo "❌ Token do bot não configurado no .env"
        echo "📖 Configure o TELEGRAM_BOT_TOKEN no arquivo .env"
        return 1
    fi
    
    echo "✅ Configurações OK!"
    return 0
}

# Função para executar o bot
run_bot() {
    echo "🚀 Iniciando o bot..."
    if check_config; then
        python telegram_bot_main.py
    else
        echo "❌ Configure o bot antes de executar!"
    fi
}

# Função para executar testes
run_tests() {
    echo "🧪 Executando testes..."
    pytest tests/ -v
}

# Loop principal
while true; do
    show_menu
    read -p "Digite sua opção: " choice
    
    case $choice in
        1)
            run_bot
            ;;
        2)
            install_deps
            ;;
        3)
            check_config
            ;;
        4)
            run_tests
            ;;
        5)
            echo "👋 Até logo!"
            exit 0
            ;;
        *)
            echo "❌ Opção inválida!"
            ;;
    esac
    
    read -p "Pressione Enter para continuar..."
done
