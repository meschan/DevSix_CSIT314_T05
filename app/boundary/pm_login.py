# app/boundary/pm_login.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..control.pm_login_control import PMLoginControl, PMAuthenticationError
from ..extensions import user_repo

bp = Blueprint("pm_login", __name__, template_folder="../templates")
_control = PMLoginControl(user_repo)

@bp.get("/login")
def login_form():
    return render_template("pm_login.html")

@bp.post("/login")
def login_submit():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    try:
        result = _control.authenticate(username, password)
    except PMAuthenticationError as e:
        flash(str(e), "danger")
        # 一定要 return 页面，避免出现 “did not return a valid response” 的 TypeError
        return render_template("pm_login.html", username=username), 401

    # 登录成功：写入会话并跳转
    user = result.user
    session["pm_user_id"] = user.id
    session["pm_username"] = user.username
    flash("Login successful.", "success")
    return redirect(url_for("pm_home.home"))











'''from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from ..control.pm_login_control import PmLoginControl, PlatformManagerAuthenticationError

bp = Blueprint("pm_login", __name__, template_folder="../templates")

_control = PmLoginControl()


@bp.get("/login")
def login_form():
    """Display the PM login page."""
    return render_template("pm_login.html", username="")


@bp.post("/login")
def login_submit():
    """Process PM login submissions."""
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    try:
        user = _control.authenticate(username, password)
    except PlatformManagerAuthenticationError as e:
        flash(str(e), "danger")
        return render_template("pm_login.html"), 401

        # 登录成功 -> 写 session 并跳转主页
    session["pm_username"] = user.username
    session["pm_user_id"] = user.id
    flash("Login successful.", "success")
    return redirect(url_for("pm_home.home"))







    if not username or not password:
        flash("Please enter both username and password.", "warning")
        return render_template("pm_login.html", username=username)

    try:
        user = _control.authenticate(username, password)

        # Login successful, session recorded.
        session["user_id"] = user.id
        session["username"] = user.username
        session["role_name"] = user.role.value

        flash(f"Welcome, {user.username}!", "success")
        return redirect(url_for("pm_home.home"))

    except PlatformManagerAuthenticationError as e:
        flash(str(e), "danger")
        return render_template("pm_login.html", username=username)
'''