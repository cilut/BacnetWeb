from flask import Flask, render_template, request, Blueprint, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["POST"])
def login():
    # Get form information.
    name = request.form.get("user")
    pwd = request.form.get("pwd")
    remember = request.form.get("remember")
    usr = User.query.filter_by(usr=name).first()
    if usr is not None and check_password_hash(usr.password, pwd):
        login_user(usr, remember=remember)
        return jsonify({"success": True})
    return jsonify({"success": False})


@auth.route("/signup")
def show_signup_form():
    return render_template("signup.html")


@auth.route("/signedup", methods=["POST"])
def signedup():
    name = request.form.get("user")
    email = request.form.get("email")
    pwd = request.form.get("pwd")
    usr_db = User.query.filter_by(usr=name).first()
    if usr_db is not None:
        return jsonify({"success": False})
    usr = User(usr=name, password=generate_password_hash(pwd, "sha256"), email=email)
    db.session.add(usr)
    db.session.commit()
    return jsonify({"success": True})


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

