import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from app.models.estoque_model import Estoque
from app.container import Container

load_dotenv()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oi, Elbia! Seu bot está funcionando!")

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Comandos disponíveis:
/start - Inicia o bot
/help - Mostra esta ajuda
/adicionar <seller_id> <sku> <quantidade> - Adiciona produto ao estoque
"""
    await update.message.reply_text(help_text)

# Comando /adicionar
async def adicionar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text("Uso: /adicionar <seller_id> <sku> <quantidade>")
            return

        seller_id, sku, quantidade = args
        quantidade = int(quantidade)

        container = Container()
        estoque_service = container.estoque_service()

        estoque_service.adicionar(seller_id, sku, quantidade)

        await update.message.reply_text(f"✅ Produto {sku} adicionado ao estoque do seller {seller_id} com quantidade {quantidade}.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao adicionar produto: {str(e)}")