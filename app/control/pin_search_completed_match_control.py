# app/control/pin_search_completed_match_control.py
from typing import List, Optional, Dict, Any
from flask import session
from ..extensions import user_repo

class PinSearchCompletedMatchControl:
    """
    提供 PIN 用户端：按 category 过滤查看匹配结果
    - matched_to_me: 别人发的、分配给我的
    - my_matched: 我发的、分配给其它 PIN 的
    """

    def __init__(self, request_repo, category_repo=None):
        self._req = request_repo
        self._cat = category_repo

    # 供页面下拉用
    def list_categories(self) -> List[str]:
        names: List[str] = []
        if self._cat:
            # 兼容 list_all()/all() / values()
            if hasattr(self._cat, "list_all"):
                items = self._cat.list_all()
            elif hasattr(self._cat, "all"):
                items = self._cat.all()
            else:
                items = getattr(self._cat, "values", lambda: [])()
            for c in items:
                name = getattr(c, "name", None) or getattr(c, "category", None) or str(c)
                if name and name not in names:
                    names.append(name)
        return names

    def _req_category(self, r) -> str:
        return (getattr(r, "category", None)
                or getattr(r, "category_name", None)
                or "")

    def _req_owner_username(self, r) -> str:
        return (getattr(r, "owner_username", None)
                or getattr(r, "pin_username", None)
                or getattr(r, "username", None)
                or "")

    def _req_matched_flag(self, r) -> bool:
        if hasattr(r, "is_matched"):
            return bool(getattr(r, "is_matched"))
        return bool(getattr(r, "matched", False))

    def _req_matched_username(self, r) -> str:
        # 常见几种命名都兼容
        return (getattr(r, "matched_pin_username", None)
                or getattr(r, "matched_to_username", None)
                or getattr(r, "matched_pin", None)
                or "")

    def _req_id(self, r) -> int:
        return int(getattr(r, "id", 0))

    def _req_title(self, r) -> str:
        return getattr(r, "title", "")

    def _req_status(self, r) -> str:
        return getattr(r, "status", "Open")

    def _req_created_at(self, r) -> str:
        return str(getattr(r, "created_at", ""))

    def search(self, category: Optional[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        返回两个列表：
        - matched_to_me：别人发的、匹配给我的
        - my_matched：我发的、匹配给其他 PIN 的
        category 为 None/'All' 则不过滤
        """
        current_pin_id = session.get("pin_user_id")
        current_pin_username = session.get("pin_username", "")

        # 新增：一次性构建 id->username
        id2name = {u.id: getattr(u, "username", "") for u in user_repo.list_all()}

        # 取所有 request（做兼容）
        if hasattr(self._req, "list_all"):
            all_req = self._req.list_all()
        elif hasattr(self._req, "get_all"):
            all_req = self._req.get_all()
        else:
            all_req = list(getattr(self._req, "_items", {}).values())

        def pack(r):
            return {
                "id": self._req_id(r),
                "title": self._req_title(r),
                "category": self._req_category(r),
                "status": self._req_status(r),
                "created_at": self._req_created_at(r),
                "owner_username": owner_name,
                "matched_to": self._req_matched_username(r),
            }

        want_cat = (category or "").strip()
        matched_to_me, my_matched = [], []

        for r in all_req:
            cat = self._req_category(r)
            if want_cat and want_cat.lower() != "all" and cat != want_cat:
                continue

            matched = self._req_matched_flag(r)
            matched_to_user = self._req_matched_username(r)
            owner_id = int(getattr(r, "owner_id", 0) or getattr(r, "pin_user_id", 0))
            owner_name = (
                    self._req_owner_username(r) or id2name.get(owner_id, "")
            )

            if matched:
                # 分两类：
                # 1) 别人发的，分配给我
                if matched_to_user == current_pin_username and owner_id != current_pin_id and owner_name != current_pin_username:
                    matched_to_me.append(pack(r))
                # 2) 我发的，分配给其它 PIN
                if owner_id == current_pin_id or owner_name == current_pin_username:
                    if matched_to_user and matched_to_user != current_pin_username:
                        my_matched.append(pack(r))

        return {"matched_to_me": matched_to_me, "my_matched": my_matched}
