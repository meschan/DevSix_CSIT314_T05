from flask import Blueprint, render_template, request, flash
from ..control.search_user_profile_control import SearchUserProfileControl

bp = Blueprint("search_user_profile", __name__, template_folder="../templates")
control = SearchUserProfileControl()

@bp.get("/user-profiles/search")
def search_form():
    profiles = control.get_all_profiles()

    profile_id_raw = request.args.get("profile_id", "").strip()
    selected_profile_id = int(profile_id_raw) if profile_id_raw.isdigit() else None

    #  You must first give users/profile_name a default value.
    #  This way, even if no profile is selected, an UnboundLocalError will not occur.
    users = []
    profile_name = None

    if selected_profile_id is not None:
        try:
            result = control.search(selected_profile_id)
            users = result.users
            profile_name = result.profile_name

            if not users:
                flash(f'No users found for profile "{profile_name}".', "info")
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "search_user_profile.html",
        profiles=profiles,
        selected_profile_id=selected_profile_id,
        users=users,
        profile_name=profile_name,
    )
