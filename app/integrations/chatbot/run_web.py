#!/usr/bin/env python3
"""
Script para executar a interface web do chatbot
"""

import uvicorn
import sys
from pathlib import Path

# Adicionar path do projeto
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    print("🚀 Iniciando PC-Estoque Chatbot Web Interface...")
    print("📍 Interface disponível em: http://localhost:8081")
    print("⏹️  Para parar: Ctrl+C")
    print()

    try:
        uvicorn.run(
            "web_api_clean:app",
            host="0.0.0.0",
            port=8081,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Chatbot Web Interface encerrado")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)
