from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from ..control.pm_update_category_control import PMUpdateCategoryControl

bp = Blueprint("pm_update_category", __name__, template_folder="../templates")
_control = PMUpdateCategoryControl()

def _ensure_pm_login():
    if "pm_username" not in session:
        return redirect(url_for("pm_login.login_form"))
    return None

@bp.get("/update-categories")
def list_categories():
    guard = _ensure_pm_login()
    if guard: return guard
    categories = _control.list_categories()
    return render_template("pm_update_categories.html", categories=categories)

@bp.get("/update-category/<int:cat_id>")
def update_form(cat_id: int):
    guard = _ensure_pm_login()
    if guard: return guard
    cat = _control.get_category(cat_id)
    if not cat:
        flash("Category not found.", "danger")
        return redirect(url_for("pm_update_category.list_categories"))
    return render_template("pm_update_category_form.html", category=cat)

@bp.post("/update-category/<int:cat_id>")
def update_submit(cat_id: int):
    guard = _ensure_pm_login()
    if guard: return guard
    new_name = request.form.get("name", "").strip()
    result = _control.rename(cat_id, new_name)
    flash(result.message, "success" if result.ok else "danger")
    if result.ok:
        return redirect(url_for("pm_update_category.list_categories"))
    # 出错则回显
    cat = _control.get_category(cat_id)
    return render_template("pm_update_category_form.html",
                           category=cat, last_name=new_name), 400
