import unittest
import json
from app import create_app, db
from models.user import User

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        # Create test user
        self.user = User(username='testuser', email='test@example.com', role='candidate')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_health_check(self):
        response = self.client.get('/api/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
    
    def test_classify_email(self):
        response = self.client.post('/api/classify', 
            json={
                'subject': 'Test Subject',
                'body': 'This is a test email body'
            }
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', data)
        self.assertIn('confidence', data)
    
    def test_classify_batch(self):
        response = self.client.post('/api/classify-batch',
            json={
                'emails': [
                    {'subject': 'Test 1', 'body': 'Email body 1'},
                    {'subject': 'Test 2', 'body': 'Email body 2'}
                ]
            }
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total'], 2)
        self.assertEqual(len(data['results']), 2)

if __name__ == '__main__':
    unittest.main()