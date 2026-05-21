import os
import pathlib
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey123')
    
    # Database Configuration
    db_path = os.path.join(basedir, 'database', 'complaints.db')
    default_db_uri = f"sqlite:///{pathlib.Path(os.path.abspath(db_path)).as_posix()}"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default_db_uri)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads Configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB limit
