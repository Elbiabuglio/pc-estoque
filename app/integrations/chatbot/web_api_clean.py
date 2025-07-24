"""
Interface Web FastAPI para o Chatbot PC-Estoque
Design Profissional e Elegante
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import sys
from pathlib import Path
import logging

# Adicionar path do projeto
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sistema simplificado - sem dependências de IA por enquanto
CHATBOT_AVAILABLE = False

# Controle de usuários logados por sessão
usuarios_logados = {}
try:
    from app.container import Container
    from app.repositories.estoque_repository import EstoqueRepository
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("⚠️ Banco de dados não disponível - usando modo demonstração")

# CRIAR A INSTÂNCIA DO APP PRIMEIRO
app = FastAPI(
    title="PC-Estoque Assistente API",
    description="API do Assistente Inteligente para Controle de Estoque",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar templates e arquivos estáticos
CURRENT_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=CURRENT_DIR / "templates")

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory=CURRENT_DIR / "static"), name="static")

# Inicializar sistema simplificado
chatbot_facade = None
logger.info("Sistema em modo básico - resposta sempre rápida")

# Modelos Pydantic
class MensagemRequest(BaseModel):
    mensagem: str
    session_id: str = "web_default"

class MensagemResponse(BaseModel):
    resposta: str
    sucesso: bool
    tipo: str
    features: dict

# Função para buscar sellers do banco (mock/demo)
async def buscar_sellers_do_banco():
    """Função mock para simular busca de sellers"""
    return {
        "admin": {"nome": "Administrador", "nivel": "admin"},
        "seller1": {"nome": "João Silva", "nivel": "seller"},
        "seller2": {"nome": "Maria Santos", "nivel": "seller"},
        "demo": {"nome": "Usuário Demo", "nivel": "demo"},
    }

# Função de processamento básico sem IA (fallback)
async def processar_basico(mensagem: str, session_id: str = "default") -> str:
    """Função de processamento básico sem IA (fallback)"""
    try:
        # Verificar se usuário está logado
        if session_id not in usuarios_logados and not mensagem.startswith('identificar'):
            return """<div class='popup-container' style='background-color: #fff3cd !important; border-radius: 12px !important; box-shadow: 0 4px 12px rgba(255, 193, 7, 0.2) !important; padding: 32px !important; max-width: 500px !important; width: 100% !important; box-sizing: border-box !important; margin: 1rem auto !important; font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif !important; border-left: 4px solid #ffc107 !important;'>
  <div class='popup-title' style='font-size: 20px !important; font-weight: bold !important; color: #856404 !important; margin-bottom: 8px !important;'>🔐 IDENTIFICAÇÃO NECESSÁRIA</div>
  <div class='popup-subtitle' style='font-size: 16px !important; color: #34495e !important; margin-bottom: 20px !important;'>
    Para usar o sistema, identifique-se primeiro.
  </div>
  <div style='margin-bottom: 18px; color: #495057; font-size: 15px !important;'>
    <strong>Como se identificar:</strong><br>
    Digite: <code style='background: #f8f9fa; padding: 2px 6px; border-radius: 4px;'>identificar [seu_id]</code>
  </div>
  <div style='font-size: 14px; color: #6c757d;'>
    IDs disponíveis para teste: admin, seller1, seller2, demo
  </div>
</div>"""

        # Comando de identificação
        if mensagem.startswith('identificar'):
            partes = mensagem.split()
            if len(partes) == 2:
                seller_id = partes[1]
                # Buscar sellers válidos
                sellers = await buscar_sellers_do_banco()
                if seller_id in sellers:
                    usuarios_logados[session_id] = {
                        "user_id": seller_id,
                        "nome": sellers[seller_id]["nome"],
                        "nivel": sellers[seller_id]["nivel"]
                    }
                    return f"""
<div style='font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa; margin: 0; padding: 40px; display: flex; justify-content: center; align-items: flex-start;'>
  <div class='popup-container' style='background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); padding: 32px; max-width: 700px; width: 100%; box-sizing: border-box;'>
    <div class='popup-title' style='font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 8px;'>
      ACESSO AUTORIZADO: <span style="color:#2980b9;">{seller_id}</span>
    </div>
    <div class='popup-subtitle' style='font-size: 16px; color: #34495e; margin-bottom: 24px;'>
      Bem-vindo, <strong>{sellers[seller_id]['nome']}</strong>!<br>
      Você agora tem acesso completo ao sistema PC-Estoque.<br>
      Nível de acesso: <span style='color: #2980b9; font-weight: 600;'>{sellers[seller_id]['nivel'].upper()}</span>
    </div>
    
    <h3 style='font-size: 16px; color: #2c3e50; border-bottom: 1px solid #e0e0e0; padding-bottom: 6px; margin-top: 24px; margin-bottom: 12px;'>
      GESTÃO DE ESTOQUE
    </h3>
    <ul style='list-style: none; padding-left: 0; margin: 0;'>
      <li style='padding: 8px 12px; margin-bottom: 6px; background-color: #f0f4f8; border-radius: 6px; font-size: 14px; color: #2d3436;'>
        <code style='font-weight: 600; color: #2980b9;'>adicionar</code> – Adicionar novo produto
      </li>
      <li style='padding: 8px 12px; margin-bottom: 6px; background-color: #f0f4f8; border-radius: 6px; font-size: 14px; color: #2d3436;'>
        <code style='font-weight: 600; color: #2980b9;'>consultar</code> – Consultar produto específico
      </li>
      <li style='padding: 8px 12px; margin-bottom: 6px; background-color: #f0f4f8; border-radius: 6px; font-size: 14px; color: #2d3436;'>
        <code style='font-weight: 600; color: #2980b9;'>atualizar</code> – Atualizar quantidade
      </li>
      <li style='padding: 8px 12px; margin-bottom: 6px; background-color: #f0f4f8; border-radius: 6px; font-size: 14px; color: #2d3436;'>
        <code style='font-weight: 600; color: #2980b9;'>remover</code> – Remover produto
      </li>
      <li style='padding: 8px 12px; margin-bottom: 6px; background-color: #f0f4f8; border-radius: 6px; font-size: 14px; color: #2d3436;'>
        <code style='font-weight: 600; color: #2980b9;'>listar</code> – Ver todos os produtos
      </li>
      <li style='padding: 8px 12px; margin-bottom: 6px; background-color: #f0f4f8; border-radius: 6px; font-size: 14px; color: #2d3436;'>
        <code style='font-weight: 600; color: #2980b9;'>estoque-baixo</code> – Ver produtos críticos
      </li>
    </ul>
    
    <h3 style='font-size: 16px; color: #2c3e50; border-bottom: 1px solid #e0e0e0; padding-bottom: 6px; margin-top: 24px; margin-bottom: 12px;'>
      SISTEMA & CONTROLE
    </h3>
    <ul style='list-style: none; padding-left: 0; margin: 0;'>
      <li style='padding: 8px 12px; margin-bottom: 6px; background-color: #f0f4f8; border-radius: 6px; font-size: 14px; color: #2d3436;'>
        <code style='font-weight: 600; color: #2980b9;'>historico</code> – Histórico de movimentações
      </li>
      <li style='padding: 8px 12px; margin-bottom: 6px; background-color: #f0f4f8; border-radius: 6px; font-size: 14px; color: #2d3436;'>
        <code style='font-weight: 600; color: #2980b9;'>logout</code> – Encerrar sessão
      </li>
    </ul>
    
    <div style='margin-top: 24px; font-style: italic; color: #7f8c8d; font-size: 13px;'>
      Dica: Digite qualquer comando para começar!
    </div>
  </div>
</div>"""
                else:
                    return f"""<div class='popup-container' style='background-color: #f8d7da !important; border-radius: 12px !important; box-shadow: 0 4px 12px rgba(220, 53, 69, 0.2) !important; padding: 32px !important; max-width: 500px !important; width: 100% !important; box-sizing: border-box !important; margin: 1rem auto !important; font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif !important; border-left: 4px solid #dc3545 !important;'>
  <div class='popup-title' style='font-size: 20px !important; font-weight: bold !important; color: #721c24 !important; margin-bottom: 8px !important;'>❌ SELLER NÃO ENCONTRADO</div>
  <div class='popup-subtitle' style='font-size: 16px !important; color: #34495e !important; margin-bottom: 20px !important;'>
    Seller <strong>{seller_id}</strong> não encontrado.
  </div>
  <div style='font-size: 14px; color: #6c757d;'>
    IDs válidos: admin, seller1, seller2, demo
  </div>
</div>"""
            else:
                return """<div class='popup-container' style='background-color: #fff3cd !important; border-radius: 12px !important; box-shadow: 0 4px 12px rgba(255, 193, 7, 0.2) !important; padding: 32px !important; max-width: 500px !important; width: 100% !important; box-sizing: border-box !important; margin: 1rem auto !important; font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif !important; border-left: 4px solid #ffc107 !important;'>
  <div class='popup-title' style='font-size: 20px !important; font-weight: bold !important; color: #856404 !important; margin-bottom: 8px !important;'>⚠️ PARÂMETRO FALTANDO</div>
  <div class='popup-subtitle' style='font-size: 16px !important; color: #34495e !important; margin-bottom: 20px !important;'>
    Sintaxe correta: <code style='background: #f8f9fa; padding: 2px 6px; border-radius: 4px; color: #495057;'>identificar [seu_seller_id]</code>
  </div>
</div>"""
        
        # Comando de logout
        if mensagem.strip().lower() == 'logout':
            if session_id in usuarios_logados:
                nome = usuarios_logados[session_id]['nome']
                del usuarios_logados[session_id]
                return f"""<div class='popup-container' style='background-color: #d1ecf1 !important; border-radius: 12px !important; box-shadow: 0 4px 12px rgba(23, 162, 184, 0.2) !important; padding: 32px !important; max-width: 500px !important; width: 100% !important; box-sizing: border-box !important; margin: 1rem auto !important; font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif !important; border-left: 4px solid #17a2b8 !important;'>
  <div class='popup-title' style='font-size: 20px !important; font-weight: bold !important; color: #0c5460 !important; margin-bottom: 8px !important;'>👋 LOGOUT REALIZADO</div>
  <div class='popup-subtitle' style='font-size: 16px !important; color: #34495e !important; margin-bottom: 20px !important;'>
    Até logo, <strong>{nome}</strong>!
  </div>
  <div style='font-size: 14px; color: #6c757d;'>
    Para acessar novamente, use: <code style='background: #f8f9fa; padding: 2px 6px; border-radius: 4px;'>identificar [seu_id]</code>
  </div>
</div>"""

        if mensagem.strip().lower() == 'estoque-baixo':
            return """
<div style='font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa; margin: 0; padding: 40px; display: flex; justify-content: center; align-items: flex-start;'>
  <div class='popup-container' style='background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(231, 76, 60, 0.15); padding: 32px; max-width: 800px; width: 100%; box-sizing: border-box; border-left: 4px solid #e74c3c;'>
    <div class='popup-title' style='font-size: 20px; font-weight: bold; color: #c0392b; margin-bottom: 8px;'>
      🚨 PRODUTOS COM ESTOQUE CRÍTICO
    </div>
    <div class='popup-subtitle' style='font-size: 16px; color: #34495e; margin-bottom: 24px;'>
      Produtos que precisam de reposição urgente (quantidade ≤ 5)
    </div>
    
    <div style='background: #fff5f5; border-radius: 8px; padding: 20px; margin-bottom: 20px;'>
      <div style='color: #c0392b; font-weight: 600; margin-bottom: 15px; font-size: 16px;'>⚠️ ALERTA CRÍTICO</div>
      
      <div style='background: white; border-radius: 6px; padding: 15px; margin-bottom: 10px; border-left: 3px solid #e74c3c;'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
          <span style='font-weight: 600; color: #2c3e50; font-size: 15px;'>KB003 - Teclado Mecânico RGB</span>
          <span style='background: #f8d7da; color: #721c24; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;'>🚨 CRÍTICO</span>
        </div>
        <div style='display: flex; justify-content: space-between; color: #6c757d; font-size: 14px;'>
          <span>Quantidade atual: <strong style='color: #e74c3c;'>3 unidades</strong></span>
          <span>Preço: <strong>R$ 250,00</strong></span>
        </div>
        <div style='margin-top: 8px; font-size: 12px; color: #e67e22;'>
          📅 Sugestão: Reabastecer com pelo menos 10 unidades
        </div>
      </div>
    </div>
    
    <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 8px; padding: 20px;'>
      <h4 style='margin: 0 0 12px 0; color: #2c3e50; font-size: 14px;'>📊 ESTATÍSTICAS DE ESTOQUE CRÍTICO</h4>
      <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;'>
        <div style='text-align: center;'>
          <div style='font-size: 24px; font-weight: bold; color: #e74c3c;'>1</div>
          <div style='font-size: 12px; color: #6c757d;'>Produto Crítico</div>
        </div>
        <div style='text-align: center;'>
          <div style='font-size: 24px; font-weight: bold; color: #e67e22;'>R$ 750,00</div>
          <div style='font-size: 12px; color: #6c757d;'>Valor Bloqueado</div>
        </div>
        <div style='text-align: center;'>
          <div style='font-size: 24px; font-weight: bold; color: #f39c12;'>25%</div>
          <div style='font-size: 12px; color: #6c757d;'>Taxa de Criticidade</div>
        </div>
      </div>
    </div>
    
    <div style='margin-top: 20px; padding: 15px; background: #e8f4fd; border-radius: 8px; border-left: 3px solid #3498db;'>
      <div style='color: #2980b9; font-weight: 600; margin-bottom: 8px; font-size: 14px;'>💡 AÇÕES RECOMENDADAS</div>
      <ul style='margin: 0; padding-left: 20px; color: #34495e; font-size: 13px;'>
        <li>Entrar em contato com fornecedores para reposição urgente</li>
        <li>Considerar compras em maior quantidade para evitar rupturas</li>
        <li>Monitorar vendas diárias destes produtos</li>
      </ul>
    </div>
    
    <div style='margin-top: 20px; font-style: italic; color: #7f8c8d; font-size: 13px;'>
      🔄 Atualizado automaticamente • Use <code style='background: #f8f9fa; padding: 2px 6px; border-radius: 4px; color: #2980b9;'>listar</code> para ver todos os produtos
    </div>
  </div>
</div>"""

        # Outros comandos (mock para demonstração)
        usuario = usuarios_logados.get(session_id, {})
        
        if mensagem.strip().lower() == 'listar':
            return """
<div style='font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa; margin: 0; padding: 40px; display: flex; justify-content: center; align-items: flex-start;'>
  <div class='popup-container' style='background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); padding: 32px; max-width: 900px; width: 100%; box-sizing: border-box;'>
    <div class='popup-title' style='font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 8px;'>
      📦 PRODUTOS EM ESTOQUE
    </div>
    <div class='popup-subtitle' style='font-size: 16px; color: #34495e; margin-bottom: 24px;'>
      Lista completa de produtos disponíveis no sistema
    </div>
    
    <div style='overflow-x: auto; margin-top: 20px;'>
      <table style='width: 100%; border-collapse: collapse; font-size: 14px; background: #fff;'>
        <thead>
          <tr style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
            <th style='padding: 15px 12px; text-align: left; font-weight: 600; border-radius: 8px 0 0 0;'>SKU</th>
            <th style='padding: 15px 12px; text-align: left; font-weight: 600;'>Produto</th>
            <th style='padding: 15px 12px; text-align: center; font-weight: 600;'>Quantidade</th>
            <th style='padding: 15px 12px; text-align: right; font-weight: 600;'>Preço Unit.</th>
            <th style='padding: 15px 12px; text-align: center; font-weight: 600; border-radius: 0 8px 0 0;'>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr style='background: #f8f9fa; transition: background 0.3s ease;'>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #2980b9;'>PC001</td>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; color: #2c3e50;'>Desktop Gamer RTX 4060</td>
            <td style='padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #27ae60;'>15</td>
            <td style='padding: 12px; text-align: right; border-bottom: 1px solid #e9ecef; color: #2c3e50;'>R$ 3.500,00</td>
            <td style='padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef;'>
              <span style='background: #d4edda; color: #155724; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600;'>✅ NORMAL</span>
            </td>
          </tr>
          <tr style='background: #ffffff; transition: background 0.3s ease;'>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #2980b9;'>NB002</td>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; color: #2c3e50;'>Notebook Dell Inspiron i5</td>
            <td style='padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #f39c12;'>8</td>
            <td style='padding: 12px; text-align: right; border-bottom: 1px solid #e9ecef; color: #2c3e50;'>R$ 2.800,00</td>
            <td style='padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef;'>
              <span style='background: #fff3cd; color: #856404; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600;'>⚠️ MÉDIO</span>
            </td>
          </tr>
          <tr style='background: #f8f9fa; transition: background 0.3s ease;'>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #2980b9;'>KB003</td>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; color: #2c3e50;'>Teclado Mecânico RGB</td>
            <td style='padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #e74c3c;'>3</td>
            <td style='padding: 12px; text-align: right; border-bottom: 1px solid #e9ecef; color: #2c3e50;'>R$ 250,00</td>
            <td style='padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef;'>
              <span style='background: #f8d7da; color: #721c24; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600;'>🚨 CRÍTICO</span>
            </td>
          </tr>
          <tr style='background: #ffffff; transition: background 0.3s ease;'>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #2980b9;'>MT004</td>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; color: #2c3e50;'>Monitor 24" Full HD</td>
            <td style='padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef; font-weight: 600; color: #27ae60;'>22</td>
            <td style='padding: 12px; text-align: right; border-bottom: 1px solid #e9ecef; color: #2c3e50;'>R$ 680,00</td>
            <td style='padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef;'>
              <span style='background: #d4edda; color: #155724; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600;'>✅ NORMAL</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div style='margin-top: 20px; padding: 15px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 8px;'>
      <h4 style='margin: 0 0 8px 0; color: #2c3e50; font-size: 14px;'>📊 RESUMO DO ESTOQUE</h4>
      <div style='display: flex; gap: 20px; flex-wrap: wrap;'>
        <div style='color: #27ae60; font-weight: 600;'>✅ Normal: 2 produtos</div>
        <div style='color: #f39c12; font-weight: 600;'>⚠️ Médio: 1 produto</div>
        <div style='color: #e74c3c; font-weight: 600;'>🚨 Crítico: 1 produto</div>
      </div>
    </div>
    
    <div style='margin-top: 20px; font-style: italic; color: #7f8c8d; font-size: 13px;'>
      💡 Use <code style='background: #f8f9fa; padding: 2px 6px; border-radius: 4px; color: #2980b9;'>estoque-baixo</code> para ver apenas produtos críticos
    </div>
  </div>
</div>"""

        return f"""<div class='popup-container' style='background-color: #e2e3e5 !important; border-radius: 12px !important; box-shadow: 0 4px 12px rgba(108, 117, 125, 0.2) !important; padding: 32px !important; max-width: 600px !important; width: 100% !important; box-sizing: border-box !important; margin: 1rem auto !important; font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif !important; border-left: 4px solid #6c757d !important;'>
  <div class='popup-title' style='font-size: 20px !important; font-weight: bold !important; color: #495057 !important; margin-bottom: 8px !important;'>🤖 COMANDO PROCESSADO</div>
  <div class='popup-subtitle' style='font-size: 16px !important; color: #34495e !important; margin-bottom: 20px !important;'>
    Você disse: <em>"{mensagem}"</em>
  </div>
  <div style='margin-bottom: 18px; color: #495057; font-size: 15px !important;'>
    Este é um sistema de demonstração. Em produção, este comando seria processado pelo sistema completo.
  </div>
  <div style='font-size: 14px; color: #6c757d;'>
    Usuário: <strong>{usuario.get('nome', 'Desconhecido')}</strong> | Nível: <strong>{usuario.get('nivel', 'N/A')}</strong>
  </div>
</div>"""
        
    except Exception as e:
        return f"Erro interno no processamento: {str(e)}"

# Função de processamento com IA integrada
async def processar_com_ia(mensagem: str, session_id: str = "web_default") -> dict:
    """Função de processamento - sempre resposta rápida"""
    try:
        # SEMPRE usar processamento básico primeiro para garantir resposta rápida
        resposta = await processar_basico(mensagem, session_id)
        
        return {
            "resposta": resposta,
            "sucesso": True,
            "tipo": "basico_rapido",
            "features": {"commands": True, "ai": False, "database": False}
        }
        
    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        return {
            "resposta": f"Erro interno: {str(e)}",
            "sucesso": False,
            "tipo": "erro",
            "features": {}
        }

# ROTAS DA API

@app.get("/", response_class=HTMLResponse)
async def root():
    # Redireciona para /chat ou exibe mensagem de boas-vindas
    return """
    <html>
        <head>
            <title>PC-Estoque Chatbot</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style='font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); text-align: center; padding-top: 60px; margin: 0; min-height: 100vh;'>
            <div style='background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px; max-width: 500px; margin: 0 auto; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);'>
                <h1 style='color: #333; margin-bottom: 10px; font-size: 32px;'>🖥️ PC-Estoque</h1>
                <h2 style='color: #666; margin-bottom: 30px; font-weight: 300; font-size: 18px;'>Assistente Inteligente</h2>
                <p style='color: #555; margin-bottom: 30px; line-height: 1.6;'>Bem-vindo à interface web do assistente de estoque!</p>
                <a href="/chat" style='display: inline-block; color: #fff; background: linear-gradient(45deg, #007bff, #0056b3); padding: 15px 30px; border-radius: 50px; text-decoration: none; font-size: 18px; font-weight: 500; transition: transform 0.3s ease; box-shadow: 0 8px 20px rgba(0, 123, 255, 0.3);'>
                    🚀 Acessar Chat
                </a>
            </div>
        </body>
    </html>
    """

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Página principal do chat"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/api/chat", response_model=MensagemResponse)
async def processar_mensagem(request: MensagemRequest):
    """Endpoint para processar mensagens do chat"""
    try:
        resultado = await processar_com_ia(request.mensagem, request.session_id)
        return MensagemResponse(**resultado)
    except Exception as e:
        logger.error(f"Erro na API de chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def status():
    """Status da API"""
    return {
        "status": "online",
        "chatbot_available": CHATBOT_AVAILABLE,
        "database_available": DATABASE_AVAILABLE,
        "usuarios_logados": len(usuarios_logados),
        "features": {
            "commands": True,
            "ai": CHATBOT_AVAILABLE,
            "database": DATABASE_AVAILABLE
        }
    }

@app.get("/api/usuarios")
async def usuarios_ativos():
    """Lista usuários ativos (sem dados sensíveis)"""
    return {
        "total": len(usuarios_logados),
        "usuarios": [
            {
                "session_id": sid[:8] + "...",
                "nome": dados["nome"],
                "nivel": dados["nivel"]
            }
            for sid, dados in usuarios_logados.items()
        ]
    }

# Para rodar o servidor
if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando PC-Estoque Chatbot Web Interface...")
    print("📍 Interface disponível em: http://localhost:8081")
    print("⏹️  Para parar: Ctrl+C")
    uvicorn.run(app, host="0.0.0.0", port=8081, reload=True)