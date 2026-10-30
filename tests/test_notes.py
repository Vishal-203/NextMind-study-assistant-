def create_note(client, headers, subject='Math'):
    response = client.post('/api/notes/', headers=headers, json={
        'subject': subject,
        'topic': 'Calculus',
        'content': 'Derivatives and integrals'
    })
    assert response.status_code == 200
    return response.get_json()['data']['id']


def test_authenticated_user_can_create_and_list_notes(client, auth_headers):
    note_id = create_note(client, auth_headers)
    response = client.get('/api/notes/', headers=auth_headers)
    assert response.status_code == 200
    items = response.get_json()['data']['items']
    assert any(note['id'] == note_id for note in items)


def test_user_cannot_read_another_users_note(client, mongo_db, auth_headers):
    mongo_db.notes.insert_one({
        '_id': __import__('bson').ObjectId(),
        'user_id': 'different-user-id',
        'subject': 'Private',
        'topic': 'Secret',
        'content': 'Not accessible'
    })
    note_id = str(mongo_db.notes.find_one()['_id'])
    response = client.get(f'/api/notes/{note_id}', headers=auth_headers)
    assert response.status_code == 404


def test_user_can_update_and_delete_owned_note(client, auth_headers):
    note_id = create_note(client, auth_headers)
    response = client.put(f'/api/notes/{note_id}', headers=auth_headers, json={
        'content': 'Updated content'
    })
    assert response.status_code == 200

    response = client.delete(f'/api/notes/{note_id}', headers=auth_headers)
    assert response.status_code == 200


def test_user_cannot_update_another_users_note(client, mongo_db, auth_headers):
    from bson import ObjectId
    note_id = ObjectId()
    mongo_db.notes.insert_one({
        '_id': note_id,
        'user_id': 'another-user',
        'subject': 'Private',
        'topic': 'Secret',
        'content': 'Original'
    })
    response = client.put(f'/api/notes/{note_id}', headers=auth_headers, json={
        'content': 'Tampered'
    })
    assert response.status_code == 404
