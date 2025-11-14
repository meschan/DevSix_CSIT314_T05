# app/boundary/csr_save_volunteer_request.py
from flask import Blueprint, render_template, redirect, url_for, flash, session
from ..control.csr_save_volunteer_request_control import CSRSaveVolunteerRequestControl
from ..extensions import request_repo, user_repo, shortlist_repo

bp = Blueprint("csr_save_request", __name__, template_folder="../templates")
_control = CSRSaveVolunteerRequestControl(request_repo, user_repo, shortlist_repo)

@bp.get("/save-requests")
def list_available():
    # 可选：需要登录校验（如果你的 CSR 会话键不同，请按实际替换）
    if "csr_username" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("csr_login.login_form"))

    rows = _control.list_available()
    return render_template("csr_save_volunteer_request.html", requests=rows)

@bp.post("/save-requests/<int:req_id>/save")
def save_one(req_id: int):
    if "csr_username" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("csr_login.login_form"))

    ok, msg = _control.save_to_shortlist(req_id)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("csr_save_request.list_available"))
