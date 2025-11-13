from flask import Blueprint, render_template, session, redirect, url_for, flash
from ..control.view_request_control import ViewRequestControl

bp = Blueprint(
    name="pin_view_request",
    import_name=__name__,
    template_folder="../templates",
)

_control = ViewRequestControl()


def _ensure_login():
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))
    return None


@bp.get("/requests")
def list_requests():
    # Login check
    redirect_resp = _ensure_login()
    if redirect_resp:
        return redirect_resp

    pin_user_id = session["pin_user_id"]
    requests = _control.list_for_pin(pin_user_id)

    if not requests:
        flash("You do not have any requests yet.", "info")

    return render_template("pin_view_requests.html", requests=requests)
