from flask import Blueprint, render_template

bp = Blueprint("landing", __name__, template_folder="../templates")

@bp.get("/")
def index():
    # A simple homepage: providing login options for four different roles.

    return render_template("index.html")
