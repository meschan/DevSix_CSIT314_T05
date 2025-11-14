# app/boundary/csr_search_shortlisted_request.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..control.csr_search_shortlisted_request_control import CSRSearchShortlistedRequestControl
from ..extensions import request_repo, user_repo, shortlist_repo

bp = Blueprint("csr_search_shortlisted", __name__, template_folder="../templates")
_control = CSRSearchShortlistedRequestControl(request_repo, user_repo, shortlist_repo)

@bp.get("/shortlist/search")
def search_form():
    if "csr_username" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("csr_login.login_form"))

    # 初次访问不给默认结果，只展示空页面
    return render_template("csr_search_shortlisted_request.html", results=None, keyword="")

@bp.post("/shortlist/search")
def search_submit():
    if "csr_username" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("csr_login.login_form"))

    keyword = request.form.get("keyword", "").strip()
    if not keyword:
        flash("Please enter a keyword to search.", "warning")
        return render_template("csr_search_shortlisted_request.html", results=None, keyword="")

    rows = _control.search(keyword)
    if not rows:
        flash("No shortlisted requests matched your search.", "info")
    return render_template("csr_search_shortlisted_request.html", results=rows, keyword=keyword)

@bp.post("/shortlist/search/<int:req_id>/view")
def add_view(req_id: int):
    if "csr_username" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("csr_login.login_form"))

    ok, msg = _control.add_view(req_id)
    flash(msg, "success" if ok else "danger")
    # 回到搜索页；保持 UX 简单，这里回空表单页
    return redirect(url_for("csr_search_shortlisted.search_form"))
