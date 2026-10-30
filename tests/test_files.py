from io import BytesIO

from bson import ObjectId


def test_file_upload_and_listing(client, auth_headers):
    response = client.post('/api/files/', headers=auth_headers, data={
        'file': (BytesIO(b'study material'), 'notes.txt')
    })
    assert response.status_code == 200

    response = client.get('/api/files/', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.get_json()['data']) == 1


def test_user_cannot_delete_another_users_file(client, mongo_db, auth_headers):
    file_id = ObjectId()
    mongo_db.files.insert_one({
        '_id': file_id,
        'user_id': 'another-user',
        'original_filename': 'private.txt',
        'stored_filename': 'missing.txt',
        'file_type': 'txt',
        'file_size': 10
    })
    response = client.delete(f'/api/files/{file_id}', headers=auth_headers)
    assert response.status_code == 404


def test_user_cannot_download_another_users_file(client, mongo_db, auth_headers):
    file_id = ObjectId()
    mongo_db.files.insert_one({
        '_id': file_id,
        'user_id': 'another-user',
        'original_filename': 'private.txt',
        'stored_filename': 'missing.txt',
        'file_type': 'txt',
        'file_size': 10
    })
    response = client.get(f'/api/files/{file_id}/download', headers=auth_headers)
    assert response.status_code == 404
