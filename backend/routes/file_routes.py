from flask import Blueprint, current_app
from flask_jwt_extended import jwt_required
from controllers.file_controller import upload_file, delete_file, get_file, list_files

file_bp = Blueprint('file', __name__)


@file_bp.route('', methods=['POST'])
@file_bp.route('/', methods=['POST'])
@jwt_required()
def upload():
    return upload_file(current_app)


@file_bp.route('', methods=['GET'])
@file_bp.route('/', methods=['GET'])
@jwt_required()
def files():
    return list_files(current_app)

@file_bp.route('/<file_id>', methods=['DELETE'])
@jwt_required()
def remove_file(file_id):
    return delete_file(current_app, file_id)


@file_bp.route('/<file_id>/download', methods=['GET'])
@jwt_required()
def download(file_id):
    return get_file(current_app, file_id)
