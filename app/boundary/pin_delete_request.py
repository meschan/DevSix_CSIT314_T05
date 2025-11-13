from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
)
from ..control.pin_delete_request_control import PinDeleteRequestControl


bp = Blueprint("pin_delete_request", __name__, template_folder="../templates")

control = PinDeleteRequestControl()


def _require_login():
    """
    Ensure you are logged in with your PIN; otherwise,
    you will be redirected to the login page.
    """
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))
    return None


@bp.get("/request/delete")
def list_requests():
    """
    Displays all removable requests for the current PIN user.
    """
    not_logged_in = _require_login()
    if not_logged_in:
        return not_logged_in

    pin_user_id = session["pin_user_id"]
    requests = control.list_requests(pin_user_id)

    return render_template("pin_delete_request_list.html", requests=requests)


@bp.get("/request/delete/<int:req_id>")
def confirm_form(req_id: int):
    """Confirmation page before deletion"""
    not_logged_in = _require_login()
    if not_logged_in:
        return not_logged_in

    pin_user_id = session["pin_user_id"]

    try:
        req = control.get_request(pin_user_id, req_id)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("pin_delete_request.list_requests"))

    return render_template("pin_delete_request_confirm.html", req=req)


@bp.post("/request/delete/<int:req_id>")
def delete_submit(req_id: int):
    """Actual deletion"""
    not_logged_in = _require_login()
    if not_logged_in:
        return not_logged_in

    pin_user_id = session["pin_user_id"]

    ok = control.delete_request(req_id)
    if not ok:
        flash("The request you attempted to delete does not exist.", "danger")
    else:
        flash("The request has been deleted successfully.", "success")

    return redirect(url_for("pin_delete_request.list_requests"))
