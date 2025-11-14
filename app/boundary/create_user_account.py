from flask import Blueprint, render_template, request, redirect, url_for, flash
# Boundary depends on Control; Control depends on Entity (repo)
from ..control.create_user_account_control import (
    CreateUserAccountControl, ValidationError, ConflictError
)
from ..extensions import user_repo

bp = Blueprint("create_user", __name__, template_folder="../templates")


#done

_control = CreateUserAccountControl(user_repo)

@bp.get("/create")
def create_form():
    """Display Create User Form (Normal Flow: 'The system displays Create User Form')."""
    return render_template("create_user_account.html")

@bp.post("/create")
def submit_form():
    """
    Handle Submit Form:
    - validate inputs
    - check duplicates
    - create account or show errors (Alternative flows)
    """
    form = request.form
    try:
        user = _control.create_user_account(
            username=form.get("username", ""),
            email=form.get("email", ""),
            phone_number=form.get("phone_number", ""),
            address=form.get("address", ""),
            role=form.get("role", "user"),
            password=form.get("password", ""),
        )
        flash(f"User '{user.username}' created successfully (id={user.id}).", "success")
        # Redirect prevents form re-submission on refresh
        return redirect(url_for("create_user.create_form"))
    except ValidationError as ve:
        # Alternative flow: invalid user info -> loop to enter again
        flash(f"Validation error ({ve.field}): {ve}", "error")
        return render_template("create_user_account.html", form=form), 400
    except ConflictError as ce:
        # Alternative flow: duplicate found -> display error, stop action
        flash(f"Conflict: {ce}", "error")
        return render_template("create_user_account.html", form=form), 409
