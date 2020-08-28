from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user

from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from bacnetweb import mail, db
from bacnetweb.models import User

from bacnetweb.forms.routes import UpdateForm, ResetPassForm, ChangePassForm

users = Blueprint('users', __name__)


@users.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('auxiliar/about.html')


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.password.data):
            current_user.password = generate_password_hash(form.password_new.data, "sha256")
            current_user.email = form.email.data
            db.session.add(current_user)
            db.session.commit()
            flash(f'Account updated for {current_user.usr}', 'success')
            return render_template('user/profile.html', title='Account', form=form)
        else:
            flash('Update unsuccessful. Please check password', 'danger')
    return render_template('user/profile.html', title='Account', form=form)


@users.route("/reset_pass", methods=['GET', 'POST'])
def reset_pass():
    form = ResetPassForm()

    if form.validate_on_submit():
        usr = User.query.filter_by(email=form.email.data, usr=form.username.data).first()
        if usr is None:
            flash(f'If there is an account that matches the user and the email check your mailbox ', 'success')
            return redirect(url_for("main.index"))
        token = usr.get_reset_token()
        msg = Message("Password Reset Request",
                      sender="cipri686@gmail.com",
                      recipients=[form.email.data])
        msg.body = f''' To reset your password, visit the following link:
{url_for('users.new_pass', token=token, _external=True)}
If you did not request this email then simply ignore this email.
            '''
        mail.send(msg)
        flash(f'If there is an account that matches the user and the email check your mailbox ', 'success')
        return redirect(url_for("main.index"))
    return render_template("signup/reset_pass.html", form=form)


@users.route("/new_pass/<token>", methods=['GET', 'POST'])
def new_pass(token):
    usr = User.verify_reset_token(token)
    form = ChangePassForm()
    if form.validate_on_submit():
        usr.password = generate_password_hash(form.password_new.data, "sha256")
        db.session.add(usr)
        db.session.commit()
        flash(f'Password updated properly for user:  {usr.usr}', 'success')
        return redirect(url_for("main.index"))
    return render_template('signup/new_pass.html', title='Account', form=form)

