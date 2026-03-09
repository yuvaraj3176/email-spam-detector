import unittest
from app import create_app, db
from models.user import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_registration(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'role': 'candidate'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
    
    def test_user_login(self):
        # Create user first
        user = User(username='testuser', email='test@example.com', role='candidate')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Test login
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
    
    def test_invalid_login(self):
        response = self.client.post('/login', data={
            'username': 'nonexistent',
            'password': 'wrongpass'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

if __name__ == '__main__':
    unittest.main()