from flask import Blueprint, render_template, redirect, flash, url_for
from ..control.pm_monthly_report_control import PMMonthlyReportControl
from ..extensions import request_repo, user_repo

bp = Blueprint("pm_monthly_report", __name__, url_prefix="/pm/report")


control = PMMonthlyReportControl(request_repo, user_repo)

@bp.route("/monthly", methods=["GET"])
def monthly():
    rows = control.list_last_30days()

    return render_template("pm_monthly_report.html", rows=rows)

@bp.post("/monthly/generate")
def generate_monthly():
    report = control.generate( )     # 不改方法名与签名
    flash(f"Monthly report generated: {report.title}", "success")
    # 生成后跳到“删除/管理报告”页面，方便你立即看到是否入库成功
    return redirect(url_for("pm_delete_report.list_reports"))