import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sec-log-super-secret-key-2026-change-in-prod'
    DATABASE = os.path.join(BASE_DIR, 'database', 'securelog.db')
    DEBUG = True