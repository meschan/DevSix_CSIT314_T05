# app/boundary/csr_search_request.py
from flask import Blueprint, render_template, session, redirect, url_for
from ..control.csr_search_request_control import CSRSearchRequestControl

bp = Blueprint("csr_search_request", __name__, template_folder="../templates")
_control = CSRSearchRequestControl()

@bp.get("/search-request")
def list_page():
    # 登录保护：必须是 CSR 已登录
    if "csr_username" not in session:
        # 你的 CSR 登录蓝图名字如果不是 'csr_login'，把下面 endpoint 改成你实际的
        return redirect(url_for("csr_login.login_form"))

    requests = _control.list_all_requests()
    return render_template("csr_search_request.html", requests=requests)
