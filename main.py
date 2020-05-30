from flask import Flask, render_template, request, Blueprint, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template("login.html")
