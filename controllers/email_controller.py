from flask import Blueprint, render_template, request, flash, jsonify, current_app, url_for
from flask_login import login_required, current_user
from services.spam_classifier_service import SpamClassifierService
from models.email_classifier import EmailLog
from utils.helpers import allowed_file, save_uploaded_file
import os
from werkzeug.utils import secure_filename

email_bp = Blueprint('email_controller', __name__)

@email_bp.route('/dashboard')
@login_required
def dashboard():
    # Get user statistics
    stats = SpamClassifierService.get_statistics(current_user.id)
    history = SpamClassifierService.get_user_history(current_user.id, limit=10)
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         history=history,
                         user=current_user)

@email_bp.route('/detect', methods=['GET', 'POST'])
@login_required
def detect():
    if request.method == 'POST':
        email_subject = request.form.get('subject', '')
        email_body = request.form.get('body', '')
        
        if not email_body:
            flash('Please enter email content', 'warning')
            return redirect(url_for('email_controller.detect'))
        
        # Classify email
        result = SpamClassifierService.classify_email(
            email_subject, 
            email_body, 
            current_user.id
        )
        
        return render_template('result.html', result=result)
    
    return render_template('detect.html')

@email_bp.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    logs = EmailLog.query.filter_by(user_id=current_user.id)\
        .order_by(EmailLog.processed_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('history.html', logs=logs)

@email_bp.route('/portfolio')
def portfolio():
    # Get all uploaded portfolio images
    portfolio_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'portfolio')
    images = []
    
    if os.path.exists(portfolio_folder):
        for filename in os.listdir(portfolio_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                images.append({
                    'filename': filename,
                    'path': url_for('static', filename=f'uploads/portfolio/{filename}'),
                    'title': filename.rsplit('.', 1)[0].replace('_', ' ').title()
                })
    
    return render_template('portfolio.html', images=images)

@email_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file selected', 'warning')
            return redirect(request.url)
        
        file = request.files['photo']
        
        if file.filename == '':
            flash('No file selected', 'warning')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Save to portfolio folder
            filename = secure_filename(file.filename)
            portfolio_path = os.path.join('static', 'uploads', 'portfolio')
            os.makedirs(portfolio_path, exist_ok=True)
            
            file_path = os.path.join(portfolio_path, filename)
            file.save(file_path)
            
            flash('Photo uploaded successfully!', 'success')
            return redirect(url_for('email_controller.portfolio'))
        else:
            flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF)', 'danger')
    
    return render_template('upload.html')