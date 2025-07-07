import pytest
from unittest.mock import AsyncMock, Mock
from app.services.base.crud_service import CrudService
from app.common.exceptions import NotFoundException

class FakeEntity:
    pass

@pytest.mark.asyncio
async def test_create():
    repo = AsyncMock()
    repo.create.return_value = FakeEntity()
    service = CrudService(repo)

    result = await service.create(FakeEntity())
    repo.create.assert_called_once()
    assert isinstance(result, FakeEntity)

@pytest.mark.asyncio
async def test_find_by_id_found():
    repo = AsyncMock()
    repo.find_by_id.return_value = FakeEntity()
    service = CrudService(repo)

    result = await service.find_by_id("id1")
    repo.find_by_id.assert_called_once_with("id1")
    assert isinstance(result, FakeEntity)

@pytest.mark.asyncio
async def test_find_by_id_not_found_raises():
    repo = AsyncMock()
    repo.find_by_id.return_value = None
    service = CrudService(repo)

    with pytest.raises(NotFoundException):
        await service.find_by_id("id1", can_raise_exception=True)

@pytest.mark.asyncio
async def test_find_by_id_not_found_no_raise():
    repo = AsyncMock()
    repo.find_by_id.return_value = None
    service = CrudService(repo)

    result = await service.find_by_id("id1", can_raise_exception=False)
    assert result is None

@pytest.mark.asyncio
async def test_find():
    repo = AsyncMock()
    repo.find.return_value = [FakeEntity()]
    service = CrudService(repo)

    paginator = Mock()
    paginator.limit = 10
    paginator.offset = 0
    paginator.get_sort_order = Mock(return_value="id")

    filters = {"name": "test"}

    result = await service.find(paginator, filters)

    repo.find.assert_called_once()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_update():
    repo = AsyncMock()
    repo.update.return_value = FakeEntity()
    service = CrudService(repo)

    result = await service.update("id1", FakeEntity())
    repo.update.assert_called_once()
    assert isinstance(result, FakeEntity)

@pytest.mark.asyncio
async def test_delete_by_id():
    repo = AsyncMock()
    repo.delete_by_id.return_value = None
    service = CrudService(repo)

    await service.delete_by_id("id1")
    repo.delete_by_id.assert_called_once_with("id1")
