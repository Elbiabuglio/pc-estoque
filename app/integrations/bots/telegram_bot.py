import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from app.models.estoque_model import Estoque
from app.container import Container
from app.settings import settings

load_dotenv()

# Dicionário para armazenar sellers autenticados por chat_id
authenticated_sellers = {}

# Helper function para configurar o container


def get_configured_container():
    """Retorna um container configurado com as variáveis de ambiente"""
    container = Container()
    container.config.from_dict({
        "app_db_url": str(settings.app_db_url),
        "app_redis_url": str(settings.app_redis_url),
        "app_openid_wellknown": str(settings.app_openid_wellknown)
    })
    return container


def get_user_seller(chat_id: int) -> str | None:
    """Retorna o seller_id do usuário autenticado"""
    return authenticated_sellers.get(chat_id)


def is_authenticated(chat_id: int) -> bool:
    """Verifica se o usuário está autenticado"""
    return chat_id in authenticated_sellers


def authenticate_user(chat_id: int, seller_id: str):
    """Autentica um usuário com um seller_id"""
    authenticated_sellers[chat_id] = seller_id


def require_authentication(func):
    """Decorator para exigir autenticação antes de executar comando"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        if not is_authenticated(chat_id):
            await update.message.reply_text(
                "🔒 Você precisa se identificar primeiro!\n"
                "Use: /identificar <seu_seller_id>"
            )
            return
        return await func(update, context)
    return wrapper

# Comando /start


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or "usuário"

    if is_authenticated(chat_id):
        seller_id = get_user_seller(chat_id)
        await update.message.reply_text(
            f"👋 Olá {user_name}!\n"
            f"Você já está identificado como seller: `{seller_id}`\n\n"
            f"Use /help para ver os comandos disponíveis."
        )
    else:
        await update.message.reply_text(
            f"👋 Olá {user_name}! Bem-vindo ao PC-Estoque Bot!\n\n"
            f"🔐 Para começar, você precisa se identificar:\n"
            f"Use: `/identificar <seu_seller_id>`\n\n"
            f"Exemplo: `/identificar luizaLabs`\n\n"
            f"Após se identificar, você poderá gerenciar seu estoque!"
        )

# Comando /identificar


async def identificar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text(
                "❌ Uso correto: `/identificar <seu_seller_id>`\n"
                "Exemplo: `/identificar luizaLabs`"
            )
            return

        seller_id = args[0].strip()
        chat_id = update.effective_chat.id
        user_name = update.effective_user.first_name or "usuário"

        # Validar se seller_id não está vazio
        if not seller_id:
            await update.message.reply_text("❌ Seller ID não pode estar vazio!")
            return

        # Autenticar o usuário
        authenticate_user(chat_id, seller_id)

        await update.message.reply_text(
            f"✅ Olá {user_name}!\n"
            f"Você foi identificado como seller: `{seller_id}`\n\n"
            f"🎯 Agora você pode usar todos os comandos.\n"
            f"📦 Todas as operações serão feitas no seu estoque.\n\n"
            f"Use /help para ver os comandos disponíveis!"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao se identificar: {str(e)}")

# Comando /help


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📋 **Comandos disponíveis:**

🔐 **Identificação:**
/start - Inicia o bot
/identificar <seller_id> - Se identifica como seller
/help - Mostra esta ajuda

📦 **Gestão de Estoque:**
/adicionar <sku> <quantidade> - Adiciona produto ao estoque
/consultar <sku> - Consulta quantidade de um produto
/atualizar <sku> <quantidade> - Define quantidade exata do produto
/remover <sku> - Remove produto do estoque

📊 **Relatórios:**
/estoque_baixo - Lista produtos com estoque baixo (≤ 15 unidades)
/listar - Lista seus produtos no estoque
/config - Mostra configurações do sistema

💡 **Dica:** Todas as operações são feitas apenas no seu estoque!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


@require_authentication
async def adicionar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Uso: /adicionar <sku> <quantidade>")
            return

        sku, quantidade = args
        quantidade = int(quantidade)

        # Validar quantidade
        if quantidade <= 0:
            await update.message.reply_text("❌ A quantidade deve ser maior que zero!")
            return

        # Pegar o seller_id do usuário autenticado
        chat_id = update.effective_chat.id
        seller_id = get_user_seller(chat_id)

        container = get_configured_container()
        estoque_service = container.estoque_service()

        # Verifica se o produto já existe
        try:
            estoque_existente = await estoque_service.get_by_seller_id_and_sku(seller_id, sku)
            # Se existe, atualiza a quantidade (incrementa)
            nova_quantidade = estoque_existente.quantidade + quantidade
            await estoque_service.update(seller_id, sku, nova_quantidade)
            await update.message.reply_text(
                f"✅ Produto {sku} atualizado! Quantidade anterior: {estoque_existente.quantidade}, "
                f"Nova quantidade: {nova_quantidade} (incremento: +{quantidade})"
            )
        except Exception:
            # Se não existe, cria um novo
            novo_estoque = Estoque(seller_id=seller_id,
                                   sku=sku, quantidade=quantidade)
            await estoque_service.create(novo_estoque)
            await update.message.reply_text(f"✅ Produto {sku} adicionado ao estoque do seller {seller_id} com quantidade {quantidade}.")

    except ValueError:
        await update.message.reply_text("❌ Quantidade deve ser um número inteiro.")
    except Exception as e:
        error_message = str(e)

        # Tratar erros específicos de validação
        if "quantidade deve ser maior que zero" in error_message:
            await update.message.reply_text("❌ A quantidade deve ser maior que zero!")
        elif "estoque_invalido" in error_message:
            await update.message.reply_text("❌ Quantidade inválida. Deve ser um número positivo!")
        else:
            await update.message.reply_text(f"❌ Erro ao adicionar produto: {error_message}")

# Comando /consultar


@require_authentication
async def consultar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Uso: /consultar <sku>")
            return

        sku = args[0]

        # Pegar o seller_id do usuário autenticado
        chat_id = update.effective_chat.id
        seller_id = get_user_seller(chat_id)

        container = get_configured_container()
        estoque_service = container.estoque_service()

        estoque = await estoque_service.get_by_seller_id_and_sku(seller_id, sku)
        await update.message.reply_text(
            f"📦 Produto: {sku}\n"
            f"🏪 Seller: {seller_id}\n"
            f"📊 Quantidade: {estoque.quantidade}\n"
            f"📅 Última atualização: {estoque.updated_at}"
        )
    except Exception as e:
        error_message = str(e)
        
        # Tratar erro específico de produto não encontrado
        if "404" in error_message and "estoque_nao_encontrado" in error_message:
            # Extrair o SKU do contexto do erro se possível
            import re
            sku_match = re.search(r"'sku': '([^']+)'", error_message)
            sku_name = sku_match.group(1) if sku_match else sku
            await update.message.reply_text(f"❌ Produto '{sku_name}' não encontrado no seu estoque!")
        elif "404" in error_message or "não encontrado" in error_message.lower():
            await update.message.reply_text(f"❌ Produto '{sku}' não encontrado no seu estoque!")
        else:
            await update.message.reply_text(f"❌ Erro ao consultar produto: {error_message}")

# Comando atualizar


@require_authentication
async def atualizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Uso: /atualizar <sku> <quantidade>")
            return

        sku, quantidade = args
        quantidade = int(quantidade)

        # Validar quantidade
        if quantidade <= 0:
            await update.message.reply_text("❌ A quantidade deve ser maior que zero!")
            return

        # Pegar o seller_id do usuário autenticado
        chat_id = update.effective_chat.id
        seller_id = get_user_seller(chat_id)

        container = get_configured_container()
        estoque_service = container.estoque_service()

        estoque_anterior = await estoque_service.get_by_seller_id_and_sku(seller_id, sku)
        await estoque_service.update(seller_id, sku, quantidade)

        await update.message.reply_text(
            f"✅ Produto {sku} atualizado!\n"
            f"Quantidade anterior: {estoque_anterior.quantidade}\n"
            f"Nova quantidade: {quantidade}"
        )
    except ValueError:
        await update.message.reply_text("❌ Quantidade deve ser um número inteiro.")
    except Exception as e:
        error_message = str(e)

        # Tratar erros específicos de validação
        if "quantidade deve ser maior que zero" in error_message:
            await update.message.reply_text("❌ A quantidade deve ser maior que zero!")
        elif "estoque_invalido" in error_message:
            await update.message.reply_text("❌ Quantidade inválida. Deve ser um número positivo!")
        elif "404" in error_message or "não encontrado" in error_message.lower():
            await update.message.reply_text(f"❌ Produto {sku} não encontrado no seu estoque!")
        else:
            await update.message.reply_text(f"❌ Erro ao atualizar produto: {error_message}")

# Comando /remover


@require_authentication
async def remover(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Uso: /remover <sku>")
            return

        sku = args[0]

        # Pegar o seller_id do usuário autenticado
        chat_id = update.effective_chat.id
        seller_id = get_user_seller(chat_id)

        container = get_configured_container()
        estoque_service = container.estoque_service()

        # Verifica se o produto existe antes de remover
        estoque = await estoque_service.get_by_seller_id_and_sku(seller_id, sku)
        await estoque_service.delete(seller_id, sku)

        await update.message.reply_text(f"✅ Produto {sku} removido do estoque!")
    except Exception as e:
        error_message = str(e)
        
        # Tratar erro específico de produto não encontrado
        if "404" in error_message and "estoque_nao_encontrado" in error_message:
            # Extrair o SKU do contexto do erro se possível
            import re
            sku_match = re.search(r"'sku': '([^']+)'", error_message)
            sku_name = sku_match.group(1) if sku_match else sku
            await update.message.reply_text(f"❌ Produto '{sku_name}' não encontrado no seu estoque!")
        elif "404" in error_message or "não encontrado" in error_message.lower():
            await update.message.reply_text(f"❌ Produto '{sku}' não encontrado no seu estoque!")
        else:
            await update.message.reply_text(f"❌ Erro ao remover produto: {error_message}")

# Comando /estoque_baixo


@require_authentication
async def estoque_baixo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Pegar o seller_id do usuário autenticado
        chat_id = update.effective_chat.id
        seller_id = get_user_seller(chat_id)

        container = get_configured_container()
        estoque_service = container.estoque_service()

        # Lista produtos com estoque baixo do seller
        # Usar o threshold configurado nas settings
        produtos_baixo = await estoque_service.repository.find_all_below_threshold(settings.low_stock_threshold)

        # Filtrar apenas produtos do seller autenticado
        produtos_do_seller = [
            p for p in produtos_baixo if p.seller_id == seller_id]

        if not produtos_do_seller:
            await update.message.reply_text("✅ Nenhum produto seu com estoque baixo encontrado!")
            return

        message = "⚠️ *Seus produtos com estoque baixo:*\n\n"
        for produto in produtos_do_seller:
            message += f"📦 SKU: `{produto.sku}`\n"
            message += f"📊 Quantidade: {produto.quantidade}\n"
            message += f"📅 Atualizado: {produto.updated_at.strftime('%d/%m/%Y %H:%M')}\n\n"

        await update.message.reply_text(message, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao consultar estoque baixo: {str(e)}")

# Comando /listar


@require_authentication
async def listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Pegar o seller_id do usuário autenticado
        chat_id = update.effective_chat.id
        seller_id = get_user_seller(chat_id)

        container = get_configured_container()
        estoque_service = container.estoque_service()

        # Lista produtos do seller específico
        await update.message.reply_text(f"🔍 Buscando seus produtos...")

        # Usar consulta SQL direta para buscar produtos do seller
        async with estoque_service.repository.sql_client.make_session() as session:
            from sqlalchemy import select
            stmt = select(estoque_service.repository.entity_base_class).where(
                estoque_service.repository.entity_base_class.seller_id == seller_id
            ).limit(20)
            result = await session.execute(stmt)
            entities = result.scalars().all()
            produtos = [estoque_service.repository.model_class.model_validate(
                entity) for entity in entities]

        if not produtos:
            await update.message.reply_text("❌ Você não possui produtos cadastrados no estoque")
            return

        message = f"📋 *Seus produtos no estoque:*\n\n"

        for produto in produtos:
            message += f"📦 SKU: `{produto.sku}`\n"
            message += f"📊 Quantidade: {produto.quantidade}\n"
            message += f"📅 Atualizado: {produto.updated_at.strftime('%d/%m/%Y %H:%M')}\n\n"

        await update.message.reply_text(message, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao listar produtos: {str(e)}")

# Comando /config


@require_authentication
async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra as configurações atuais do sistema"""
    try:
        await update.message.reply_text(
            f"⚙️ **Configurações do Sistema:**\n\n"
            f"📊 Limite de estoque baixo: **{settings.low_stock_threshold} unidades**\n"
            f"📱 Versão do sistema: **{settings.version}**\n"
            f"🏪 Nome da aplicação: **{settings.app_name}**\n\n"
            f"💡 Produtos com quantidade ≤ {settings.low_stock_threshold} são considerados estoque baixo.",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao mostrar configurações: {str(e)}")

# Função para tratar callbacks dos botões do menu


async def handle_help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trata os callbacks dos botões do menu de ajuda"""
    query = update.callback_query
    await query.answer()

    callback_data = query.data

    help_responses = {
        "help_identificar": """
🆔 **Comando: /identificar**

**Uso:** `/identificar <seu_seller_id>`

**Exemplo:** `/identificar luizaLabs`

**Descrição:** 
Este comando permite que você se identifique no sistema. Após a identificação, todas as operações de estoque serão feitas apenas para o seu seller.

**⚠️ Importante:** Você deve se identificar antes de usar qualquer outro comando!
""",

        "help_adicionar": """
➕ **Comando: /adicionar**

**Uso:** `/adicionar <sku> <quantidade>`

**Exemplos:** 
• `/adicionar ABC123 50` - Adiciona 50 unidades do produto ABC123
• `/adicionar NOTEBOOK-DELL 10` - Adiciona 10 notebooks Dell

**Comportamento:**
• Se o produto já existe: **incrementa** a quantidade
• Se é um produto novo: **cria** no estoque

**⚠️ Importante:** A quantidade deve ser maior que zero!
""",

        "help_consultar": """
🔍 **Comando: /consultar**

**Uso:** `/consultar <sku>`

**Exemplos:** 
• `/consultar ABC123` - Consulta o produto ABC123
• `/consultar NOTEBOOK-DELL` - Consulta notebooks Dell

**Retorna:**
• Quantidade atual
• Seller responsável
• Data da última atualização
""",

        "help_atualizar": """
✏️ **Comando: /atualizar**

**Uso:** `/atualizar <sku> <quantidade>`

**Exemplos:** 
• `/atualizar ABC123 25` - Define quantidade como 25
• `/atualizar NOTEBOOK-DELL 5` - Define quantidade como 5

**⚠️ Importante:** 
• Define a quantidade **exata** (não incrementa)
• A quantidade deve ser maior que zero!
• O produto deve existir no seu estoque
""",

        "help_remover": """
🗑️ **Comando: /remover**

**Uso:** `/remover <sku>`

**Exemplos:** 
• `/remover ABC123` - Remove o produto ABC123
• `/remover NOTEBOOK-DELL` - Remove notebooks Dell

**⚠️ Atenção:** 
• Remove **completamente** o produto do estoque
• Esta ação não pode ser desfeita!
• O produto deve existir no seu estoque
""",

        "help_estoque_baixo": f"""
⚠️ **Comando: /estoque_baixo**

**Uso:** `/estoque_baixo`

**Descrição:** 
Lista todos os seus produtos com estoque baixo (≤ {settings.low_stock_threshold} unidades).

**Retorna:**
• SKU do produto
• Quantidade atual
• Data da última atualização

**💡 Dica:** Use este comando regularmente para controlar seu estoque!
""",

        "help_listar": """
📋 **Comando: /listar**

**Uso:** `/listar`

**Descrição:** 
Lista todos os seus produtos cadastrados no estoque (máximo 20 produtos).

**Retorna:**
• SKU de cada produto
• Quantidade atual
• Data da última atualização

**💡 Dica:** Use para ter uma visão geral do seu estoque!
""",

        "help_config": """
⚙️ **Comando: /config**

**Uso:** `/config`

**Descrição:** 
Mostra as configurações atuais do sistema.

**Retorna:**
• Limite de estoque baixo
• Versão do sistema
• Nome da aplicação

**💡 Útil para:** Saber qual o limite considerado "estoque baixo"
""",

        "help_exemplos": """
💡 **Exemplos Práticos de Uso:**

**🎯 Cenário 1: Novo Produto**
1. `/adicionar MOUSE-GAMER 100` → Adiciona 100 mouses
2. `/consultar MOUSE-GAMER` → Verifica se foi adicionado
3. `/atualizar MOUSE-GAMER 80` → Ajusta para 80 unidades

**🎯 Cenário 2: Controle Diário**
1. `/listar` → Ver todos os produtos
2. `/estoque_baixo` → Verificar produtos em falta
3. `/adicionar TECLADO-RGB 50` → Repor estoque

**🎯 Cenário 3: Produto Descontinuado**
1. `/consultar PRODUTO-ANTIGO` → Ver quantidade atual
2. `/remover PRODUTO-ANTIGO` → Remover do estoque

**💡 Dica:** Sempre use `/estoque_baixo` para monitorar!
"""
    }

    response = help_responses.get(callback_data, "❌ Opção não encontrada!")

    await query.edit_message_text(
        text=response,
        parse_mode='Markdown'
    )
