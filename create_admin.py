#!/usr/bin/env python
from app import create_app, db
from models.user import User

def create_admin_user():
    app = create_app('development')
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
        
        # Create a test candidate
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
            print("Candidate user created successfully!")
        else:
            print("Candidate user already exists.")

if __name__ == '__main__':
    create_admin_user()