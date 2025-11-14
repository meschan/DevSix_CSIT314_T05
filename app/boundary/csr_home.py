# app/boundary/csr_home.py
from flask import Blueprint, render_template, session, redirect, url_for, flash

bp = Blueprint("csr_home", __name__, template_folder="../templates")

@bp.get("/home")
def home():
    if "csr_user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("csr_login.login_form"))
    return render_template("csr_home.html", username=session.get("csr_username",""))

@bp.post("/logout")
def logout():
    """从主页发起的登出动作"""
    # 仅清理 CSR 登录用到的会话键
    session.pop("csr_username", None)
    session.pop("csr_user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("csr_login.login_form"))