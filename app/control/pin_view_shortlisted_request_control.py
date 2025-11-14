# app/control/pin_view_shortlisted_request_control.py
from dataclasses import dataclass
from typing import List
from flask import session
from ..extensions import request_repo, shortlist_repo  # 用你的全局单例

@dataclass
class SavedRow:
    id: int
    title: str
    category: str
    status: str
    created_at: str
    saved_count: int

class PinViewShortlistedRequestControl:
    def list_my_saved(self) -> List[SavedRow]:
        """
        返回当前 PIN 用户自己创建的所有请求；并给出该请求是否被保存过（0/1）
        注意：你当前业务约束是“同一 request 只会被保存一次（全局集合）”，
             因此计数 = 1 if is_saved else 0。
        """
        pin_user_id = session.get("pin_user_id")
        if pin_user_id is None:
            return []

        my_requests = request_repo.get_all_for_user(pin_user_id)

        rows: List[SavedRow] = []
        for r in my_requests:
            req_id = getattr(r, "id", 0)

            # 兼容不同命名：is_saved / contains / has
            if hasattr(shortlist_repo, "is_saved"):
                is_saved = bool(shortlist_repo.is_saved(req_id))
            elif hasattr(shortlist_repo, "contains"):
                is_saved = bool(shortlist_repo.contains(req_id))
            elif hasattr(shortlist_repo, "has"):
                is_saved = bool(shortlist_repo.has(req_id))
            else:
                is_saved = False

            rows.append(
                SavedRow(
                    id=req_id,
                    title=getattr(r, "title", ""),
                    category=(getattr(r, "category", None)
                              or getattr(r, "category_name", "")),
                    status=getattr(r, "status", "Open"),
                    created_at=str(getattr(r, "created_at", "")),
                    saved_count=1 if is_saved else 0,
                )
            )
        return rows