import os

from flask import Flask, render_template, request

from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin


mail = Mail()
login_manager = LoginManager()
admin = Admin()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'prueba'
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("USER_GMAIL")
    app.config["MAIL_PASSWORD"] = os.getenv("PASS_GMAIL")

    mail.init_app(app)

    from .models import db, User, MyModelView
    db.init_app(app)

    admin.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    admin.add_view(MyModelView(User, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .user import usr as usr_blueprint
    app.register_blueprint(usr_blueprint)

    from .bacnet import bacnet as bacnet_blueprint
    app.register_blueprint(bacnet_blueprint)

    return app
