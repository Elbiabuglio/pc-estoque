#!/usr/bin/env python3
"""
Bot simples para controle de estoque via Telegram
Execute este arquivo diretamente para iniciar o bot
"""
from app.integrations.bots.telegram_bot import (
    start,
    help_command,
    identificar,
    adicionar,
    consultar,
    atualizar,
    remover,
    estoque_baixo,
    listar,
    config
)
import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Importar comandos do bot


def main():
    """Função principal do bot"""
    # Token do bot
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not bot_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN não encontrado no arquivo .env")
        print("❌ TELEGRAM_BOT_TOKEN não encontrado no arquivo .env")
        return

    print("🤖 Inicializando bot do Telegram...")

    # Criar aplicação
    application = Application.builder().token(bot_token).build()

    # Registrar comandos
    handlers = [
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        CommandHandler("identificar", identificar),
        CommandHandler("adicionar", adicionar),
        CommandHandler("consultar", consultar),
        CommandHandler("atualizar", atualizar),
        CommandHandler("remover", remover),
        CommandHandler("estoque_baixo", estoque_baixo),
        CommandHandler("listar", listar),
        CommandHandler("config", config),
    ]

    for handler in handlers:
        application.add_handler(handler)

    print("✅ Bot configurado com sucesso!")
    print("📱 Comandos disponíveis: /start, /identificar, /help, /adicionar, /consultar, /atualizar, /remover, /estoque_baixo, /listar, /config")
    print("⏹️  Pressione Ctrl+C para parar")
    print("-" * 60)

    # Iniciar polling
    logger.info("Bot iniciado em modo polling...")
    application.run_polling(allowed_updates=['message'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n✅ Bot parado pelo usuário")
        logger.info("Bot parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")
        logger.error(f"Erro ao executar bot: {e}")
