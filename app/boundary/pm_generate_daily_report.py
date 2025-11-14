from flask import Blueprint, render_template,redirect,url_for,flash
from ..control.pm_daily_report_control import PMDailyReportControl
from ..extensions import request_repo, user_repo

bp = Blueprint("pm_daily_report", __name__, url_prefix="/pm/report")


control = PMDailyReportControl(request_repo, user_repo)

@bp.route("/daily", methods=["GET"])
def daily():
    rows = control.list_last_24h()

    return render_template("pm_daily_report.html", rows=rows)

@bp.post("/daily/generate")
def generate_daily():
    report = control.generate( )     # 不改方法名与签名
    flash(f"Daily report generated: {report.title}", "success")
    # 生成后跳到“删除/管理报告”页面，方便你立即看到是否入库成功
    return redirect(url_for("pm_delete_report.list_reports"))