import os
from datetime import datetime

from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

from utils.helpers import parse_object_id, resp

# Configure file upload
UPLOAD_FOLDER = os.getenv(
    'UPLOAD_FOLDER',
    os.path.join(os.path.dirname(__file__), '..', 'uploads')
)
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'jpg', 'jpeg', 'png', 'docx'}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@jwt_required()
def upload_file(app):
    """Upload file and store metadata in database"""
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return resp(False, 'No file provided', status=400)
    
    file = request.files['file']
    if file.filename == '':
        return resp(False, 'No file selected', status=400)
    
    if not allowed_file(file.filename):
        return resp(False, f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}', status=400)
    
    try:
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        if not original_filename:
            return resp(False, 'Invalid filename', status=400)

        ext = original_filename.rsplit('.', 1)[1].lower()
        file_id = str(ObjectId())
        filename = f"{file_id}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save file
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        if file_size > MAX_FILE_SIZE:
            os.remove(filepath)
            return resp(False, 'File too large (max 20MB)', status=400)
        
        # Store metadata in database
        file_doc = {
            'user_id': user_id,
            'original_filename': original_filename,
            'stored_filename': filename,
            'file_type': ext,
            'file_size': file_size,
            'created_at': datetime.utcnow()
        }
        result = app.mongo.db.files.insert_one(file_doc)
        
        return resp(True, 'File uploaded', {
            'id': str(result.inserted_id),
            'filename': original_filename,
            'size': file_doc['file_size']
        })
    except Exception as e:
        return resp(False, f'Upload failed: {str(e)}', status=500)


@jwt_required()
def delete_file(app, file_id):
    """Delete uploaded file"""
    user_id = get_jwt_identity()
    file_obj_id = parse_object_id(file_id, 'file_id')
    if file_obj_id is None:
        return resp(False, 'Invalid file ID', status=400)
    
    # Find file metadata
    file_doc = app.mongo.db.files.find_one({
        '_id': file_obj_id,
        'user_id': user_id
    })
    
    if not file_doc:
        return resp(False, 'File not found', status=404)
    
    try:
        # Delete physical file
        filepath = os.path.join(UPLOAD_FOLDER, file_doc['stored_filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Remove from database
        app.mongo.db.files.delete_one({'_id': file_obj_id})
        
        return resp(True, 'File deleted')
    except Exception as e:
        return resp(False, f'Deletion failed: {str(e)}', status=500)


@jwt_required()
def get_file(app, file_id):
    """Download file (secure access)"""
    user_id = get_jwt_identity()
    file_obj_id = parse_object_id(file_id, 'file_id')
    if file_obj_id is None:
        return resp(False, 'Invalid file ID', status=400)
    
    # Find file metadata
    file_doc = app.mongo.db.files.find_one({
        '_id': file_obj_id,
        'user_id': user_id
    })
    
    if not file_doc:
        return resp(False, 'File not found', status=404)
    
    try:
        filepath = os.path.join(UPLOAD_FOLDER, file_doc['stored_filename'])
        if not os.path.exists(filepath):
            return resp(False, 'File not found on disk', status=404)
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=file_doc['original_filename']
        )
    except Exception as e:
        return resp(False, f'Download failed: {str(e)}', status=500)


@jwt_required()
def list_files(app):
    """List all uploaded files for user"""
    user_id = get_jwt_identity()
    
    files = list(app.mongo.db.files.find({'user_id': user_id}).sort('created_at', -1))
    
    result = []
    for f in files:
        result.append({
            'id': str(f['_id']),
            'filename': f['original_filename'],
            'size': f['file_size'],
            'type': f['file_type'],
            'created_at': f['created_at']
        })
    
    return resp(True, 'Files fetched', result)
