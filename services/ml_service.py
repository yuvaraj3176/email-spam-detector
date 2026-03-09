import pandas as pd
import numpy as np
import nltk
import re
import os
import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Global variables for model and vectorizer
model = None
vectorizer = None
pipeline = None

def preprocess_text(text):
    """Clean and preprocess text data"""
    if not isinstance(text, str):
        text = str(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize and lemmatize
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    
    return ' '.join(words)

def create_sample_dataset():
    """Create a sample dataset for training"""
    data = {
        'text': [
            # Spam examples
            "Congratulations! You've won a free iPhone. Click here to claim your prize now!",
            "URGENT: Your account has been compromised. Verify your details immediately.",
            "Make $5000 per week working from home! Limited time offer.",
            "You have been selected for a free vacation to Bahamas. Call now!",
            "Dear customer, your PayPal account needs verification. Click the link below.",
            "Get viagra at 80% discount. Order now and get free shipping.",
            "Your tax refund is pending. Submit your information to receive payment.",
            "Nigerian prince needs your help to transfer millions. You'll get 30%.",
            "Increase your chances with our miracle pills. 100% guaranteed.",
            "Last chance to claim your lottery winnings of $1,000,000!",
            
            # Ham (legitimate) examples
            "Hi team, please find attached the quarterly report for review.",
            "Can we schedule a meeting for tomorrow at 2 PM to discuss the project?",
            "Your order #12345 has been shipped and will arrive in 3-5 business days.",
            "Thank you for subscribing to our newsletter. You'll receive weekly updates.",
            "Meeting minutes from today's standup: John will work on the frontend.",
            "Please remember to submit your timesheet by Friday 5 PM.",
            "The code review for pull request #567 is complete. Good work!",
            "Lunch is served in the cafeteria from 12-2 PM today.",
            "Your password was successfully changed. If this wasn't you, contact support.",
            "The Jenkins build for branch main has failed. Please check the logs."
        ],
        'label': [
            'spam', 'spam', 'spam', 'spam', 'spam',
            'spam', 'spam', 'spam', 'spam', 'spam',
            'ham', 'ham', 'ham', 'ham', 'ham',
            'ham', 'ham', 'ham', 'ham', 'ham'
        ]
    }
    
    # Create more variations
    texts = []
    labels = []
    
    for i in range(50):  # Create 50 samples
        for text, label in zip(data['text'], data['label']):
            texts.append(text)
            labels.append(label)
            
            # Add variations for spam
            if label == 'spam':
                texts.append(text + " Don't miss out!")
                labels.append('spam')
                texts.append("FREE: " + text)
                labels.append('spam')
            else:
                texts.append("RE: " + text)
                labels.append('ham')
                texts.append("FWD: " + text)
                labels.append('ham')
    
    return pd.DataFrame({'text': texts, 'label': labels})

def train_model():
    """Train the spam classification model"""
    global model, vectorizer, pipeline
    
    # Create dataset
    df = create_sample_dataset()
    
    # Preprocess texts
    print("Preprocessing texts...")
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_text'], df['label'], test_size=0.2, random_state=42, stratify=df['label']
    )
    
    # Create pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ('classifier', MultinomialNB(alpha=0.1))
    ])
    
    # Train model
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'spam_classifier.pkl')
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")
    
    return pipeline

def load_model():
    """Load the trained model"""
    global pipeline
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'spam_classifier.pkl')
    
    if os.path.exists(model_path):
        pipeline = joblib.load(model_path)
        print("Model loaded successfully")
    else:
        print("Model not found. Training new model...")
        pipeline = train_model()
    
    return pipeline

def predict_email(text):
    """Predict if an email is spam or ham"""
    global pipeline
    
    if pipeline is None:
        pipeline = load_model()
    
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Make prediction
    prediction = pipeline.predict([processed_text])[0]
    
    # Get probability
    probabilities = pipeline.predict_proba([processed_text])[0]
    confidence = max(probabilities) * 100
    
    return prediction, confidence

# Initialize model on import
pipeline = load_model()