from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..extensions import user_repo
from ..control.pin_login_control import PinLoginControl, PinAuthenticationError

bp = Blueprint("pin_login", __name__, template_folder="../templates")

_control = PinLoginControl(user_repo)


@bp.get("/login")
def login_form():
    # Display Form
    if session.get("pin_username"):
        return redirect(url_for("pin_home.home"))
    return render_template("pin_login.html", username="")


@bp.post("/login")
def login_submit():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    if not username or not password:
        flash("Please enter both username and password.", "warning")
        return render_template("pin_login.html", username=username), 400

    try:
        user = _control.authenticate(username, password)
    except PinAuthenticationError as e:
        flash(str(e), "danger")
        return render_template("pin_login.html", username=username), 401

    # 登录成功：存会话并跳转
    session["pin_user_id"] = user.id
    session["pin_username"] = user.username
    session["pin_full_name"] = user.username
    flash("Login successful.", "success")
    return redirect(url_for("pin_home.home"))




    '''try:
        user = _control.authenticate(username, password)
        # Login successful, session recorded.
        session["pin_user_id"] = user.id
        session["pin_username"] = user.username
        session["pin_role"] = user.role.value

        flash(f"Welcome, {user.username}!", "success")
        return redirect(url_for("pin_home.home"))

    except PinAuthenticationError as e:
        flash(str(e), "danger")
        return render_template("pin_login.html", username=username), 401
'''