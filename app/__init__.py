from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://phpmyadmin:sudoferi@localhost/asrarPayeshKoshan'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import routeapi
    from .routesPublic import public
    
    app.register_blueprint(routeapi, url_prefix="/")
    app.register_blueprint(public, url_prefix="/api")
    

    return app
