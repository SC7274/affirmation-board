import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://affirmation_admin:2025@localhost/affirmation_board'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH_CREDENTIALS = {
        'google': {
            'id': '468392319370-9c5nqqlglf64gc589bl9rcsminupejfb.apps.googleusercontent.com',
            'secret': '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'
        }
    }
