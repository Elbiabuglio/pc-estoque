import pytest
from fastapi.testclient import TestClient

from app.api_main import app


@pytest.fixture(scope="session")
def api_client():
    # XXX Carregue....
    
    api_app = app
    with TestClient(api_app) as fastapi_client:
        yield fastapi_client
        
    # XXX Libere o que carregou