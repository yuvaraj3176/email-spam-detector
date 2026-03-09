from services.ml_service import predict_email
from models.email_classifier import EmailLog
from app import db
from flask_login import current_user
from datetime import datetime

class SpamClassifierService:
    
    @staticmethod
    def classify_email(email_subject, email_body, user_id=None):
        """
        Classify an email as spam or ham
        """
        # Combine subject and body for better prediction
        full_text = f"{email_subject} {email_body}" if email_subject else email_body
        
        # Get prediction
        prediction, confidence = predict_email(full_text)
        
        # Save to database if user is logged in
        if user_id:
            log = EmailLog(
                user_id=user_id,
                email_subject=email_subject,
                email_body=email_body[:500],  # Store first 500 chars to save space
                prediction=prediction,
                confidence=confidence
            )
            db.session.add(log)
            db.session.commit()
        
        return {
            'prediction': prediction,
            'confidence': round(confidence, 2),
            'is_spam': prediction == 'spam',
            'processed_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_user_history(user_id, limit=50):
        """Get classification history for a user"""
        logs = EmailLog.query.filter_by(user_id=user_id)\
            .order_by(EmailLog.processed_at.desc())\
            .limit(limit)\
            .all()
        
        return [{
            'id': log.id,
            'subject': log.email_subject,
            'body_preview': log.email_body[:100] + '...' if len(log.email_body) > 100 else log.email_body,
            'prediction': log.prediction,
            'confidence': log.confidence,
            'processed_at': log.processed_at.isoformat()
        } for log in logs]
    
    @staticmethod
    def get_statistics(user_id=None):
        """Get classification statistics"""
        query = EmailLog.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        total = query.count()
        spam_count = query.filter_by(prediction='spam').count()
        ham_count = query.filter_by(prediction='ham').count()
        
        return {
            'total': total,
            'spam': spam_count,
            'ham': ham_count,
            'spam_percentage': round((spam_count / total * 100) if total > 0 else 0, 2)
        }