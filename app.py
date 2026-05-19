import os
from flask import Flask
from models import db, bcrypt, login_manager
from config import Config

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
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
