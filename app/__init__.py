from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config  # Add this import at the top

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templetes')
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    with app.app_context():
        db.create_all()
    
    return app