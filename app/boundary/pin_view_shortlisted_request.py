# app/boundary/pin_view_shortlisted_request.py
from flask import Blueprint, render_template, session, redirect, url_for
from ..control.pin_view_shortlisted_request_control import PinViewShortlistedRequestControl

bp = Blueprint("pin_view_shortlisted_request", __name__, template_folder="../templates")
_control = PinViewShortlistedRequestControl()

@bp.get("/pin/request-saved")
def show_saved():
    # 与 pin_view_request_views 的登录校验一致
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))
    rows = _control.list_my_saved()
    return render_template(
        "pin_view_shortlisted_request.html",
        owner=session.get("pin_username", ""),
        rows=rows,
    )
