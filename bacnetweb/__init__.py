from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_admin import Admin
from bacnetweb.config import Config


db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
admin = Admin()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    from bacnetweb.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from bacnetweb.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from bacnetweb.users.routes import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from bacnetweb.bacnet.routes import bacnet as bacnet_blueprint
    app.register_blueprint(bacnet_blueprint)

    return app
