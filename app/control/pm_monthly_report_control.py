from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from ..extensions import report_repo
from ..entity.report import Report

class PMMonthlyReportControl:
    def __init__(self, request_repo, user_repo=None):
        self._request_repo = request_repo
        self._user_repo = user_repo
        self.report_repo = report_repo

    # ----------------- 小工具 -----------------
    def _get(self, r: Any, *names: str, default: Any = "") -> Any:
        for n in names:
            if hasattr(r, n):
                v = getattr(r, n, None)
                if v not in (None, ""):
                    return v
        if isinstance(r, dict):
            for n in names:
                if n in r and r[n] not in (None, ""):
                    return r[n]
        return default

    def _to_dt(self, v: Any) -> Optional[datetime]:
        if v is None or v == "":
            return None
        if isinstance(v, datetime):
            return v
        s = str(v).strip()
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
        except Exception:
            return None

    def _r_id(self, r: Any) -> str:
        return str(self._get(r, "id", "req_id", default=""))

    def _r_title(self, r: Any) -> str:
        return str(self._get(r, "title", default=""))

    def _r_category(self, r: Any) -> str:
        return str(self._get(r, "category", "category_name", default=""))

    def _r_owner_id(self, r: Any) -> Any:
        return self._get(r, "pin_user_id", "owner_id", default=None)

    def _r_owner_name(self, r: Any) -> str:
        name = self._get(r, "owner_username", "pin_username", default="")
        if name:
            return str(name)
        uid = self._r_owner_id(r)
        if uid and self._user_repo and hasattr(self._user_repo, "get_by_id"):
            u = self._user_repo.get_by_id(uid)
            if u:
                return str(self._get(u, "username", default=""))
        return ""

    def _r_matched_to(self, r: Any) -> str:
        return str(self._get(r, "matched_to", "matched_to_username", default=""))

    def _r_matched_at(self, r: Any) -> Optional[datetime]:
        dt = self._to_dt(self._get(r, "matched_at", "matched_time", "matched_ts", default=None))
        return dt

    def _r_created_at(self, r: Any) -> str:
        return str(self._get(r, "created_at", default=""))

    def _r_is_matched(self, r: Any) -> bool:
        return bool(self._r_matched_to(r))

    def _pack_row(self, r: Any) -> Dict[str, Any]:
        return {
            "id": self._r_id(r),
            "title": self._r_title(r),
            "category": self._r_category(r),
            "owner": self._r_owner_name(r),
            "matched_to": self._r_matched_to(r),
            "matched_at": self._r_matched_at(r),
            "created_at": self._r_created_at(r),
        }

    # ----------------- 页面用主方法 -----------------
    def list_last_30days(self) -> List[Dict[str, Any]]:

        now = datetime.utcnow()
        threshold = now - timedelta(days=30)

        items = []
        for r in self._request_repo.list_all():
            if not self._r_is_matched(r):
                continue
            m_at = self._r_matched_at(r)
            if m_at is None:
                continue
            if m_at >= threshold:
                items.append(self._pack_row(r))

        items.sort(key=lambda x: x["matched_at"] or datetime.min, reverse=True)

        for it in items:
            if isinstance(it["matched_at"], datetime):
                it["matched_at"] = it["matched_at"].isoformat(sep=" ", timespec="seconds")
        return items

    def generate(self):
        since = datetime.utcnow() - timedelta(days=30)
        items = self._request_repo.list_matched_since(since)
        title = "Monthly Matched Report (Last 30 days)"

        report = Report(
            id=None,
            title=title,
            period="monthly",  # weekly / monthly 对应填 "weekly"/"monthly"
            created_at=datetime.utcnow(),  # 或你项目里习惯的时区
            items=items  # 直接塞列表即可
        )
        report_repo.add(report)  # ★ 关键一步：存入全局仓库

        return report
