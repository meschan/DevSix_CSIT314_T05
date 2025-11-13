from flask import Blueprint, render_template
from ..extensions import user_profile_repo
from ..control.view_user_profile_control import ViewUserProfileControl

bp = Blueprint("view_user_profile", __name__, template_folder="../templates")
_control = ViewUserProfileControl(user_profile_repo)


@bp.get("/profiles")
def list_profiles():
    """Displays all created user profiles (including the default 4)."""
    profiles = _control.list_all()
    return render_template("view_user_profiles.html", profiles=profiles)
