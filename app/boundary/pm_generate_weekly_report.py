from flask import Blueprint, render_template,redirect,url_for,flash
from ..control.pm_weekly_report_control import PMWeeklyReportControl
from ..extensions import request_repo, user_repo

bp = Blueprint("pm_weekly_report", __name__, url_prefix="/pm/report")


control = PMWeeklyReportControl(request_repo, user_repo)


@bp.route("/weekly", methods=["GET"])
def weekly():
    rows = control.list_last_7d()

    return render_template("pm_weekly_report.html", rows=rows)

@bp.post("/weekly/generate")
def generate_weekly():
    report = control.generate( )
    flash(f"Weekly report generated: {report.title}", "success")
    return redirect(url_for("pm_delete_report.list_reports"))