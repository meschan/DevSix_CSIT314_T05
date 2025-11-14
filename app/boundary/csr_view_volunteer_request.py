from flask import Blueprint, render_template, redirect, url_for, flash
from ..control.csr_view_volunteer_request_control import CSRViewVolunteerRequestControl
from ..extensions import request_repo, user_repo

bp = Blueprint("csr_view_volunteer", __name__, template_folder="../templates")
_control = CSRViewVolunteerRequestControl(request_repo, user_repo)

@bp.get("/view-volunteer-requests")
def view_all():
    rows = _control.list_all_rows()
    return render_template("csr_view_volunteer_request.html", requests=rows)

# 新增：点击“View”按钮时调用，完成 views+1 然后回到列表
@bp.post("/view-volunteer-requests/<int:req_id>/view")
def add_view(req_id: int):
    ok = _control.add_view(req_id)
    if not ok:
        flash("Request not found.", "warning")
    else:
        flash("View recorded.", "success")
    return redirect(url_for("csr_view_volunteer.view_all"))
