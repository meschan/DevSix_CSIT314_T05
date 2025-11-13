from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..control.update_user_profile_control import UpdateUserProfileControl

bp = Blueprint("update_user_profile", __name__, template_folder="../templates")
control = UpdateUserProfileControl()

@bp.get("/user-profiles/update")
def show_form():
    users, profiles = control.get_form_data()
    return render_template(
        "update_user_profile.html",
        users=users,
        profiles=profiles,
        selected_username=None,
        selected_profile_id=None,
    )

@bp.post("/user-profiles/update")
def submit_update():
    username = request.form.get("username", "").strip()
    profile_id_raw = request.form.get("profile_id", "").strip()

    if not username or not profile_id_raw:
        flash("Please select both username and user profile.", "warning")
        users, profiles = control.get_form_data()
        return render_template(
            "update_user_profile.html",
            users=users,
            profiles=profiles,
            selected_username=username or None,
            selected_profile_id=int(profile_id_raw) if profile_id_raw.isdigit() else None,
        )

    try:
        profile_id = int(profile_id_raw)
    except ValueError:
        flash("Invalid profile selection.", "danger")
        users, profiles = control.get_form_data()
        return render_template(
            "update_user_profile.html",
            users=users,
            profiles=profiles,
            selected_username=username,
            selected_profile_id=None,
        )

    result = control.update_profile_for_user(username, profile_id)
    flash(result.message, "success" if result.ok else "danger")

    return redirect(url_for("update_user_profile.show_form"))
