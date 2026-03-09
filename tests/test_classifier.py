import unittest
from services.ml_service import preprocess_text, predict_email, train_model
from services.spam_classifier_service import SpamClassifierService

class ClassifierTestCase(unittest.TestCase):
    def setUp(self):
        # Train model before tests
        self.pipeline = train_model()
    
    def test_preprocess_text(self):
        text = "Hello! This is a TEST email with numbers 123 and symbols @#$."
        processed = preprocess_text(text)
        
        self.assertIsInstance(processed, str)
        self.assertNotIn('!', processed)
        self.assertNotIn('123', processed)
        self.assertNotIn('@', processed)
    
    def test_spam_prediction(self):
        spam_text = "Congratulations! You've won a free iPhone! Click here to claim now!"
        prediction, confidence = predict_email(spam_text)
        
        self.assertEqual(prediction, 'spam')
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 100)
    
    def test_ham_prediction(self):
        ham_text = "Hi team, please find attached the quarterly report for review."
        prediction, confidence = predict_email(ham_text)
        
        self.assertEqual(prediction, 'ham')
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 100)
    
    def test_classifier_service(self):
        result = SpamClassifierService.classify_email(
            "Test Subject",
            "This is a test email body"
        )
        
        self.assertIn('prediction', result)
        self.assertIn('confidence', result)
        self.assertIn('is_spam', result)

if __name__ == '__main__':
    unittest.main()