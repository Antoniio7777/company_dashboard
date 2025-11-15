import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    TALISMAN_CONTENT_SECURITY_POLICY = {
        'default-src': "'self'",
        'style-src': [
            "'self'",
            "https://cdn.jsdelivr.net",
            "'unsafe-inline'"
        ],
        'script-src': [
            "'self'",
            "https://cdn.jsdelivr.net",
        ],
        'font-src': "https://cdn.jsdelivr.net"
    }

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    TESTING = False
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}