from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from bacnetweb import db
from bacnetweb.forms.routes import LoginForm, SignupForm
from bacnetweb.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    form = LoginForm()

    if form.validate_on_submit():
        usr = User.query.filter_by(usr=form.username.data).first()
        if usr and check_password_hash(usr.password, form.password.data):
            login_user(usr, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login/login.html", title='Login', form=form)


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    form = SignupForm()
    if form.validate_on_submit():
        usr = User(usr=form.username.data, password=generate_password_hash(form.password.data, "sha256"),
                   email=form.email.data, admin=False)
        db.session.add(usr)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup/signup.html', title='Signup', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
