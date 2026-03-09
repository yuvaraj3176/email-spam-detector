# 🔒Enterprise Email Spam & Phishing Detection 

📋 Overview
Enterprise-grade web app for detecting spam/phishing emails using NLP & Machine Learning. Real-time classification with 95%+ accuracy.

✨ Features
🔐 Authentication
Role-based access (Admin/Candidate)

Secure register/login system

Session management

🤖 AI Detection
Real-time email classification

NLP preprocessing

Confidence scoring

ML model (Naive Bayes)

📊 Dashboard
Visual analytics with charts

Detection history

User statistics

Activity tracking

🖼️ Portfolio
Image upload gallery

Responsive design

Admin moderation

🔌 5 REST APIs
Health check

Single/Batch classification

User statistics

Admin analytics

🛠️ Tech Stack
Layer	Technologies
Backend	Python 3.8+, Flask, Flask-Login, SQLAlchemy
ML/NLP	scikit-learn, NLTK, Pandas, NumPy
Frontend	Bootstrap 5, JavaScript, Chart.js
Database	SQLite (dev), PostgreSQL (prod)
📥 Installation
bash
# Clone repo
git clone https://github.com/yourusername/email-spam-detector.git
cd email-spam-detector

# Virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Initialize database
python create_admin.py

# Run application
python run.py
Access at: http://localhost:5000

🔑 Default Users
Role	Username	Password
👑 Admin	admin	admin123
👤 Candidate	candidate	candidate123
📡 API Endpoints
Method	Endpoint	Description
GET	/api/health	Health check
POST	/api/classify	Single email
POST	/api/classify-batch	Batch emails
GET	/api/statistics	User stats
GET	/api/admin/stats	Admin stats
🧠 ML Model
Algorithm: Multinomial Naive Bayes

Vectorization: TF-IDF (5000 features)

Preprocessing: Lemmatization, stopword removal

Accuracy: 95%+

🧪 Testing
bash
python -m pytest tests/
🚀 Quick Deploy
Gunicorn
bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
Docker
bash
docker build -t spam-detector .
docker run -p 5000:5000 spam-detector
📁 Project Structure
text
email-spam-detector/
├── app.py              # Main app
├── run.py              # Runner
├── config.py           # Configs
├── requirements.txt    # Dependencies
├── models/             # DB models
├── controllers/        # Routes
├── services/           # Business logic
├── templates/          # HTML
├── static/            # CSS/JS/Images
├── tests/             # Unit tests
└── utils/             # Helpers
🤝 Contributing
Fork 🍴

Branch: git checkout -b feature/AmazingFeature

Commit: git commit -m 'Add feature'

Push: git push origin feature/AmazingFeature

Pull Request 📬


<img width="1920" height="1080" alt="Screenshot 2026-03-09 132446" src="https://github.com/user-attachments/assets/8a0ece28-d51f-49fa-8863-563e8e772056" />
<img width="1920" height="1080" alt="Screenshot 2026-03-09 132528" src="https://github.com/user-attachments/assets/ade3e9ed-b4fd-4abd-ba17-1cbcd4190b7d" />
<img width="1920" height="1080" alt="Screenshot 2026-03-09 133013" src="https://github.com/user-attachments/assets/9d3d7869-9976-496f-9d80-e6e95172a730" />
<img width="1920" height="1080" alt="Screenshot 2026-03-09 134034" src="https://github.com/user-attachments/assets/7510169b-1830-4797-a7ab-135d1d401bad" />
