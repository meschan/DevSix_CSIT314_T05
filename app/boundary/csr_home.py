# app/boundary/csr_home.py
from flask import Blueprint, render_template, session, redirect, url_for

bp = Blueprint("csr_home", __name__, template_folder="../templates")

@bp.get("/home")
def home():
    if "csr_user_id" not in session:
        return redirect(url_for("csr_login.login_form"))
    return render_template("csr_home.html", username=session.get("csr_username",""))
