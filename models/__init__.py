# This file makes the models directory a Python package
from models.user import User
from models.email_classifier import EmailLog

__all__ = ['User', 'EmailLog']