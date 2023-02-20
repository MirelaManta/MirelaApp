# __init__.py makes the website folder a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
# DB_NAME = "database.db"
# Changed database to not be hardcoded anymore


def create_app(db_name="database.db"):
    app = Flask(__name__)        # it initializes the app
    app.config['SECRET_KEY'] = 'no one should see this'   # this is the secret key for my app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'  # my sqlalchemy database is stored at this location <--
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app, db_name)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # it tells us where flask should redirect us if we're not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


def create_database(app, db_name="database.db"):
    if not path.exists('instance/' + db_name):
        with app.app_context():
            db.create_all()
            print('Created Database!')

