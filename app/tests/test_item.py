from typing import List

import pytest
from fastapi.testclient import TestClient
from main import app
from crud import CreateSchema
from sqlalchemy.orm import Session
from pytest import MonkeyPatch


@pytest.fixture(autouse=True)
def client():
    client = TestClient(app)
    yield client


@pytest.fixture
def items():
    return [
        {'id': 1, 'title': 'foo', 'user_id': 1},
        {'id': 2, 'title': 'bar', 'user_id': 2},
        {'id': 3, 'title': 'foobar', 'user_id': 1}
    ]


def test_read_items(
    client,
    monkeypatch: MonkeyPatch,
    items: List[dict]
):
    def mock_read_all(cls, session, *, skip, limit):
        return items[skip:limit]

    monkeypatch.setattr('crud.read_all', mock_read_all)

    res = client.get('/items')
    assert res.json() == items

    res = client.get('/items?skip=1')
    assert res.json() == items[1:]

    res = client.get('/items?limit=1')
    assert res.json() == items[:1]


def test_create_item(client, monkeypatch: MonkeyPatch):
    test_data = {'id': 1, 'title': 'foo', 'user_id': 1}

    def mock_create(cls, session, *, data):
        return test_data

    monkeypatch.setattr('crud.create_one', mock_create)

    res = client.post('/items/', json=test_data)
    assert res.json() == test_data


def test_update_item(client, monkeypatch: MonkeyPatch):
    test_data = {'id': 1, 'title': 'foo', 'user_id': 1}
    update_data = {'title': 'bar'}

    def mock_read_one(cls, session, pk):
        return test_data

    monkeypatch.setattr('crud.get_by_id', mock_read_one)

    def mock_update_one(session: Session, *, obj, data: CreateSchema):
        for k, v in data.dict(exclude_unset=True).items():
            if obj.get(k) != v:
                obj[k] = v
        return obj

    monkeypatch.setattr('crud.update_one', mock_update_one)

    res = client.put('/items/1', json=update_data)
    assert res.json() == test_data


def test_delete_item(client, items, monkeypatch: MonkeyPatch):
    test_data = {'id': 1, 'title': 'foo', 'user_id': 1}

    def mock_read_one(cls, session, pk):
        return test_data

    monkeypatch.setattr('crud.get_by_id', mock_read_one)

    def mock_delete_by_id(cls, session, *, pk):
        for i, item in enumerate(items):
            if item['id'] == pk:
                items.pop(i)
        return pk

    monkeypatch.setattr('crud.delete_by_id', mock_delete_by_id)
    res = client.delete('/items/1')
    assert res.json() == test_data
