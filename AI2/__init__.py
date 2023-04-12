from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

db = SQLAlchemy()
#DB_NAME = "database.db"
DB_NAME = "cclmpr"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hthththththt'
    DATABASE_URL = f"mysql+pymysql://admin:12345678@cclmpr.cenrv2a3hx41.ap-south-1.rds.amazonaws.com:3306/{DB_NAME}"
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #from .models import user
    from .models import User, Note
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('AI2/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')


# AI se start hoga
# python manage.py startapp AI
