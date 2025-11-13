from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
)
from ..control.pin_search_request_control import PinSearchRequestControl
from ..extensions import request_repo

bp = Blueprint("pin_search_request", __name__, template_folder="../templates")

_control = PinSearchRequestControl(request_repo)

def _require_login():
    """Redirecting to the PIN login page if not logged in"""
    if "pin_user_id" not in session:
        flash("Please log in to search your requests.", "warning")
        return redirect(url_for("pin_login.login_form"))
    return None


@bp.get("/request/search")
def search_form():
    """Show search page + search results"""
    not_logged_in = _require_login()
    if not_logged_in:
        return not_logged_in

    keyword = request.args.get("keyword", "").strip()
    results = []
    if keyword:
        pin_user_id = session["pin_user_id"]
        results = _control.search(pin_user_id, keyword)
        if not results:
            flash(f'No requests found for "{keyword}".', "info")

    return render_template(
        "pin_search_request.html",
        keyword=keyword,
        results=results,
    )
