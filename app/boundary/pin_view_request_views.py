from flask import Blueprint, render_template, session, redirect, url_for
from ..control.pin_view_request_views_control import PinViewRequestViewsControl

bp = Blueprint("pin_view_request_views", __name__, template_folder="../templates")
_control = PinViewRequestViewsControl()

@bp.get("/pin/request-views")
def show_views():
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))
    rows = _control.list_my_views()
    return render_template("pin_view_request_views.html",
                           owner=session.get("pin_username", ""),
                           rows=rows)
