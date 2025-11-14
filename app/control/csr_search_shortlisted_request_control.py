# app/control/csr_search_shortlisted_request_control.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ShortlistedRow:
    id: Optional[int]
    title: str
    category: str
    owner_username: str
    status: str
    description: str
    views: int
    created_at: str

class CSRSearchShortlistedRequestControl:
    """
    在 shortlist 中按 keyword 搜索 request：
    - 命中字段：title / category(category_name) / owner_username
    - 全部使用不区分大小写的模糊匹配
    """
    def __init__(self, request_repo, user_repo, shortlist_repo) -> None:
        self._req_repo = request_repo
        self._user_repo = user_repo
        self._shortlist = shortlist_repo

    def _get_request_by_id(self, request_id: int):
        get_by_id = getattr(self._req_repo, "get_by_id", None)
        if callable(get_by_id):
            return get_by_id(request_id)
        # 退化方案
        for r in self._req_repo.list_all():
            if getattr(r, "id", None) == request_id:
                return r
        return None

    def _row_from_request(self, r, id_to_username) -> ShortlistedRow:
        category = getattr(r, "category", "") or getattr(r, "category_name", "")
        owner = id_to_username.get(getattr(r, "pin_user_id", None), "")
        return ShortlistedRow(
            id=getattr(r, "id", None),
            title=getattr(r, "title", ""),
            category=category,
            owner_username=owner,
            status=getattr(r, "status", "Open"),
            description=getattr(r, "description", ""),
            views=int(getattr(r, "views", 0)),
            created_at=str(getattr(r, "created_at", "")),
        )

    def search(self, keyword: str) -> List[ShortlistedRow]:
        kw = (keyword or "").strip().lower()
        if not kw:
            return []

        # 用户字典：id -> username
        users = self._user_repo.list_all()
        id_to_username = {u.id: getattr(u, "username", "") for u in users}

        rows: List[ShortlistedRow] = []
        for rid in self._shortlist.list_all_ids():
            r = self._get_request_by_id(int(rid))
            if not r:
                continue

            title = (getattr(r, "title", "") or "").lower()
            category = ((getattr(r, "category", "") or getattr(r, "category_name", "") or "")).lower()
            owner = (id_to_username.get(getattr(r, "pin_user_id", None), "") or "").lower()

            if kw in title or kw in category or kw in owner:
                rows.append(self._row_from_request(r, id_to_username))

        rows.sort(key=lambda x: (x.id is None, x.id))
        return rows

    def add_view(self, request_id: int) -> tuple[bool, str]:
        r = self._get_request_by_id(request_id)
        if not r:
            return False, "Request not found."

        incr = getattr(self._req_repo, "increment_views", None)
        if callable(incr):
            incr(request_id)
            return True, "View recorded."

        current = int(getattr(r, "views", 0))
        setattr(r, "views", current + 1)
        upd = getattr(self._req_repo, "update", None)
        if callable(upd):
            upd(r)
        return True, "View recorded."
