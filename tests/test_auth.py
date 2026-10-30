def test_registration_and_login(client):
    response = client.post('/api/auth/register', json={
        'name': 'Ada Lovelace',
        'email': 'ADA@example.com',
        'password': 'secure-password'
    })
    assert response.status_code == 200

    response = client.post('/api/auth/login', json={
        'email': 'ada@example.com',
        'password': 'secure-password'
    })
    assert response.status_code == 200
    assert response.get_json()['data']['token']


def test_duplicate_registration_is_rejected(client):
    payload = {'name': 'Ada', 'email': 'ada@example.com', 'password': 'password'}
    assert client.post('/api/auth/register', json=payload).status_code == 200
    response = client.post('/api/auth/register', json=payload)
    assert response.status_code == 409


def test_login_requires_valid_credentials(client):
    response = client.post('/api/auth/login', json={
        'email': 'missing@example.com',
        'password': 'incorrect'
    })
    assert response.status_code == 401


def test_profile_requires_authentication(client):
    response = client.get('/api/auth/profile')
    assert response.status_code == 401
