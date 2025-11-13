from flask import Blueprint, render_template, request, flash
from ..control.suspend_user_profile_control import SuspendUserProfileControl

bp = Blueprint("suspend_user_profile", __name__, template_folder="../templates")

_control = SuspendUserProfileControl()


@bp.get("/suspend")
def show_suspend_page():
    """
    The page displays the option to suspend user profiles.
    """
    profiles = _control.list_profiles()
    return render_template(
        "suspend_user_profile.html",
        profiles=profiles,
        selected_profile_id=None,
    )


@bp.post("/suspend")
def submit_suspend():
    """
    Handle suspend commits.
    """
    raw_id = request.form.get("profile_id", "").strip()

    profiles = _control.list_profiles()

    if not raw_id:
        flash("Please select a user profile to suspend.", "warning")
        return render_template(
            "suspend_user_profile.html",
            profiles=profiles,
            selected_profile_id=None,
        )

    try:
        profile_id = int(raw_id)
    except ValueError:
        flash("Invalid user profile selection.", "danger")
        return render_template(
            "suspend_user_profile.html",
            profiles=profiles,
            selected_profile_id=None,
        )

    result = _control.suspend(profile_id)

    flash(result.message, "success" if result.ok else "danger")

    # Retrieve the list again to see the latest status (Active / Suspended).
    profiles = _control.list_profiles()
    return render_template(
        "suspend_user_profile.html",
        profiles=profiles,
        selected_profile_id=profile_id,
    )
