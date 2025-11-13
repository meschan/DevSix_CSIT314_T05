from flask import Blueprint, render_template, redirect, url_for, session, flash

bp = Blueprint("user_admin_home", __name__, template_folder="../templates")

@bp.get("/home")
def home():
    # Administrator's homepage (accessible only after logging in)
    if "admin_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("admin_login.login_form"))
    return render_template("user_admin_home.html")

@bp.get("/logout")
def logout():
    session.pop("admin_id", None)
    session.pop("admin_username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("admin_login.login_form"))
