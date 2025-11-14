# app/boundary/csr_view_shortlisted_request.py
# app/boundary/csr_view_shortlisted_request.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..control.csr_view_shortlisted_request_control import CSRViewShortlistedRequestControl

bp = Blueprint("csr_view_shortlisted_request", __name__, template_folder="../templates")
_control = CSRViewShortlistedRequestControl()

# ===== 列表页 =====
@bp.get("/shortlisted")
def list_shortlisted():
    csr_username = session.get("csr_username", "")
    items = _control.list_shortlisted(csr_username)
    return render_template("csr_view_shortlisted_request.html", requests=items, csr_username=csr_username)

# ===== 计数 +1（按钮 POST）=====
@bp.post("/shortlisted/<int:req_id>/view")
def view_shortlisted(req_id: int):
    csr_username = session.get("csr_username", "")
    new_views = _control.view_one(csr_username, req_id)
    if new_views is None:
        flash("You can only view requests saved in your shortlist.", "warning")
    else:
        flash(f"Viewed. Current views: {new_views}.", "success")
    return redirect(url_for("csr_view_shortlisted_request.list_shortlisted"))

# ===== 匹配（GET 展示选择器，POST 提交匹配）=====
@bp.get("/shortlisted/<int:req_id>/match")
def match_form(req_id: int):
    csr_username = session.get("csr_username", "")
    # 为了把创建者排除在候选之外，需要拿到该 request 的 owner
    from ..extensions import request_repo
    req = request_repo.get_by_id(req_id)
    owner = getattr(req, "pin_username", None) or getattr(req, "owner_username", None)
    pins = _control.candidates_pins(exclude_username=owner)
    if not pins:
        flash("No eligible PIN candidates.", "info")
        return redirect(url_for("csr_view_shortlisted_request.list_shortlisted"))
    return render_template("csr_match_form.html", req=req, candidates=pins)

@bp.post("/shortlisted/<int:req_id>/match")
def match_submit(req_id: int):
    csr_username = session.get("csr_username", "")
    target = request.form.get("pin_username", "").strip()
    ok, msg = _control.match_one(csr_username, req_id, target)
    flash(msg, "success" if ok else "warning")
    return redirect(url_for("csr_view_shortlisted_request.list_shortlisted"))



















#can run but no match

'''from flask import Blueprint, render_template, redirect, url_for, flash, session
from ..control.csr_view_shortlisted_request_control import CSRViewShortlistedRequestControl
from ..extensions import request_repo, user_repo, shortlist_repo

bp = Blueprint("csr_view_shortlisted", __name__, template_folder="../templates")
_control = CSRViewShortlistedRequestControl(request_repo, user_repo, shortlist_repo)

@bp.get("/shortlist")
def list_shortlisted():
    if "csr_username" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("csr_login.login_form"))

    rows = _control.list_shortlisted()
    return render_template("csr_view_shortlisted_request.html", requests=rows)

@bp.post("/shortlist/<int:req_id>/view")
def add_view(req_id: int):
    if "csr_username" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("csr_login.login_form"))

    ok, msg = _control.add_view(req_id)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("csr_view_shortlisted.list_shortlisted"))
'''