"""
Script para executar o bot do Telegram para o PC-Estoque

Uso:
    python run_telegram_bot.py

Certifique-se de que a variável TELEGRAM_BOT_TOKEN está definida no arquivo .env
"""

import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from app.integrations.bots import telegram_bot as bot

load_dotenv()

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Token do Telegram não encontrado no arquivo .env")

    # Cria a aplicação do bot
    app = Application.builder().token(token).build()

    # Registra os comandos/handlers
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("help", bot.help_command))
    app.add_handler(CommandHandler("adicionar", bot.adicionar))

    # Inicia o polling (escutando os comandos)
    print("Bot Telegram rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()