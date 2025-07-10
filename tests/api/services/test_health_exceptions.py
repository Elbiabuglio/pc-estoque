"""
Testes unitários para as exceções definidas em health_exceptions.
"""

import pytest

from app.services.health_check.health_exceptions import (
    HealthCheckException,
    InvalidConfigurationException,
    ServiceReturnedUnexpectedResult,
    ServiceUnavailable,
    ServiceWarning,
)

"""
Fixtures e instâncias auxiliares para testes das exceções de health_check.
"""

@pytest.fixture
def exception_instance():
    """Instância da exceção base HealthCheckException."""
    return HealthCheckException("Algo deu errado")


@pytest.fixture
def invalid_config_exception():
    """Instância da exceção InvalidConfigurationException."""
    return InvalidConfigurationException("Configuração inválida detectada")


@pytest.fixture
def service_warning_exception():
    """Instância da exceção ServiceWarning."""
    return ServiceWarning("Serviço respondeu com comportamento inesperado")


@pytest.fixture
def service_unavailable_exception():
    """Instância da exceção ServiceUnavailable."""
    return ServiceUnavailable("O serviço está temporariamente indisponível")


@pytest.fixture
def unexpected_result_exception():
    """Instância da exceção ServiceReturnedUnexpectedResult."""
    return ServiceReturnedUnexpectedResult("O serviço retornou dados inválidos")

# -------- HealthCheckException --------

def test_exception_message_type(exception_instance):
    """Deve retornar o tipo de mensagem padrão da exceção base."""
    assert exception_instance.message_type == "unknown error"


def test_exception_message(exception_instance):
    """Deve manter a mensagem passada na inicialização."""
    assert exception_instance.message == "Algo deu errado"


def test_exception_str(exception_instance):
    """Deve formatar a mensagem no formato correto ao usar str()."""
    assert str(exception_instance) == "unknown error: Algo deu errado"


# -------- InvalidConfigurationException --------

def test_invalid_config_message_type(invalid_config_exception):
    """Deve retornar o tipo de mensagem correto para configuração inválida."""
    assert invalid_config_exception.message_type == "unexpected configuration"


def test_invalid_config_message(invalid_config_exception):
    """Deve manter a mensagem fornecida."""
    assert invalid_config_exception.message == "Configuração inválida detectada"


def test_invalid_config_str(invalid_config_exception):
    """Deve formatar corretamente a mensagem de exceção."""
    assert str(invalid_config_exception) == "unexpected configuration: Configuração inválida detectada"


# -------- ServiceWarning --------

def test_service_warning_message_type(service_warning_exception):
    """Deve ter o tipo de mensagem 'warning'."""
    assert service_warning_exception.message_type == "warning"


def test_service_warning_message(service_warning_exception):
    """Deve armazenar corretamente a mensagem da exceção."""
    assert service_warning_exception.message == "Serviço respondeu com comportamento inesperado"


def test_service_warning_str(service_warning_exception):
    """Deve apresentar o texto formatado corretamente com o tipo de aviso."""
    assert str(service_warning_exception) == "warning: Serviço respondeu com comportamento inesperado"


# -------- ServiceUnavailable --------

def test_service_unavailable_message_type(service_unavailable_exception):
    """Deve possuir o tipo de mensagem 'unavailable'."""
    assert service_unavailable_exception.message_type == "unavailable"


def test_service_unavailable_message(service_unavailable_exception):
    """Deve preservar a mensagem informada."""
    assert service_unavailable_exception.message == "O serviço está temporariamente indisponível"


def test_service_unavailable_str(service_unavailable_exception):
    """Deve formatar corretamente a mensagem da exceção de indisponibilidade."""
    assert str(service_unavailable_exception) == "unavailable: O serviço está temporariamente indisponível"


# -------- ServiceReturnedUnexpectedResult --------

def test_unexpected_result_message_type(unexpected_result_exception):
    """Deve retornar o tipo de mensagem 'unexpected result'."""
    assert unexpected_result_exception.message_type == "unexpected result"


def test_unexpected_result_message(unexpected_result_exception):
    """Deve manter corretamente a mensagem passada."""
    assert unexpected_result_exception.message == "O serviço retornou dados inválidos"


def test_unexpected_result_str(unexpected_result_exception):
    """Deve apresentar a mensagem formatada corretamente."""
    assert str(unexpected_result_exception) == "unexpected result: O serviço retornou dados inválidos"