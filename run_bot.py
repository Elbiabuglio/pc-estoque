#!/usr/bin/env python3
"""
Script para executar o bot do Telegram de forma simplificada
"""
from app.integrations.bots.telegram_bot_main import main
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))


if __name__ == "__main__":
    print("🤖 Iniciando bot do Telegram para controle de estoque...")
    print("💡 Pressione Ctrl+C para parar o bot")
    print("-" * 50)

    try:
        main()
    except KeyboardInterrupt:
        print("\n✅ Bot parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)
