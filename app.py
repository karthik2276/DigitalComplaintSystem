import os
from flask import Flask
from models import db, bcrypt, login_manager
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey123') 
    
    # Use absolute path for sqlite database or DATABASE_URL if in production
    basedir = os.path.abspath(os.path.dirname(__name__))
    db_path = os.path.join(basedir, 'database', 'complaints.db')
    default_db_uri = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', default_db_uri)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # File upload config
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB limit
    
    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'
    
    # Create tables before first request
    with app.app_context():
        # importing routes here to avoid circular imports
        from routes import main_bp
        app.register_blueprint(main_bp)
        
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
