# app/boundary/view_user_account.py
from flask import Blueprint, render_template
from ..control.view_user_account_control import ViewUserAccountControl

bp = Blueprint("view_user_account", __name__, template_folder="../templates")
_control = ViewUserAccountControl()

@bp.get("/user-accounts")
def list_accounts():
    accounts = _control.list_all()
    return render_template("view_user_accounts.html", accounts=accounts)
