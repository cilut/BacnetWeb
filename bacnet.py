from flask import Flask, render_template, request, Blueprint, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

bacnet = Blueprint('bacnet', __name__)


@bacnet.route("/load")
@login_required
def load():
    return "carga objetos del usuario"


@bacnet.route("/update")
@login_required
def update():
    return "actualiza datos objeto"


@bacnet.route("/register")
@login_required
def register():
    return "registra objeto bacnet"
