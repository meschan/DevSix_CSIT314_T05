# app/control/csr_search_request_control.py
from dataclasses import dataclass
from typing import List, Dict, Any

from ..entity.request_repository import InMemoryRequestRepository
from ..entity.user_repository import UserRepository


@dataclass
class SearchRow:
    id: int | str
    title: str
    category: str
    owner_username: str
    status: str
    description: str
    created_at: str

class CSRSearchRequestControl:
    """
    CSR 搜索 PIN 的 Request。
    - 不改实体/仓库签名；
    - 仅在提交查询时返回结果；
    - Owner 通过 user_repo 的用户表(按 id 建索引)解析。
    """
    def __init__(
        self,
        request_repo: InMemoryRequestRepository,
        user_repo: UserRepository,
    ) -> None:
        self._req_repo = request_repo
        self._user_repo = user_repo

    def _users_by_id(self) -> Dict[int, Any]:
        # user_repo 没有 get_by_id，用 list_all 自己建索引即可。 :contentReference[oaicite:0]{index=0}
        return {u.id: u for u in self._user_repo.list_all()}

    def search(self, mode: str, keyword: str) -> List[SearchRow]:
        mode = (mode or "").lower().strip()
        q = (keyword or "").strip()
        if not mode or not q:
            # 没有提交有效查询 -> 不返回任何结果（页面显示为空）
            return []

        # 取全量，再在内存中过滤（不改仓库层接口）。 :contentReference[oaicite:1]{index=1}
        items = self._req_repo.list_all()

        # 解析 Owner
        users = self._users_by_id()

        def owner_name(pin_user_id: int | None) -> str:
            u = users.get(pin_user_id or -1)
            return (u.username if u else "") or ""

        # 统一取字段的工具
        def get(obj, name, default=""):
            return getattr(obj, name, default) or default

        # 归一化类别字段（兼容你历史字段名）
        def cat_of(r) -> str:
            return (get(r, "category") or get(r, "category_name")).strip()

        q_low = q.lower()
        if mode == "category":
            items = [r for r in items if cat_of(r).lower() == q_low]
        elif mode == "username":
            # 与 owner 用户名比对（大小写不敏感）
            items = [
                r for r in items
                if owner_name(get(r, "pin_user_id")).lower() == q_low
            ]
        elif mode == "title":
            items = [r for r in items if q_low in get(r, "title", "").lower()]
        else:
            # 未知模式 -> 返回空
            return []

        rows: List[SearchRow] = []
        for r in items:
            rows.append(
                SearchRow(
                    id=get(r, "id", ""),
                    title=get(r, "title", ""),
                    category=cat_of(r),
                    owner_username=owner_name(get(r, "pin_user_id")),
                    status=get(r, "status", "Open"),
                    description=get(r, "description", ""),
                    created_at=str(get(r, "created_at", "")),
                )
            )
        return rows
