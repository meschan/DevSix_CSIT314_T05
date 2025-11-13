# app/boundary/csr_search_request.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from ..control.csr_search_request_control import CSRSearchRequestControl
from ..control.csr_shortlist_control import CSRShortlistControl

bp = Blueprint("csr_search_request", __name__, template_folder="../templates")
_control = CSRSearchRequestControl()
_shortlist_control = CSRShortlistControl()

@bp.get("/search-request")
def list_page():
    # 登录保护：必须是 CSR 已登录
    if "csr_username" not in session:
        # 你的 CSR 登录蓝图名字如果不是 'csr_login'，把下面 endpoint 改成你实际的
        return redirect(url_for("csr_login.login_form"))

    requests = _control.list_all_requests()
    return render_template("csr_search_request.html", requests=requests)


@bp.post("/search-request/<int:req_id>/shortlist")
def save_to_shortlist(req_id: int):
    if "csr_username" not in session or "csr_user_id" not in session:
        return redirect(url_for("csr_login.login_form"))

    csr_user_id = session["csr_user_id"]
    result = _shortlist_control.save_to_shortlist(csr_user_id, req_id)

    if result == "added":
        flash("Saved to shortlist.", "success")
    elif result == "exists":
        flash("Opportunity already in your shortlist.", "info")
    else:
        flash("Opportunity could not be found.", "danger")

    return redirect(url_for("csr_search_request.list_page"))
