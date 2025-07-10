from unittest.mock import MagicMock, patch

import pytest

from app import api_main


# 🔸 Fixture que cria mock do Container
@pytest.fixture
def mock_container():
    """
    Fixture que cria um mock para o Container,
    patchando 'app.api_main.Container'.
    """
    with patch("app.api_main.Container") as MockContainer:
        yield MockContainer.return_value


# 🔸 Fixture que cria mock da função create_app
@pytest.fixture
def mock_create_app():
    """
    Fixture que cria um mock para a função create_app,
    retornando um mock de app.
    """
    with patch("app.api.api_application.create_app") as mock:
        mock_app = MagicMock()
        mock.return_value = mock_app
        yield mock


# 🔸 Fixture que cria mock do api_settings
@pytest.fixture
def mock_api_settings():
    """
    Fixture que cria um mock para api_settings
    no módulo app.api_main.
    """
    with patch("app.api_main.api_settings") as mock:
        yield mock
        

def test_init_creates_app_and_wires_modules(mock_container, mock_create_app, mock_api_settings):
    """
    Testa se a função init() cria a aplicação corretamente,
    configura o container, cria o app, realiza o wiring dos módulos
    e retorna o app criado.
    """
    app = api_main.init()

    # Verifica se o container configurou as settings
    mock_container.config.from_pydantic.assert_called_once_with(mock_api_settings)
    # Verifica se a função create_app foi chamada para criar o app
    mock_create_app.assert_called_once()
    # Verifica se o container fez o wiring dos 3 módulos esperados
    assert mock_container.wire.call_count == 3
    # Verifica se o app retornado é o mock retornado por create_app
    assert app == mock_create_app.return_value