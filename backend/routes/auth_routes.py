from flask import Blueprint, current_app
from flask_jwt_extended import jwt_required
from controllers.auth_controller import (
    register_user,
    login_user,
    profile,
    oauth_start,
    oauth_callback,
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    return register_user(current_app)

@auth_bp.route('/login', methods=['POST'])
def login():
    return login_user(current_app)

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    return profile(current_app)


@auth_bp.route('/oauth/<provider>/start', methods=['GET'])
def oauth_start_route(provider):
    return oauth_start(current_app, provider)


@auth_bp.route('/oauth/google/callback', methods=['GET'])
def google_oauth_callback():
    return oauth_callback(current_app, 'google')


@auth_bp.route('/oauth/github/callback', methods=['GET'])
def github_oauth_callback():
    return oauth_callback(current_app, 'github')
