# cSpell:ignore sqlalchemy jsonify wtforms newsalchemyuser yourpassword

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY_TABLE = 'sessions'