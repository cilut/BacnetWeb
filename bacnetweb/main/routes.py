from flask import render_template, Blueprint


main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/struct")
def struct():
    return render_template("auxiliar/struct.html")