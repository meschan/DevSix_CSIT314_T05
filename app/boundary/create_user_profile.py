from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..extensions import user_profile_repo
from ..control.create_user_profile_control import (
    CreateUserProfileControl,
    DuplicateProfileError,
    ValidationError,
)

bp = Blueprint("create_user_profile", __name__, template_folder="../templates")
_control = CreateUserProfileControl(user_profile_repo)

@bp.get("/profiles/create")
def create_form():
    # Always provide errors / form_data to avoid template undefined issues.
    return render_template(
        "create_user_profile.html",
        errors={},
        form_data={"name": ""},
    )

@bp.post("/profiles/create")
def create_submit():
    name = (request.form.get("name") or "").strip()

    try:
        profile = _control.create(name)
        flash(f"User profile '{profile.name}' has been created successfully.", "success")
        return redirect(url_for("user_admin_home.home"))

    except DuplicateProfileError as e:
        flash(str(e), "danger")
        return render_template(
            "create_user_profile.html",
            errors={"name": str(e)},
            form_data={"name": name},
        )

    except ValidationError as e:
        # `e.errors` is a dictionary that contains at least the error name.
        flash("Please correct the highlighted errors.", "danger")
        return render_template(
            "create_user_profile.html",
            errors=e.errors,
            form_data={"name": name},
        )
