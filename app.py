from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import config
import os
import nltk
import warnings
warnings.filterwarnings('ignore')

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_controller.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import models here to avoid circular imports
    from models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Ensure upload folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join('static', 'uploads', 'portfolio'), exist_ok=True)
    
    # Register blueprints
    from controllers.auth_controller import auth_bp
    from controllers.email_controller import email_bp
    from controllers.api_controller import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Train the ML model on startup
        from services.ml_service import train_model
        train_model()
        
        # Create default admin user if not exists
        from models.user import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
        # Create default candidate user if not exists
        candidate = User.query.filter_by(username='candidate').first()
        if not candidate:
            candidate = User(
                username='candidate',
                email='candidate@example.com',
                role='candidate'
            )
            candidate.set_password('candidate123')
            db.session.add(candidate)
            
        db.session.commit()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)