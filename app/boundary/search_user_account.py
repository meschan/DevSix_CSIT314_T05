# app/boundary/search_user_account.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..control.search_user_account_control import SearchUserAccountControl

bp = Blueprint("search_user_account", __name__, template_folder="../templates")

_control = SearchUserAccountControl()

@bp.get("/user-accounts/search")
def search_form():
    # 初始进入页面，无结果
    return render_template("search_user_account.html", keyword="", results=[])

@bp.post("/user-accounts/search")
def search_submit():
    keyword = request.form.get("keyword", "").strip()
    if not keyword:
        flash("Please enter a username / email / phone / role to search.", "warning")
        return redirect(url_for("search_user_account.search_form"))

    result = _control.search(keyword)
    if not result.users:
        flash(f"No users found for '{result.keyword}'.", "info")

    return render_template(
        "search_user_account.html",
        keyword=result.keyword,
        results=result.users,
    )
