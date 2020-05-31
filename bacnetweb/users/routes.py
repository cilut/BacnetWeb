from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from bacnetweb import mail, db
from bacnetweb.models import User

users = Blueprint("users", __name__)


@users.route("/profile", methods=["GET"])
@login_required
def profile():
    user_log = current_user
    return render_template("profile.html", user=user_log.usr, email=user_log.email)


@users.route("/update", methods=["POST"])
@login_required
def update():
    # Get form information.
    name = request.form.get("users")
    pwd = request.form.get("pwd")
    pwd_new = request.form.get("pwd_new")
    email = request.form.get("email")
    usr = User.query.filter_by(usr=name).first()
    if usr is not None and check_password_hash(usr.password, pwd):
        usr.password = generate_password_hash(pwd_new, "sha256")
        usr.email = email
        db.session.commit()
        return jsonify({"success": True}, )
    return jsonify({"success": False})


@users.route("/reset_pass")
def reset_pass():
    return render_template("reset_pass.html")


@users.route("/send_email", methods=["POST"])
def send_email():
    email = request.form.get("email")
    usr = User.query.filter_by(email=email).first()
    if usr is None:
        return redirect(url_for("main .index"))
    token = usr.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="cipri686@gmail.com",
                  recipients=[email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.new_pass', token=token, _external=True)}
If you did not request this email then simply ignore this email.
    '''
    mail.send(msg)
    return redirect(url_for("main.index"))


@users.route("/new_pass/<token>", methods=['GET', 'POST'])
def new_pass(token):
    usr = User.verify_reset_token(token)
    if request.method == 'GET':
        if usr is None:
            return render_template("error.html")
        return render_template("new_pass.html", token=token)
    pwd_new = request.form.get("pwd_new")
    usr.password = generate_password_hash(pwd_new, "sha256")
    db.session.commit()
    return redirect(url_for("main.index"))
