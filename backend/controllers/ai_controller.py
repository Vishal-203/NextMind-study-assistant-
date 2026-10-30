import os

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from openai import OpenAI

from controllers.file_analyzer import extract_text_from_file
from utils.helpers import parse_object_id, resp


CONTEXTUAL_STUDY_ASSISTANT_PROMPT = (
    "You are a helpful AI study assistant.\n"
    "- Use the provided study material as your primary context when it is available.\n"
    "- If notes or uploaded material are provided, prioritize them in your answer.\n"
    "- You may use general knowledge when the context is incomplete or the user asks beyond it.\n"
    "- Keep answers clear, relevant, and concise unless the user asks for detail."
)


def get_ai_client():
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if not api_key:
        return None
    base_url = os.getenv('OPENAI_BASE_URL', '').strip()
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def get_ai_model():
    return os.getenv('OPENAI_MODEL', 'allam-2-7b').strip() or 'allam-2-7b'


def _normalize_context_text(text):
    return ' '.join(text.split()).strip() if isinstance(text, str) else ''


def _request_text(data, *keys):
    for key in keys:
        value = data.get(key)
        if isinstance(value, str):
            value = value.strip()
            if value:
                return value
    return ''


def _build_contextual_messages(message, study_material):
    return [
        {'role': 'system', 'content': CONTEXTUAL_STUDY_ASSISTANT_PROMPT},
        {
            'role': 'user',
            'content': (
                "Study material:\n"
                f"{study_material}\n\n"
                "Student question:\n"
                f"{message}"
            )
        }
    ]


def _build_general_messages(message):
    return [
        {
            'role': 'system',
            'content': 'You are a helpful academic assistant. Answer clearly and concisely.'
        },
        {'role': 'user', 'content': message}
    ]


def _build_note_context(note):
    parts = []
    subject = (note.get('subject') or '').strip()
    topic = (note.get('topic') or '').strip()
    content = (note.get('content') or '').strip()
    tags = note.get('tags') or []

    if subject:
        parts.append(f"Subject: {subject}")
    if topic:
        parts.append(f"Topic: {topic}")
    if tags:
        parts.append("Tags: " + ', '.join(str(tag) for tag in tags if str(tag).strip()))
    if content:
        parts.append("Note content:\n" + content)

    return '\n\n'.join(part for part in parts if part.strip())


def _get_note_context(app, note_id):
    note_obj_id = parse_object_id(note_id, 'note_id')
    if note_obj_id is None:
        return {'success': False, 'message': 'Invalid note ID', 'status': 400}

    user_id = get_jwt_identity()
    note = app.mongo.db.notes.find_one({'_id': note_obj_id, 'user_id': user_id})
    if not note:
        note = app.mongo.db.notes.find_one({'_id': note_obj_id, 'shared_with': user_id})
    if not note:
        return {'success': False, 'message': 'Note not found', 'status': 404}

    note_text = _build_note_context(note)
    normalized = _normalize_context_text(note_text)
    if not normalized:
        return {'success': False, 'message': 'Selected note has no readable content', 'status': 400}

    return {'success': True, 'data': {'text': normalized}}


def _combine_context_parts(parts):
    cleaned = [part for part in (_normalize_context_text(part) for part in parts) if part]
    return '\n\n'.join(cleaned)


def analyze_uploaded_file(app):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return resp(False, 'A JSON request body is required', status=400)

    file_id = data.get('file_id')
    if not isinstance(file_id, str) or not file_id.strip():
        return resp(False, 'file_id is required', status=400)

    result = extract_text_from_file(app, file_id.strip())
    if not result.get('success'):
        return resp(False, result.get('message', 'File analysis failed'), status=result.get('status', 400))

    extracted = result['data']
    return resp(True, 'File analyzed successfully', {
        'filename': extracted['filename'],
        'text': extracted['text'],
        'character_count': len(extracted['text'])
    })


def _build_summary_prompt(text):
    return (
        'Summarize the following text in 3-4 bullet points, keeping the summary clear and concise.\n\n' +
        text
    )


@jwt_required()
def answer_question(app):
    data = request.get_json() or {}
    question = _request_text(data, 'message', 'question')
    file_id = data.get('file_id')
    note_id = data.get('note_id')
    direct_context = _normalize_context_text(
        data.get('content') or data.get('study_material') or data.get('extracted_text')
    )

    if not question:
        return resp(False, 'Question is required', status=400)

    context_parts = [direct_context]
    if note_id:
        note_result = _get_note_context(app, note_id)
        if not note_result.get('success'):
            return resp(
                False,
                note_result.get('message', 'Note context failed'),
                status=note_result.get('status', 400)
            )
        context_parts.append(note_result['data']['text'])

    if file_id:
        file_result = extract_text_from_file(app, file_id)
        if not file_result.get('success'):
            return resp(
                False,
                file_result.get('message', 'File extraction failed'),
                status=file_result.get('status', 400)
            )
        context_parts.append(file_result['data']['text'])

    context_text = _combine_context_parts(context_parts)

    client = get_ai_client()
    if client is None:
        return resp(False, 'AI service is not configured', status=503)

    try:
        response = client.chat.completions.create(
            model=get_ai_model(),
            messages=(
                _build_contextual_messages(question, context_text)
                if context_text
                else _build_general_messages(question)
            ),
            max_tokens=400,
            temperature=0.4 if context_text else 0.7
        )
        ans = response.choices[0].message.content.strip()
        return resp(True, 'Answer generated', {'answer': ans})
    except Exception as e:
        return resp(False, f'AI service error: {str(e)}', status=500)


@jwt_required()
def summarize_text(app):
    data = request.get_json() or {}
    text = _request_text(data, 'text')
    file_id = data.get('file_id')
    note_id = data.get('note_id')

    if note_id:
        note_result = _get_note_context(app, note_id)
        if not note_result.get('success'):
            return resp(
                False,
                note_result.get('message', 'Note context failed'),
                status=note_result.get('status', 400)
            )
        text = note_result['data']['text']

    if file_id:
        file_result = extract_text_from_file(app, file_id)
        if not file_result.get('success'):
            return resp(False, file_result.get('message', 'File extraction failed'), status=file_result.get('status', 400))
        text = file_result['data']['text']

    if not text:
        return resp(False, 'Text, file_id, or note_id is required', status=400)

    client = get_ai_client()
    if client is None:
        return resp(False, 'AI service is not configured', status=503)

    try:
        prompt = _build_summary_prompt(text)
        response = client.chat.completions.create(
            model=get_ai_model(),
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant. Summarize the given text in 3-4 bullet points.'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        summary = response.choices[0].message.content.strip()
        return resp(True, 'Summary generated', {'summary': summary})
    except Exception as e:
        return resp(False, f'AI service error: {str(e)}', status=500)


@jwt_required()
def generate_quiz(app):
    data = request.get_json() or {}
    topic = _request_text(data, 'topic')
    if not topic:
        return resp(False, 'Topic is required', status=400)

    client = get_ai_client()
    if client is None:
        return resp(False, 'AI service is not configured', status=503)

    try:
        response = client.chat.completions.create(
            model=get_ai_model(),
            messages=[
                {'role': 'system', 'content': 'You are an educational assistant. Create a 5-question academic quiz with answers for the given topic.'},
                {'role': 'user', 'content': f'Create a quiz on: {topic}'}
            ],
            max_tokens=500,
            temperature=0.6
        )
        quiz = response.choices[0].message.content.strip()
        return resp(True, 'Quiz generated', {'quiz': quiz})
    except Exception as e:
        return resp(False, f'AI service error: {str(e)}', status=500)
