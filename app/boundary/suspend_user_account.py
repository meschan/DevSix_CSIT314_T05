# app/boundary/suspend_user_account.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..control.suspend_user_account_control import SuspendUserAccountControl

bp = Blueprint("suspend_user_account", __name__, url_prefix="")

_control = SuspendUserAccountControl()

@bp.get("/user-accounts/suspend")
def show_form():
    users = _control.list_all_users()
    return render_template("suspend_user_account.html", users=users)

@bp.post("/user-accounts/suspend")
def submit_suspend():
    username = request.form.get("username", "").strip()
    action = request.form.get("action", "suspend")  # "suspend" 或 "activate"

    if not username:
        flash("Please select a username.", "danger")
        return redirect(url_for("suspend_user_account.show_form"))

    if action == "activate":
        result = _control.activate(username)
    else:
        result = _control.suspend(username)

    # result = _control.suspend(username)
    flash(result.message, "success" if result.ok else "danger")
    return redirect(url_for("suspend_user_account.show_form"))
