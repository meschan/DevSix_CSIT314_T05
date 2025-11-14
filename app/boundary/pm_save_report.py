# app/boundary/pm_save_report.py
from __future__ import annotations

from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response

# 复用你项目里已经存在的全局仓库对象（不改其它文件）
from ..extensions import request_repo, report_repo

bp = Blueprint("pm_save_report", __name__, url_prefix="/pm/report/save")


# ---------- 工具：时间窗口 ----------
def _window_by_period(period: str, right_edge: datetime):
    """
    根据 period + created_at 计算 [since, until]
    - daily:  24 小时
    - weekly: 7 天
    - monthly: 30 天(简化近似, 无第三方依赖)
    """
    p = (period or "").lower().strip()
    if p == "daily":
        return right_edge - timedelta(hours=24), right_edge
    if p == "weekly":
        return right_edge - timedelta(days=7), right_edge
    if p == "monthly":
        return right_edge - timedelta(days=30), right_edge
    # 兜底：按 7 天处理
    return right_edge - timedelta(days=7), right_edge

# ---------- 工具：安全取字段 ----------
def _g(rec: dict, *names, default=None):
    """
    按顺序尝试多个字段名，取到第一个非空即返回；全为空则给 default
    """
    for n in names:
        if n in rec and rec[n] not in (None, ""):
            return rec[n]
    return default


def _as_dt(x):
    """
    字段统一转 datetime；失败返回 None
    """
    if isinstance(x, datetime):
        return x
    if x in (None, ""):
        return None
    s = str(x)
    # 常见 ISO / 带空格的时间
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass
    # 尝试 fromisoformat
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def _is_matched(rec: dict) -> bool:
    """
    判断一条 request 是否“已匹配”。尽量兼容你项目里可能存在的字段。
    """
    # 常见字段：matched / matched_flag / matched_to(_username)
    if _g(rec, "matched", "matched_flag", default=False):
        return True
    if _g(rec, "matched_to_username", "matched_to", default=None):
        return True
    # 有些实现会把状态放在 status 字段
    status = str(_g(rec, "status", default="")).lower()
    return status in {"matched", "assigned", "closed"}  # 兼容度高一点


def _matched_at(rec: dict):
    """
    取“匹配时间”字段；没有就退回创建时间
    """
    m = _as_dt(_g(rec, "matched_at", "matched_time", default=None))
    if m:
        return m
    return _as_dt(_g(rec, "created_at", default=None))


# ---------- 自包含的取数逻辑（与页面一致，且不依赖其它控制器） ----------
def _collect_rows_between(since: datetime, until: datetime):
    """
    遍历 request_repo，抽取 [since, until] 区间内“已匹配”的请求，返回扁平化行
    """
    rows = []
    for r in request_repo.list_all():
        if not isinstance(r, dict):  # 你的仓库返回 dict；若是对象可做 getattr 处理
            continue
        if not _is_matched(r):
            continue

        m_at = _matched_at(r)
        if not m_at:
            continue
        if not (since <= m_at <= until):
            continue

        owner = _g(r, "owner_username", "pin_username", "owner", "pin_user_id", "owner_id", default="")
        matched_to = _g(r, "matched_to_username", "matched_to", default="")

        rows.append({
            "id": _g(r, "id", default=""),
            "title": _g(r, "title", default=""),
            "category": _g(r, "category_name", "category", default=""),
            "owner": owner,
            "matched_to": matched_to,
            "matched_at": m_at.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": (_as_dt(_g(r, "created_at", default=None)) or m_at).strftime("%Y-%m-%d %H:%M:%S"),
        })
    return rows


# ---------- 页面：列出可保存的报告（已生成、未删除） ----------
@bp.get("/")
def list_reports():
    reports = [r for r in report_repo.list_all() if getattr(r, "deleted", False) is False]
    # 你已有“删除页面”也可以复用这个列表模板；这里单独给一个简单模板名
    return render_template("pm_save_report.html", reports=reports)


# ---------- 下载 CSV ----------
@bp.get("/csv/<int:report_id>")
def download_csv(report_id: int):
    report = report_repo.get_by_id(report_id)
    if not report:
        flash("Report not found.", "warning")
        return redirect(url_for("pm_save_report.list_reports"))

    # 以 report.created_at 作为右端点，确保与“生成/查看”报表一致
    right = report.created_at if isinstance(report.created_at, datetime) else _as_dt(report.created_at) or datetime.utcnow()
    since, until = _window_by_period(getattr(report, "period", "weekly"), right)

    rows = _collect_rows_between(since, until)

    # 生成 CSV
    import csv, io
    header = ["id", "title", "category", "owner", "matched_to", "matched_at", "created_at"]
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(header)
    for row in rows:
        w.writerow([row.get(k, "") for k in header])

    data = buf.getvalue()
    filename = f"{report.period}_{right.strftime('%Y%m%d_%H%M%S')}.csv"

    resp = make_response(data)
    resp.headers["Content-Type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp
