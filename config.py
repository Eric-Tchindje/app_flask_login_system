import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (only locally)
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class BaseConfig:
    """Base configuration shared by all environments"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'static', 'uploads'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH_MB', 2)) * 1024 * 1024  # in MB
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif').split(','))


class DevelopmentConfig(BaseConfig):
    """Development (local) configuration - uses MySQL"""
    DEBUG = True
    TESTING = True

    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'admin')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'pythonlogin')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    )


class ProductionConfig(BaseConfig):
    """Production configuration - uses PostgreSQL"""
    DEBUG = False
    TESTING = False

    # Use PostgreSQL from Render (DATABASE_URL)
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        # SQLAlchemy requires postgresql:// instead of postgres://
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
