# boundary/csr_view_completed_match.py
from flask import Blueprint, render_template
from ..control.csr_view_completed_match_control import CSRViewCompletedMatchControl

bp = Blueprint("csr_view_completed", __name__, url_prefix="/csr/view-completed")

# 暴露给 boundary 使用
control = CSRViewCompletedMatchControl()

@bp.get("/")
def view_all():
    rows = control.list_all()
    return render_template("csr_view_completed_match.html", rows=rows)
