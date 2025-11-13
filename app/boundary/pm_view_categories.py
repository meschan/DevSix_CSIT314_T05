from flask import Blueprint, render_template, redirect, url_for, session
from ..control.pm_view_categories_control import PMViewCategoriesControl

bp = Blueprint("pm_view_categories", __name__, template_folder="../templates")
_control = PMViewCategoriesControl()

@bp.get("/view-categories")
def list_categories():
    # 简单守卫：未登录 PM 则回登录页
    if "pm_username" not in session:
        return redirect(url_for("pm_login.login_form"))
    categories = _control.list_categories()
    return render_template("pm_view_categories.html", categories=categories)
