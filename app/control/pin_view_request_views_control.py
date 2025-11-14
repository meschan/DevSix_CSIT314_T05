from dataclasses import dataclass
from typing import List
from flask import session
from ..extensions import request_repo  # ★ 用全局单例
# 如果需要显示更多字段，按你的 Request 实体加即可
@dataclass
class RequestViewRow:
    id: int
    title: str
    category: str
    status: str
    created_at: str
    views: int

class PinViewRequestViewsControl:
    def list_my_views(self) -> List[RequestViewRow]:
        pin_user_id = session.get("pin_user_id")
        if pin_user_id is None:
            return []  # 或抛出未登录

        # ★ 关键：用仓库现有方法按 pin_user_id 过滤
        my_requests = request_repo.get_all_for_user(pin_user_id)

        rows: List[RequestViewRow] = []
        for r in my_requests:
            rows.append(
                RequestViewRow(
                    id=getattr(r, "id", 0),
                    title=getattr(r, "title", ""),
                    category=(getattr(r, "category", None)
                              or getattr(r, "category_name", "")),
                    status=getattr(r, "status", "Open"),
                    created_at=str(getattr(r, "created_at", "")),
                    views=int(getattr(r, "views", 0)),  # CSR view 时会 +1
                )
            )
        return rows
