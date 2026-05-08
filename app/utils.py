import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[-1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def save_upload(file, post_id, user_id):
    if not file or not file.filename or not allowed_file(file.filename):
        return None
    from app import db
    from app.models import Media
    ext = file.filename.rsplit('.', 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, unique_name))
    media = Media(
        filename=unique_name,
        original_name=secure_filename(file.filename),
        file_type=ext,
        post_id=post_id,
        uploaded_by=user_id,
    )
    db.session.add(media)
    db.session.commit()
    return media
