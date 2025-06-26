import pytest
from unittest.mock import patch
from app.api.common import trace

def test_get_trace_id_length():
    trace_id = trace.get_trace_id()
    assert isinstance(trace_id, str)
    assert len(trace_id) == 32  # 16 bytes em hexadecimal = 32 caracteres

def test_get_trace_id_mocked():
    with patch("app.api.common.trace.secrets.token_hex", return_value="abc123"):
        trace_id = trace.get_trace_id()
        assert trace_id == "abc123"