import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_file(file):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    # For S3, add upload logic here and return S3 URL
    return f'/uploads/{filename}'
