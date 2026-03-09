from app import db
from datetime import datetime

class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email_subject = db.Column(db.String(200))
    email_body = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(20))  # 'spam' or 'ham' (legitimate)
    confidence = db.Column(db.Float)
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EmailLog {self.id}: {self.prediction}>'