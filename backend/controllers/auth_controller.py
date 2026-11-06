import json
import os
import secrets
import urllib.parse
import urllib.request
from flask import request, redirect, session, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from utils.helpers import check_password, hash_password, parse_object_id, resp


def register_user(app):
    body = request.get_json() or {}
    name = body.get('name', '').strip()
    email = body.get('email', '').strip().lower()
    password = body.get('password', '')

    if not name or not email or not password:
        return resp(False, 'Name, email, and password are required', status=400)

    if app.mongo.db.users.find_one({'email': email}):
        return resp(False, 'User already exists', status=409)

    user = {
        'name': name,
        'email': email,
        'password': hash_password(password),
        'created_at': datetime.utcnow()
    }
    user_id = app.mongo.db.users.insert_one(user).inserted_id
    return resp(True, 'User registered', {'user_id': str(user_id)})


def login_user(app):
    body = request.get_json() or {}
    email = body.get('email', '').strip().lower()
    password = body.get('password', '')

    if not email or not password:
        return resp(False, 'Email and password are required', status=400)

    user = app.mongo.db.users.find_one({'email': email})
    if not user or not user.get('password') or not check_password(password, user['password']):
        return resp(False, 'Invalid credentials', status=401)

    token = create_access_token(identity=str(user['_id']))
    return resp(True, 'Login successful', {'token': token, 'user': {'id': str(user['_id']), 'name': user['name'], 'email': user['email']}})


def _oauth_redirect_uri(provider):
    configured = os.getenv(f'{provider.upper()}_REDIRECT_URI', '').strip()
    if configured:
        return configured
    return url_for(f'auth.{provider}_oauth_callback', _external=True)


def _oauth_http_json(url, data=None, headers=None):
    request_headers = dict(headers or {})
    if data is not None:
        encoded_data = urllib.parse.urlencode(data).encode()
        request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    else:
        encoded_data = None
    oauth_request = urllib.request.Request(url, data=encoded_data, headers=request_headers)
    with urllib.request.urlopen(oauth_request, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))


def _oauth_error(message):
    session.pop('oauth_state', None)
    session.pop('oauth_provider', None)
    return redirect('/index.html?oauth_error=' + urllib.parse.quote(message))


def oauth_start(app, provider):
    provider = provider.lower()
    if provider not in {'google', 'github'}:
        return _oauth_error('Unsupported OAuth provider')

    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    session['oauth_provider'] = provider

    if provider == 'google':
        client_id = os.getenv('GOOGLE_CLIENT_ID', '').strip()
        if not client_id:
            return _oauth_error('Google OAuth is not configured')
        params = urllib.parse.urlencode({
            'client_id': client_id,
            'redirect_uri': _oauth_redirect_uri('google'),
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'prompt': 'select_account',
        })
        return redirect('https://accounts.google.com/o/oauth2/v2/auth?' + params)

    if provider == 'github':
        client_id = os.getenv('GITHUB_CLIENT_ID', '').strip()
        if not client_id:
            return _oauth_error('GitHub OAuth is not configured')
        params = urllib.parse.urlencode({
            'client_id': client_id,
            'redirect_uri': _oauth_redirect_uri('github'),
            'scope': 'read:user user:email',
            'state': state,
        })
        return redirect('https://github.com/login/oauth/authorize?' + params)

    return _oauth_error('Unsupported OAuth provider')


def oauth_callback(app, provider):
    provider = provider.lower()
    if request.args.get('error'):
        return _oauth_error(request.args['error'])
    if (
        request.args.get('state') != session.get('oauth_state')
        or session.get('oauth_provider') != provider
    ):
        return _oauth_error('Invalid OAuth state')

    code = request.args.get('code')
    if not code:
        return _oauth_error('OAuth code was not returned')

    try:
        if provider == 'google':
            client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '').strip()
            token = _oauth_http_json('https://oauth2.googleapis.com/token', {
                'client_id': os.getenv('GOOGLE_CLIENT_ID', '').strip(),
                'client_secret': client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': _oauth_redirect_uri('google'),
            })
            if not token.get('access_token'):
                raise ValueError('Google did not return an access token')
            profile = _oauth_http_json(
                'https://openidconnect.googleapis.com/v1/userinfo',
                headers={'Authorization': 'Bearer ' + token['access_token']},
            )
            email = (profile.get('email') or '').strip().lower()
            name = (profile.get('name') or email.split('@')[0]).strip()
            provider_id = profile.get('sub')
            if profile.get('email_verified') is not True or not provider_id:
                raise ValueError('Google did not provide a verified account email')
        else:
            token = _oauth_http_json('https://github.com/login/oauth/access_token', {
                'client_id': os.getenv('GITHUB_CLIENT_ID', '').strip(),
                'client_secret': os.getenv('GITHUB_CLIENT_SECRET', '').strip(),
                'code': code,
                'redirect_uri': _oauth_redirect_uri('github'),
            }, {'Accept': 'application/json'})
            if not token.get('access_token'):
                raise ValueError(token.get('error_description') or 'GitHub did not return an access token')
            headers = {
                'Authorization': 'Bearer ' + token['access_token'],
                'Accept': 'application/vnd.github+json',
                'User-Agent': 'NextMind',
            }
            profile = _oauth_http_json('https://api.github.com/user', headers=headers)
            email = (profile.get('email') or '').strip().lower()
            if not email:
                emails = _oauth_http_json('https://api.github.com/user/emails', headers=headers)
                email = next((item['email'].lower() for item in emails if item.get('primary') and item.get('verified')), '')
            name = (profile.get('name') or profile.get('login') or email.split('@')[0]).strip()
            provider_id = str(profile.get('id', ''))
            if not provider_id:
                raise ValueError('GitHub did not provide an account ID')
    except Exception as exc:
        return _oauth_error(str(exc))

    if not email:
        return _oauth_error('Provider email is not available')

    query = {f'oauth_{provider}_id': provider_id}
    user = app.mongo.db.users.find_one({'$or': [{'email': email}, query]})
    if user:
        app.mongo.db.users.update_one({'_id': user['_id']}, {'$set': query | {'email': email, 'name': name}})
    else:
        result = app.mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'oauth_provider': provider,
            **query,
            'created_at': datetime.utcnow(),
        })
        user = app.mongo.db.users.find_one({'_id': result.inserted_id})

    session.pop('oauth_state', None)
    session.pop('oauth_provider', None)
    token = create_access_token(identity=str(user['_id']))
    user_data = json.dumps({
        'id': str(user['_id']),
        'name': name,
        'email': email,
    }, separators=(',', ':'))
    return redirect('/dashboard.html#oauth_token=' + urllib.parse.quote(token, safe='')
                    + '&oauth_user=' + urllib.parse.quote(user_data, safe=''))


@jwt_required()
def profile(app):
    user_id = get_jwt_identity()
    user_obj_id = parse_object_id(user_id, 'user_id')
    if user_obj_id is None:
        return resp(False, 'Invalid user ID', status=400)

    user = app.mongo.db.users.find_one({'_id': user_obj_id}, {'password': False})
    if not user:
        return resp(False, 'User not found', status=404)
    user['id'] = str(user['_id'])
    del user['_id']
    return resp(True, 'Profile fetched', user)
