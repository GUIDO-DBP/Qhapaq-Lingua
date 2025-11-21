import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    SECRET_KEY = 'qhapaq-lingua-secret-key-2024'
    DATABASE_PATH = os.path.join(BASE_DIR, 'qhapaq.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}