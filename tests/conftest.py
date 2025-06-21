"""
Arquivo de configuração de fixtures globais para os testes.

As fixtures declaradas aqui ficam disponíveis automaticamente em todos os testes,
sem necessidade de importação explícita.
"""

import pytest


@pytest.fixture(scope="session")
def dados_globais():
    """
    Fixture disponível para toda a sessão de testes.

    Executa uma configuração inicial e uma limpeza ao final da sessão.
    Retorna um dicionário com dados globais de exemplo.
    """
    print("\nConfigurando dados globais...")
    yield {"usuario": "admin", "senha": "123"}
    print("\nLimpando dados globais...")