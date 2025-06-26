from app.container import Container

def test_container_providers(
    mock_settings,
    mock_sql_client,
    mock_estoque_repository,
    mock_health_check_service,
    mock_estoque_service
):
    """
    Testa se o container retorna as dependências corretas quando sobrescreve
    os providers com mocks.

    - Configura a URL do banco em memória e uma lista vazia para health checkers.
    - Faz override dos providers com os mocks fornecidos.
    - Verifica se o container retorna os mocks corretamente para cada provider.
    """
    container = Container()
    container.config.app_db_url.from_value("sqlite:///:memory:")
    container.config.health_check_checkers.from_value([])

    # Override para usar os mocks no container
    container.settings.override(mock_settings)
    container.sql_client.override(mock_sql_client)
    container.estoque_repository.override(mock_estoque_repository)
    container.health_check_service.override(mock_health_check_service)
    container.estoque_service.override(mock_estoque_service)

    # Verifica se os singletons retornam os mocks corretamente
    assert container.settings() is mock_settings
    assert container.sql_client() is mock_sql_client
    assert container.estoque_repository() is mock_estoque_repository
    assert container.health_check_service() is mock_health_check_service
    assert container.estoque_service() is mock_estoque_service
