# app/boundary/pm_create_category.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..control.pm_create_category_control import PMCreateCategoryControl

bp = Blueprint("pm_create_category", __name__, template_folder="../templates")
_control = PMCreateCategoryControl()

@bp.get("/create-category")
def create_form():
    # 简单保护：未登录 PM 则跳回 PM 登录
    if "pm_username" not in session:
        return redirect(url_for("pm_login.login_form"))
    return render_template("pm_create_category.html")

@bp.post("/create-category")
def create_submit():
    if "pm_username" not in session:
        return redirect(url_for("pm_login.login_form"))

    name = request.form.get("name", "").strip()
    result = _control.create(name)
    flash(result.message, "success" if result.ok else "danger")
    if result.ok:
        return redirect(url_for("pm_create_category.create_form"))
    # 校验失败，回显输入
    return render_template("pm_create_category.html", last_name=name), 400
