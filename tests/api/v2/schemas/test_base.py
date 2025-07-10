from app.api.v2.schemas.base import TimestampMixinSchema, UuidMixinSchema


def test_uuid_mixin_schema_with_id(fake_uuid):
    """
    Testa se UuidMixinSchema inicializa corretamente com um ID fornecido.
    """
    schema = UuidMixinSchema(id=fake_uuid)
    assert schema.id == fake_uuid

def test_uuid_mixin_schema_without_id():
    """
    Testa se UuidMixinSchema inicializa com id None quando não fornecido.
    """
    schema = UuidMixinSchema()
    assert schema.id is None

def test_timestamp_mixin_schema_with_dates(fake_datetime):
    """
    Testa se TimestampMixinSchema inicializa corretamente com created_at e updated_at fornecidos.
    """
    schema = TimestampMixinSchema(created_at=fake_datetime, updated_at=fake_datetime)
    assert schema.created_at == fake_datetime
    assert schema.updated_at == fake_datetime

def test_timestamp_mixin_schema_without_dates():
    """
    Testa se TimestampMixinSchema inicializa com created_at e updated_at None quando não fornecidos.
    """
    schema = TimestampMixinSchema()
    assert schema.created_at is None
    assert schema.updated_at is None