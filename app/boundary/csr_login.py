# app/boundary/csr_login.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..control.csr_login_control import CsrLoginControl, CsrAuthenticationError
from ..extensions import user_repo  # 你项目里共享的仓库实例

bp = Blueprint("csr_login", __name__, template_folder="../templates")

_control = CsrLoginControl(user_repo=user_repo)

@bp.get("/login")
def login_form():
    return render_template("csr_login.html")

@bp.post("/login")
def login_submit():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    try:
        user = _control.authenticate(username, password)
    except CsrAuthenticationError as e:
        flash(str(e), "danger")
        return render_template("csr_login.html"), 401

    # 登录成功：保存会话并跳转 CSR 主页
    session["csr_username"] = user.username
    session["csr_user_id"] = user.id
    flash("Login successful.", "success")
    return redirect(url_for("csr_home.home"))
