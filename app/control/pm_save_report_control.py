# app/control/pm_save_report_control.py
from __future__ import annotations

import io
import csv
from datetime import datetime
from typing import List, Tuple, Optional, Any

from ..extensions import report_repo   # 你现成的全局仓库
# 若你的 Report 类型在 entity 中有定义，可按需引入以获得类型提示
# from ..entity.report import Report


def _get(obj: Any, *names: str, default: Any = "") -> Any:
    """容错取值：先按属性，再按字典键。"""
    for n in names:
        if hasattr(obj, n):
            v = getattr(obj, n, None)
            if v not in (None, ""):
                return v
    if isinstance(obj, dict):
        for n in names:
            if n in obj and obj[n] not in (None, ""):
                return obj[n]
    return default


def _to_dt(v: Any) -> Optional[datetime]:
    if v in (None, ""):
        return None
    if isinstance(v, datetime):
        return v
    s = str(v).strip()
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None


def _pack_row(item: Any) -> list[str]:
    """把报表里的单条 request（对象/字典）拍平成 CSV 一行"""
    rid = _get(item, "id", "req_id", default="")
    title = _get(item, "title", default="")
    category = _get(item, "category", "category_name", default="")

    # owner：尽量兼容各种字段名
    owner = _get(item, "owner", "owner_username", "pin_username",
                 "pin_user_name", "user_name", default="")

    matched_to = _get(item, "matched_to", "matched_to_username", default="")
    matched_at = _get(item, "matched_at", "matched_time", "matched_ts", default="")
    dt = _to_dt(matched_at)
    if dt:
        matched_at = dt.isoformat(sep=" ", timespec="seconds")

    created_at = _get(item, "created_at", default="")
    return [str(rid), str(title), str(category), str(owner),
            str(matched_to), str(matched_at), str(created_at)]


class PMSaveReportControl:
    """保存报表（导出 CSV）的控制器"""

    def __init__(self) -> None:
        # 直接使用全局仓库；如需注入，可改为接收参数
        self._repo = report_repo

    # —— 页面用：列出所有未删除的报表（你删除的在仓库里已不存在） ——
    def list_reports(self) -> List[Any]:
        # report_repo.list_all() 返回你之前 generate 后存进去的 Report 列表
        return self._repo.list_all()

    # —— 业务用：根据 report_id 生成 CSV 文本与建议下载文件名 ——
    def build_csv_by_id(self, report_id: int) -> Tuple[str, str]:
        report = self._find_report(report_id)
        if report is None:
            raise ValueError("Report not found")

        # 组装 CSV
        buf = io.StringIO(newline="")             # 兼容 Excel/Windows
        writer = csv.writer(buf)
        writer.writerow(["id", "title", "category",
                         "owner", "matched_to", "matched_at", "created_at"])

        items = getattr(report, "items", []) or []
        for it in items:
            writer.writerow(_pack_row(it))

        # 文件名：Title_YYYYmmdd_HHMMSS.csv
        title = getattr(report, "title", "report")
        safe_title = str(title).replace("/", "_").replace("\\", "_")
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_title}_{ts}.csv"

        return filename, buf.getvalue()

    # —— 内部工具：找报表 ——
    def _find_report(self, report_id: int) -> Optional[Any]:
        for r in self._repo.list_all():
            if str(getattr(r, "id", "")) == str(report_id):
                return r
        return None
