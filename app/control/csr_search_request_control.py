# app/control/csr_search_request_control.py
from datetime import datetime
from types import SimpleNamespace
from typing import Any

from ..extensions import request_repo, user_repo          # 你们全局注册的仓库实例（方案B）

class CSRSearchRequestControl:
    """CSR 侧：查看所有 PIN 创建的请求"""
    def __init__(self, req_repo=request_repo, usr_repo=user_repo):
        self._repo = req_repo
        self._user_repo = usr_repo

    def list_all_requests(self):
        # 兼容不同仓库命名
        if hasattr(self._repo, "list_all"):
            items = self._repo.list_all()
        elif hasattr(self._repo, "get_all"):
            items = self._repo.get_all()
        else:
            items = []

        # Ensure deterministic ordering for the UI while keeping repository order intact
        view_models = [self._to_view_model(item) for item in items]

        def sort_key(row: SimpleNamespace):
            created = getattr(row, "created_at", None)
            if isinstance(created, datetime):
                return created
            return getattr(row, "id", 0)

        return sorted(view_models, key=sort_key, reverse=True)

        return [self._to_view_model(item) for item in items]

    def _to_view_model(self, obj: Any) -> SimpleNamespace:
        if isinstance(obj, dict):
            data = obj
            pick = lambda *names, default="": next((data[n] for n in names if n in data and data[n] is not None), default)
        else:
            pick = lambda *names, default="": next((getattr(obj, n) for n in names if hasattr(obj, n) and getattr(obj, n) is not None), default)

        owner = pick("owner_username", "pin_username", "username", default="") or self._resolve_owner_by_id(
            pick("owner_id", "user_id", "pin_user_id", default=None)
        )

        return SimpleNamespace(
            id=pick("id", "request_id", default=""),
            title=pick("title", "name", default=""),
            category=pick("category", "category_name", default=""),
            display_owner=owner or "",
            pin_user_id=pick("pin_user_id", "user_id", default=""),
            status=pick("status", default="Open"),
            description=pick("description", default=""),
            created_at=pick("created_at", default=""),
        )

    def _resolve_owner_by_id(self, uid):
        if uid is None or not hasattr(self._user_repo, "get_by_id"):
            return ""
        user = self._user_repo.get_by_id(uid)
        if not user:
            return ""
        return getattr(user, "username", "") or getattr(user, "email", "")
