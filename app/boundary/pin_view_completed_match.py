# boundary/pin_view_completed_match.py
from flask import Blueprint, render_template
from ..control.pin_view_completed_match_control import PinViewCompletedMatchControl
from ..extensions import request_repo,user_repo
bp = Blueprint("pin_view_completed_match", __name__, url_prefix="/pin/completed-match")

control = PinViewCompletedMatchControl(request_repo=request_repo, user_repo=user_repo)
# .swe
@bp.get("/view")
def view_page():
    data = control.list_all()
    return render_template("pin_view_completed_match.html", **data)

