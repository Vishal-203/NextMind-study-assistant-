from types import SimpleNamespace

import mongomock
import pytest

from backend.app import app


@pytest.fixture()
def mongo_db():
    client = mongomock.MongoClient()
    return client.nextmind


@pytest.fixture()
def test_app(mongo_db):
    app.config.update(TESTING=True)
    app.mongo = SimpleNamespace(db=mongo_db)
    yield app
    app.mongo = app.extensions['pymongo'] if 'pymongo' in app.extensions else app.mongo


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def auth_headers(client):
    registration = client.post('/api/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert registration.status_code == 200
    login = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert login.status_code == 200
    token = login.get_json()['data']['token']
    return {'Authorization': f'Bearer {token}'}
