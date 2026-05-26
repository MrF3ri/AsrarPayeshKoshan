from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    print( app.config['SQLALCHEMY_DATABASE_URI'] )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'لطفا ابتدا وارد شوید.'

    from .routes import routeapi
    from .routesPublic import public
    from .admin import admin_bp   # <-- اضافه شود
    
    app.register_blueprint(routeapi, url_prefix="/")
    app.register_blueprint(public, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin")  # <-- اضافه شود

    return app

# user loader برای flask-login
from .models import Admin

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))
