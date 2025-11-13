# app/boundary/update_user_account.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..control.update_user_account_control import UpdateUserAccountControl

bp = Blueprint("update_user_account", __name__, template_folder="../templates")
_control = UpdateUserAccountControl()

# Step 1: 搜索表单（GET 展示、POST 提交）
@bp.get("/user-accounts/update")
def search_form():
    return render_template("update_user_account_search.html")

@bp.post("/user-accounts/update")
def search_submit():
    username = request.form.get("username", "").strip()
    user = _control.find_by_username(username)
    if not user:
        flash(f"User '{username}' not found.", "danger")
        return render_template("update_user_account_search.html", username=username), 404

    # 找到用户 → 渲染编辑页（仅可改手机号、地址、密码）
    return render_template("update_user_account_edit.html", user=user)

# Step 2: 提交更新
# app/boundary/update_user_account.py

@bp.post("/user-accounts/update/<username>")
def update_submit(username: str):
    new_phone   = request.form.get("phone_number", None)
    new_address = request.form.get("address", None)
    new_pwd     = request.form.get("password", None)
    new_email   = request.form.get("email", None)

    result = _control.update_fields(username, new_phone, new_address, new_pwd, new_email)

    if not result.ok:
        category = "info" if result.message == "No changes detected." else "danger"
        flash(result.message, category)
        user = _control.find_by_username(username)
        return render_template(
            "update_user_account_edit.html",
            user=user,
            form_data={
                "phone_number": new_phone,
                "address": new_address,
                "email": new_email,
            },
        ), (200 if category == "info" else 400)

    flash(result.message, "success")
    return redirect(url_for("update_user_account.search_form"))

