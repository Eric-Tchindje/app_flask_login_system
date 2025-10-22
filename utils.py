import os
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


def save_uploaded_image(image_file, old_image_path=None):
    """Save uploaded image to UPLOAD_FOLDER, remove old image if provided, and return relative DB path."""
    if not image_file or image_file.filename == '':
        return old_image_path  # nothing uploaded

    # Validate extension
    if not allowed_file(image_file.filename):
        raise ValueError('Invalid image format! Allowed: png, jpg, jpeg, gif.')

    # Remove old image if it exists
    if old_image_path:
        old_image_abs = os.path.join(current_app.root_path, old_image_path)
        if os.path.exists(old_image_abs):
            os.remove(old_image_abs)

    # Save new image
    filename = secure_filename(image_file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)
    image_file.save(file_path)

    # Return the relative path for DB storage (for serving via `static`)
    return f'uploads/{filename}'
