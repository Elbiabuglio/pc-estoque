# Bot do Telegram para Controle de Estoque

Este bot permite gerenciar o estoque através do Telegram.

## Configuração

1. **Criar um bot no Telegram:**
   - Converse com [@BotFather](https://t.me/BotFather) no Telegram
   - Use o comando `/newbot`
   - Escolha um nome e username para seu bot
   - Copie o token fornecido

2. **Configurar variáveis de ambiente:**
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` e adicione seu token do bot:
   ```
   TELEGRAM_BOT_TOKEN=seu_token_aqui
   ```

3. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Iniciar os serviços de banco (PostgreSQL e Redis):**
   ```bash
   # No Windows
   start_services.bat
   
   # No Linux/Mac
   ./start_services.sh
   
   # Ou manualmente com Docker Compose
   docker-compose up -d
   ```

5. **Executar o bot:**
   ```bash
   # Versão simples (recomendada)
   python bot_simples.py
   
   # Ou versão principal
   python telegram_bot_main.py
   ```

## Comandos Disponíveis

### 🔐 Identificação (Obrigatório)
- `/start` - Inicia o bot e mostra instruções
- `/identificar <seller_id>` - Se identifica como seller (ex: `/identificar luizaLabs`)
- `/help` - Mostra lista de comandos

### 📦 Gestão de Estoque (Após identificação)
- `/adicionar <sku> <quantidade>` - Adiciona/incrementa produto no seu estoque
- `/consultar <sku>` - Consulta quantidade de um produto seu
- `/atualizar <sku> <quantidade>` - Define quantidade exata do produto
- `/remover <sku>` - Remove produto do seu estoque

### 📊 Relatórios (Apenas seus produtos)
- `/estoque_baixo` - Lista seus produtos com estoque baixo (≤ 15 unidades)
- `/listar` - Lista todos os seus produtos no estoque
- `/config` - Mostra configurações do sistema (limite de estoque baixo, versão, etc.)

**⚠️ Importante:** Após se identificar, todas as operações são feitas apenas no seu estoque. Você não pode ver ou modificar produtos de outros sellers.

## Exemplos de Uso

### 🔐 Primeiro acesso
```
/start
/identificar luizaLabs
```

### 📦 Gerenciando estoque
```
/adicionar PRODUTO123 50
/consultar PRODUTO123
/atualizar PRODUTO123 100
/remover PRODUTO123
```

### 📊 Relatórios
```
/listar
/estoque_baixo
/config
```

## Funcionalidades

- **🔐 Sistema de Identificação**: Cada usuário se identifica com seu seller_id único
- **🛡️ Isolamento por Seller**: Cada seller só pode ver e modificar seus próprios produtos
- **📦 Gestão Completa**: Adicionar, consultar, atualizar e remover produtos
- **📊 Relatórios Personalizados**: Estoque baixo e listagem apenas dos seus produtos
- **✅ Validações**: Verifica parâmetros e permissões antes de executar operações
- **🔧 Diagnóstico**: Comando para verificar se o sistema está funcionando
- **💾 Persistência**: Dados salvos em PostgreSQL com histórico de movimentações

## ⚙️ Configurações do Sistema

### Estoque Baixo
- **Limite padrão**: 15 unidades ou menos
- **Configurável**: Pode ser alterado no arquivo `app/settings/app.py`
- **Campo**: `low_stock_threshold`
- **Verificação**: Use `/config` para ver o valor atual

### Como alterar o limite:
1. Edite `app/settings/app.py`
2. Altere a linha: `low_stock_threshold: int = Field(default=15, ...)`
3. Reinicie o bot

## 🔒 Segurança e Isolamento

### Proteção por Seller
- ✅ **Identificação obrigatória** antes de usar qualquer comando
- ✅ **Isolamento total** - sellers só veem seus próprios produtos
- ✅ **Validação automática** - sistema impede acesso cruzado
- ✅ **Sessão por chat** - cada conversa tem sua própria identificação

### Como funciona:
1. **Primeiro acesso**: Usuario deve usar `/identificar seller_id`
2. **Comandos protegidos**: Todos os comandos de estoque verificam autenticação
3. **Filtragem automática**: Sistema filtra apenas produtos do seller logado
4. **Sessão persistente**: Identificação mantida durante toda a conversa

## Estrutura do Projeto

- `bot_simples.py` - **Arquivo principal recomendado** para executar o bot
- `telegram_bot_main.py` - Arquivo alternativo para executar o bot
- `start_services.bat` / `start_services.sh` - Scripts para iniciar PostgreSQL e Redis
- `app/integrations/bots/telegram_bot.py` - Comandos e lógica do bot
- `app/services/estoque_service.py` - Serviços de negócio
- `app/models/estoque_model.py` - Modelo de dados do estoque
- `docker-compose.yml` - Configuração dos serviços PostgreSQL e Redis

## Solução de Problemas

### Erro "Could not parse SQLAlchemy URL"
- ✅ **Solução**: Certifique-se de que PostgreSQL está rodando (`start_services.bat`)

### Erro "Field required [type=missing, input_value=...]"  
- ✅ **Solução**: Corrigido na versão atual do bot

### Bot não responde
- ✅ Verifique se o `TELEGRAM_BOT_TOKEN` está correto no `.env`
- ✅ Verifique se os serviços estão rodando: `docker ps`

### Como verificar se os serviços estão rodando
```bash
# Verificar containers Docker
docker ps

# Deve mostrar:
# - pc-postgres (PostgreSQL)
# - redis
```
