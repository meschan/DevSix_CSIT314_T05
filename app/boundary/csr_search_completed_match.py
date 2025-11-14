'''from flask import Blueprint, render_template, request
from ..control.csr_search_completed_match_control import CsrSearchCompletedMatchControl
from ..extensions import request_repo,category_repo,user_repo

bp = Blueprint("csr_search_completed_match", __name__, url_prefix="/csr/search_completed_match",
                template_folder="templates")

control = CsrSearchCompletedMatchControl(
    request_repo=request_repo,
    category_repo=category_repo,
    user_repo=user_repo,
)

@bp.get("/")
def search_form(self):
    selected = request.args.get("category","All").strip()
    categories = self._all_category_names()
    rows = []
    if selected:
        if selected == "All":
            # 如果你有“查全部已匹配”的方法，用它；否则按需组合
            rows = self.search_by_category(None)  # 约定 None = 不限分类
        else:
            rows = self.search_by_category(selected)
    return render_template("csr_search_completed_match.html",
                            categories=categories,
                            selected_category=selected,
                            rows=rows)

'''

# app/boundary/csr_search_completed_match.py
'''from flask import Blueprint, render_template, request
# 按你的约定：boundary 直接从 control 模块拿到全局 control 实例
from ..control.csr_search_completed_match_control import CsrSearchCompletedMatchControl
from ..extensions import request_repo, user_repo
bp = Blueprint(
    "csr_search_completed_match",
    __name__,
    url_prefix="/csr/search-completed-match",
    template_folder="../../templates",
)

control = CsrSearchCompletedMatchControl(request_repo, user_repo)

@bp.get("/")
def search_form():
    # 读取选择；默认 All
    selected = request.args.get("category", "All").strip()

    # 所有分类：仅基于“已完成匹配”的请求
    categories = control._all_category_names()

    # 仅在带 query 时展示结果，否则给空列表（与 PIN 版交互一致）
    rows = []
    if selected:
        if selected == "All":
            rows = control.search_by_category(None)  # None 表示不限分类
        else:
            rows = control.search_by_category(selected)

    return render_template(
        "csr_search_completed_match.html",
        rows=rows,
        categories=categories,
        selected_category=selected,
    )

'''

# boundary/csr_search_completed_match.py
from flask import Blueprint, render_template, request
from ..control.csr_search_completed_match_control import CSRSearchCompletedMatchControl
bp = Blueprint("csr_search_completed_match", __name__, url_prefix="/csr/search-completed")

control = CSRSearchCompletedMatchControl()

@bp.get("/")
def search_form():
    selected = request.args.get("category", "All")

    # 下拉数据源：全部分类（包含 PM 新建的）
    categories = control.all_category_names()

    # 只有在发起查询时才展示结果；首次进入显示空表
    rows = control.search_by_category(selected) if request.args else []

    return render_template(
        "csr_search_completed_match.html",
        categories=categories,
        selected=selected,
        rows=rows,
    )

