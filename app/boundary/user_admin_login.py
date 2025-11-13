from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..control.user_admin_login_control import UserAdminLoginControl, AuthenticationError

from ..extensions import user_repo

bp = Blueprint("admin_login", __name__, template_folder="../templates")

# Use the registry module repository directly

_control = UserAdminLoginControl(user_repo)

@bp.get("/login")
def login_form():
    # Display administrator login form
    return render_template("user_admin_login.html")

@bp.post("/login")
def submit_login():
    # Processing login form submissions
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    try:
        user = _control.authenticate(username, password)
    except AuthenticationError as e:
        flash(str(e), "danger")
        return render_template("user_admin_login.html"), 401

    # 登录成功
    session["admin_id"] = user.id
    session["admin_username"] = user.username
    return redirect(url_for("user_admin_home.home"))

    '''try:
        user = _control.authenticate(username, password)
        session["admin_id"] = user.id
        flash(f"Welcome, {user.username}!", "success")
        return redirect(url_for("user_admin_home.home"))
    except AuthenticationError as e:
        flash(str(e), "error")
        return render_template("user_admin_login.html"), 401'''
