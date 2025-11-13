# app/boundary/pm_home.py
from flask import Blueprint, render_template, session, redirect, url_for, flash

bp = Blueprint("pm_home", __name__, template_folder="../templates")

@bp.get("/home")
def home():
    if "pm_user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("pm_login.login_form"))
    username = session.get("pm_username", "")
    return render_template("pm_home.html", username=username)

@bp.get("/logout")
def logout():
    session.pop("pm_user_id", None)
    session.pop("pm_username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("pm_login.login_form"))














'''from flask import Blueprint, render_template, session, redirect, url_for, flash

bp = Blueprint("pm_home", __name__, template_folder="../templates")


@bp.get("/home")
def home():
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("pm_login.login_form"))


    role_name = session.get("role_name", "")
    if role_name.lower() != "platform manager":
        flash("You are not authorised as a Platform Manager.", "danger")
        return redirect(url_for("pm_login.login_form"))

    username = session.get("username", "")
    return render_template("pm_home.html", username=username)


@bp.get("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("pm_login.login_form"))
'''