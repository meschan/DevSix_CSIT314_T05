from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)
from ..control.create_request_control import (
    CreateRequestControl, RequestValidationError,
)

from ..extensions import category_repo

bp = Blueprint(
    name="pin_create_request",
    import_name=__name__,
    template_folder="../templates",
)

_control = CreateRequestControl()


def _ensure_login():
    """
    If you are not logged in, you will be redirected to PIN login.
    """
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))
    return None


@bp.get("/requests/create")
def create_form():
    # Login check
    redirect_resp = _ensure_login()
    if redirect_resp:
        return redirect_resp

    return render_template(
        "pin_create_request.html",
        categories=[c.name for c in category_repo.get_all() if c.status == "Active"],
        errors={},
        form_data={"title": "", "category": "", "description": ""},
    )


@bp.post("/requests/create")
def create_submit():
    redirect_resp = _ensure_login()
    if redirect_resp:
        return redirect_resp

    title = request.form.get("title", "")
    category = request.form.get("category", "")
    description = request.form.get("description", "")

    form_data = {
        "title": title,
        "category": category,
        "description": description,
    }

    try:
        _control.create(
            pin_user_id=session["pin_user_id"],
            title=title,
            category=category,
            description=description,
        )
        flash("Your request has been created successfully.", "success")
        return redirect(url_for("pin_home.home"))

    except RequestValidationError as e:
        flash("Please correct the errors below.", "danger")
        return (
            render_template(
                "pin_create_request.html",
                categories=[c.name for c in category_repo.get_all() if c.status == "Active"],
                errors=e.errors,
                form_data=form_data,
            ),
            400,
        )
