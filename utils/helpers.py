import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, subfolder=''):
    """Save uploaded file with secure filename"""
    if file and allowed_file(file.filename):
        # Create secure filename with unique ID
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Create folder path
        if subfolder:
            folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        else:
            folder_path = current_app.config['UPLOAD_FOLDER']
        
        # Ensure folder exists
        os.makedirs(folder_path, exist_ok=True)
        
        # Save file
        file_path = os.path.join(folder_path, unique_filename)
        file.save(file_path)
        
        # Return relative path for database
        if subfolder:
            return os.path.join('uploads', subfolder, unique_filename)
        else:
            return os.path.join('uploads', unique_filename)
    
    return None

def format_datetime(value, format='%Y-%m-%d %H:%M'):
    """Format datetime for display"""
    if value is None:
        return ''
    return value.strftime(format)