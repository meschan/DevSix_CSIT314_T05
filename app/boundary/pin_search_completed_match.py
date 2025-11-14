# boundary/pin_search_completed_match.py
from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import request_repo, category_repo

bp = Blueprint("pin_search_completed_match", __name__, template_folder="../templates")

def _as_str(x, default=""):
    return (x or default).strip() if isinstance(x, str) else default

def _get_cat_name(req):
    # 兼容你不同的字段：category / category_name
    return _as_str(getattr(req, "category", None) or getattr(req, "category_name", None))

def _get_owner(req):
    # 兼容 owner_username / pin_username
    return _as_str(
        getattr(req, "owner_username", None)
        or getattr(req, "pin_username", None)
        or getattr(req, "owner", None)
        or getattr(req, "created_by", None)
    )

def _get_owner_id(req):
    # 兼容 owner_id / pin_user_id / user_id
    return (
        getattr(req, "owner_id", None)
        or getattr(req, "pin_user_id", None)
        or getattr(req, "user_id", None)
    )

def _get_matched_to(req):
    # 兼容 matched_to / matched_pin_username / matched_user
    return _as_str(
        getattr(req, "matched_to", None)
        or getattr(req, "matched_pin_username", None)
        or getattr(req, "matched_user", None)
    )

def _is_matched(req):
    # 兼容 matched / is_matched 布尔字段；若没有，用是否有 matched_to 推断
    if hasattr(req, "matched"):
        return bool(getattr(req, "matched"))
    if hasattr(req, "is_matched"):
        return bool(getattr(req, "is_matched"))
    return bool(_get_matched_to(req))

@bp.get("/pin/matches/search")
def search_form():
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))
    # 仅展示下拉，不立即出结果：
    cats = category_repo.get_all()   # 会包含你 PM 新建的分类
    return render_template("pin_search_completed_match.html",
                           categories=cats, selected="All",
                           matched_to_me=[], my_matched_to_others=[])

@bp.post("/pin/matches/search")
def search_submit():
    if "pin_user_id" not in session:
        return redirect(url_for("pin_login.login_form"))
    me_name = _as_str(session.get("pin_username", ""))
    me_id = session.get("pin_user_id")
    selected = request.form.get("category", "All")

    items = request_repo.list_all()

    # 1) 分到“我”的： matched 且 matched_to == 我的用户名
    matched_to_me = [r for r in items if _is_matched(r) and _get_matched_to(r) == me_name]

    # 2) 我发布且分给别人：owner == 我(或 owner_id == 我id) 且 matched 且 matched_to 存在 且 != 我
    my_matched_to_others = [
        r for r in items
        if _is_matched(r)
           and (_get_owner(r) == me_name or (_get_owner_id(r) is not None and _get_owner_id(r) == me_id))
           and _get_matched_to(r)
           and _get_matched_to(r) != me_name
    ]

    # 类别过滤（非 All 时才过滤）
    if selected and selected != "All":
        matched_to_me = [r for r in matched_to_me if _get_cat_name(r) == selected]
        my_matched_to_others = [r for r in my_matched_to_others if _get_cat_name(r) == selected]

    cats = category_repo.get_all()
    return render_template(
        "pin_search_completed_match.html",
        categories=cats,
        selected=selected,
        matched_to_me=matched_to_me,
        my_matched_to_others=my_matched_to_others,
    )










    #  没有match to others and oner

    '''me = session.get("pin_username", "")  # 你登录时保存的用户名键
    selected = request.form.get("category", "All")

    all_items = request_repo.list_all()
    # 1) 已匹配给我：matched 且 matched_to == 我
    matched_to_me = [r for r in all_items if _is_matched(r) and _get_matched_to(r) == me]
    # 2) 我发布且已匹配给别人：owner == 我 且 matched 且 matched_to != 我
    my_matched_to_others = [
        r for r in all_items
        if _get_owner(r) == me and _is_matched(r) and _get_matched_to(r) and _get_matched_to(r) != me
    ]

    # 类别过滤（All 不筛）
    if selected and selected != "All":
        matched_to_me = [r for r in matched_to_me if _get_cat_name(r) == selected]
        my_matched_to_others = [r for r in my_matched_to_others if _get_cat_name(r) == selected]

    cats = category_repo.get_all()
    return render_template("pin_search_completed_match.html",
                           categories=cats, selected=selected,
                           matched_to_me=matched_to_me,
                           my_matched_to_others=my_matched_to_others)'''
