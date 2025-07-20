from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from utils.media import save_file

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    url = save_file(file)
    return jsonify({'url': url})
