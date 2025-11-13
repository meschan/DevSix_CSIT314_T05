from flask import Blueprint, render_template, session, redirect, url_for

from ..control.csr_shortlist_control import CSRShortlistControl

bp = Blueprint("csr_shortlist", __name__, template_folder="../templates")

_shortlist_control = CSRShortlistControl()


@bp.get("/shortlist")
def view_shortlist():
    if "csr_user_id" not in session:
        return redirect(url_for("csr_login.login_form"))

    requests = _shortlist_control.get_shortlist(session["csr_user_id"])
    return render_template("csr_shortlist.html", requests=requests)
