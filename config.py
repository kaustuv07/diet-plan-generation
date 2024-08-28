# config.py

class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Adjust the URI as needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False
