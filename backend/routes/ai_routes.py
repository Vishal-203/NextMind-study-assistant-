from flask import Blueprint, current_app
from flask_jwt_extended import jwt_required
from controllers.ai_controller import (
    analyze_uploaded_file,
    answer_question,
    summarize_text,
    generate_quiz,
)

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    return answer_question(current_app)

@ai_bp.route('/ask', methods=['POST'])
@jwt_required()
def ask():
    return answer_question(current_app)

@ai_bp.route('/summarize', methods=['POST'])
@jwt_required()
def summarize():
    return summarize_text(current_app)

@ai_bp.route('/quiz', methods=['POST'])
@jwt_required()
def quiz():
    return generate_quiz(current_app)


@ai_bp.route('/analyze-file', methods=['POST'])
@jwt_required()
def analyze_file():
    return analyze_uploaded_file(current_app)
