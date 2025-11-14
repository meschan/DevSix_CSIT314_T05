from flask import Blueprint, render_template, request

from ..control.csr_search_request_control import CSRSearchRequestControl
from ..extensions import request_repo, user_repo  # 复用同一份仓库实例

bp = Blueprint("csr_search_request", __name__, template_folder="../templates")

# 控制器：只读搜索，不改实体/仓库
_control = CSRSearchRequestControl(request_repo, user_repo)


@bp.get("/search-requests")
def search_form():
    # 初次进入页面：不展示任何 request（submitted=False）
    return render_template(
        "csr_search_request.html",
        submitted=False,
        requests=[],
        mode="category",
        keyword="",
    )


@bp.post("/search-requests")
def search_submit():
    # 接收查询字段与关键词
    mode = (request.form.get("mode", "") or "").strip().lower()
    keyword = (request.form.get("q", "") or "").strip()

    rows = _control.search(mode, keyword)  # 返回已整理好的行
    return render_template(
        "csr_search_request.html",
        submitted=True,
        requests=rows,
        mode=mode,
        keyword=keyword,
    )
