# app/boundary/pm_delete_report.py
from __future__ import annotations
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..control.pm_report_delete_control import PMReportDeleteControl
from ..extensions import report_repo

bp = Blueprint("pm_delete_report", __name__, template_folder="../templates")

_control = PMReportDeleteControl(report_repo)

def _require_pm_login():
    # 若你已有更严格的鉴权（检查角色为 Platform Manager），在此补充
    if "pm_username" not in session:
        # 未登录则返回 PM 登录页
        return redirect(url_for("pm_login.login_form"))
    return None

@bp.get("/pm/reports/delete")
def list_reports():
    # 登录校验
    redir = _require_pm_login()
    if redir:
        return redir

    reports = _control.list_reports()
    return render_template("pm_delete_report.html", reports=reports)

@bp.post("/pm/reports/delete")
def submit_delete():
    # 登录校验
    redir = _require_pm_login()
    if redir:
        return redir

    report_id = request.form.get("report_id", "").strip()
    try:
        rid = int(report_id)
    except ValueError:
        flash("Invalid report id.", "danger")
        return redirect(url_for("pm_delete_report.list_reports"))

    res = _control.delete_report(rid)
    flash(res.message, "success" if res.ok else "danger")
    return redirect(url_for("pm_delete_report.list_reports"))
