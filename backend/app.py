import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from .routes.ai_routes import ai_bp
    from .routes.auth_routes import auth_bp
    from .routes.file_routes import file_bp
    from .routes.note_routes import note_bp
    from .routes.share_routes import share_bp
    from .routes.task_routes import task_bp
    from .routes.user_routes import user_bp
except ImportError:
    from routes.ai_routes import ai_bp
    from routes.auth_routes import auth_bp
    from routes.file_routes import file_bp
    from routes.note_routes import note_bp
    from routes.share_routes import share_bp
    from routes.task_routes import task_bp
    from routes.user_routes import user_bp

def _ensure_indexes(app):
    db = app.mongo.db
    try:
        db.users.create_index('email', unique=True, name='users_email_idx')
        db.notes.create_index([('user_id', 1), ('updated_at', -1)], name='notes_user_updated_idx')
        db.notes.create_index('shared_with', name='notes_shared_with_idx')
        db.notes.create_index('subject', name='notes_subject_idx')
        db.notes.create_index('topic', name='notes_topic_idx')
        db.tasks.create_index([('user_id', 1), ('deadline', 1)], name='tasks_user_deadline_idx')
        db.tasks.create_index([('user_id', 1), ('status', 1)], name='tasks_user_status_idx')
        db.files.create_index([('user_id', 1), ('created_at', -1)], name='files_user_created_idx')
    except Exception:
        pass


def create_app():
    load_dotenv(PROJECT_ROOT / '.env', override=True)
    load_dotenv(BASE_DIR / '.env')

    app_env = os.getenv('APP_ENV', os.getenv('FLASK_ENV', 'development')).lower()
    if app_env not in {'development', 'production'}:
        raise RuntimeError("APP_ENV must be either 'development' or 'production'")

    if app_env == 'production':
        required_settings = ('SECRET_KEY', 'JWT_SECRET_KEY', 'MONGO_URI')
        missing_settings = [
            name for name in required_settings
            if not os.getenv(name) or os.getenv(name, '').lower().startswith('replace_with_')
        ]
        if missing_settings:
            raise RuntimeError(
                'Missing required production environment variables: ' + ', '.join(missing_settings)
            )

    secret_key = os.getenv('SECRET_KEY')
    jwt_secret_key = os.getenv('JWT_SECRET_KEY')
    if app_env == 'development':
        secret_key = secret_key or 'development-only-secret'
        jwt_secret_key = jwt_secret_key or secret_key

    app = Flask(
        __name__,
        static_folder=str(PROJECT_ROOT / 'frontend'),
        static_url_path='/'
    )
    app.config['ENVIRONMENT'] = app_env
    app.config['SECRET_KEY'] = secret_key
    app.config['MONGO_URI'] = os.getenv(
        'MONGO_URI',
        'mongodb://localhost:27017/ai_study_assistant'
    )
    app.config['JWT_SECRET_KEY'] = jwt_secret_key

    CORS(app, supports_credentials=True)
    mongo = PyMongo(app)
    jwt = JWTManager(app)

    app.mongo = mongo
    app.jwt = jwt

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(note_bp, url_prefix='/api/notes')
    app.register_blueprint(task_bp, url_prefix='/api/tasks')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(share_bp, url_prefix='/api/notes')
    app.register_blueprint(file_bp, url_prefix='/api/files')

    _ensure_indexes(app)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/api/health')
    def health():
        return {
            'success': True,
            'status': 'healthy',
            'environment': app_env,
            'ai_configured': bool(os.getenv('OPENAI_API_KEY', '').strip()),
        }

    return app


app = create_app()


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('APP_ENV', os.getenv('FLASK_ENV', 'development')).lower() == 'development'
    app.run(host=host, port=port, debug=debug)
