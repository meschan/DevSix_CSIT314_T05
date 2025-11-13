from flask import Blueprint, render_template, session, redirect, url_for, flash

bp = Blueprint("pin_home", __name__, template_folder="../templates")

@bp.get("/home")
def home():
    # If you are not logged in, you will be redirected to the PIN login page.
    username = session.get("pin_username")
    if not username:
        flash("Please log in first.", "warning")
        return redirect(url_for("pin_login.login_form"))
    full_name = session.get("pin_full_name", username)
    return render_template("pin_home.html", full_name=full_name)

@bp.get("/logout")
def logout():
    """
    The PIN user logs out, clears their session,
    and returns to the login page.
    """
    session.pop("pin_user_id", None)
    session.pop("pin_username", None)
    session.pop("pin_full_name", None)

    flash("You have been logged out.", "info")
    return redirect(url_for("pin_login.login_form"))