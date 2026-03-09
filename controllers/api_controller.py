from models.email_classifier import EmailLog
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.spam_classifier_service import SpamClassifierService
from models.user import User
from app import db
import re

api_bp = Blueprint('api_controller', __name__)

# API 1: Health Check
@api_bp.route('/health', methods=['GET'])
def health_check():
    """API endpoint to check if the service is running"""
    return jsonify({
        'status': 'healthy',
        'message': 'Email Spam Detector API is running',
        'version': '1.0.0'
    }), 200

# API 2: Single Email Classification
@api_bp.route('/classify', methods=['POST'])
def classify_email():
    """API endpoint to classify a single email"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email_subject = data.get('subject', '')
    email_body = data.get('body', '')
    
    if not email_body:
        return jsonify({'error': 'Email body is required'}), 400
    
    # Get user_id if authenticated
    user_id = current_user.id if current_user.is_authenticated else None
    
    result = SpamClassifierService.classify_email(
        email_subject, 
        email_body, 
        user_id
    )
    
    return jsonify(result), 200

# API 3: Batch Email Classification
@api_bp.route('/classify-batch', methods=['POST'])
def classify_batch():
    """API endpoint to classify multiple emails at once"""
    data = request.get_json()
    
    if not data or 'emails' not in data:
        return jsonify({'error': 'No emails provided'}), 400
    
    emails = data['emails']
    
    if not isinstance(emails, list):
        return jsonify({'error': 'Emails must be a list'}), 400
    
    results = []
    user_id = current_user.id if current_user.is_authenticated else None
    
    for email in emails:
        subject = email.get('subject', '')
        body = email.get('body', '')
        
        if body:
            result = SpamClassifierService.classify_email(subject, body, user_id)
            results.append(result)
    
    return jsonify({
        'total': len(results),
        'results': results
    }), 200

# API 4: User Statistics
@api_bp.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """API endpoint to get classification statistics for the current user"""
    stats = SpamClassifierService.get_statistics(current_user.id)
    
    # Add user info
    stats['username'] = current_user.username
    stats['email'] = current_user.email
    
    return jsonify(stats), 200

# API 5: Admin Dashboard Statistics (requires admin)
@api_bp.route('/admin/stats', methods=['GET'])
@login_required
def admin_statistics():
    """API endpoint for admin to get system-wide statistics"""
    if not current_user.is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    # Get system-wide statistics
    total_users = User.query.count()
    total_classifications = EmailLog.query.count()
    
    # Get admin-specific stats
    from sqlalchemy import func
    
    # Classifications by user
    top_users = db.session.query(
        User.username, 
        func.count(EmailLog.id).label('count')
    ).join(EmailLog).group_by(User.id).order_by(func.count(EmailLog.id).desc()).limit(5).all()
    
    # Recent classifications
    recent = EmailLog.query.order_by(EmailLog.processed_at.desc()).limit(10).all()
    
    return jsonify({
        'total_users': total_users,
        'total_classifications': total_classifications,
        'top_users': [{'username': u, 'count': c} for u, c in top_users],
        'recent_classifications': [{
            'id': log.id,
            'user': log.user.username,
            'prediction': log.prediction,
            'confidence': log.confidence,
            'processed_at': log.processed_at.isoformat()
        } for log in recent]
    }), 200