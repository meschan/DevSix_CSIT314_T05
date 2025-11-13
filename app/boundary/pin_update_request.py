from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

from ..control.pin_update_request_control import (
    PinUpdateRequestControl,
    RequestNotFoundError,
    ValidationError,
)
from ..extensions import request_repo, category_repo

bp = Blueprint("pin_update_request", __name__, template_folder="../templates")

control = PinUpdateRequestControl(request_repo)

# 1. On the Dashboard, click "Update Request" → go here first to list all requests.
@bp.get("/requests/update")
def list_requests():
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))

    pin_user_id = session["pin_user_id"]
    requests = control.list_requests_for_user(pin_user_id)

    if not requests:
        flash("You do not have any requests to update yet.", "info")

    return render_template("pin_update_request_list.html", requests=requests)


# 2. Click "Edit" on a specific entry to enter the edit form.
@bp.get("/requests/<int:req_id>/edit")
def edit_form(req_id: int):
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))

    pin_user_id = session["pin_user_id"]

    try:
        req = control.get_request_for_edit(req_id, pin_user_id)
    except RequestNotFoundError:
        flash("Request not found.", "danger")
        return redirect(url_for("pin_update_request.list_requests"))

    categories = [c.name for c in category_repo.get_all() if c.status == "Active"]
    return render_template(
        "pin_update_request_edit.html",
        request_obj=req,
        categories=categories,
    )

# 3. Submit update
@bp.post("/requests/<int:req_id>/edit")
def edit_submit(req_id: int):
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))

    pin_user_id = session["pin_user_id"]
    title = request.form.get("title", "")
    service_category = request.form.get("service_category", "")
    description = request.form.get("description", "")

    try:
        control.update_request(
            req_id=req_id,
            pin_user_id=pin_user_id,
            title=title,
            service_category=service_category,
            description=description,
        )
        flash("Request updated successfully.", "success")
        return redirect(url_for("pin_home.home"))

    except ValidationError as e:
        flash(str(e), "warning")
        req = control.get_request_for_edit(req_id, pin_user_id)
        req.title = title
        req.category = service_category
        req.description = description
        categories = [c.name for c in category_repo.get_all() if c.status == "Active"]
        return render_template(
            "pin_update_request_edit.html",
            request_obj=req,
            categories=categories,
        )

    except RequestNotFoundError:
        flash("Request not found.", "danger")
        return redirect(url_for("pin_update_request.list_requests"))
