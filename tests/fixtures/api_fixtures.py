from app.api_main import app
from fastapi.testclient import TestClient
import pytest

@pytest.fixture(scope="session")
def api_client():
    # XXX Carregue....
    
    api_app = app
    with TestClient(api_app) as fastapi_client:
        yield fastapi_client
        
    # XXX Libere o que carregou