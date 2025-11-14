from typing import Dict, List, Optional, Any
from .request import Request
from datetime import datetime, timedelta

class InMemoryRequestRepository:
    def __init__(self) -> None:
        self._items: Dict[int, Request] = {}
        self._next_id: int = 1

    def add(self, req: Request) -> Request:
        req.id = self._next_id
        self._items[self._next_id] = req
        self._next_id += 1
        return req

    def get_all_for_user(self, pin_user_id: int) -> List[Request]:
        return [r for r in self._items.values() if r.pin_user_id == pin_user_id]

    # For use in the update controller layer
    def get_for_user(self, pin_user_id: int, req_id: int) -> Request | None:
        # Retrieve request by ID first
        req = self._items.get(req_id)

        # Next, check if this request belongs to the currently logged-in user with a PIN.
        if req and req.pin_user_id == pin_user_id:
            return req
        return None

    def get(self, req_id: int) -> Request:
        return self._items[req_id]

    def update(self, req: Request) -> Request:
        if req.id not in self._items:
            raise KeyError(f"Request #{req.id} not found")
        self._items[req.id] = req
        return req

    def delete(self, req_id: int) -> bool:
        """
        Delete the request with the specified ID.
        """
        if req_id in self._items:
            del self._items[req_id]
            return True
        return False

    def list_all(self) -> List[Request]:
        """
        返回系统中所有请求（跨所有 PIN 用户）。
        不改变现有数据结构与行为，仅做只读聚合。
        """
        return list(self._items.values())

    def get_all(self) -> List[Request]:
        """
        与 list_all 等价，提供向后兼容的别名，防止控制层
        或模板里有人用 get_all 的调用方式。
        """
        return self.list_all()

    def get_by_id(self, req_id: int) -> Request | None:
        return self._items.get(req_id)

    def mark_matched(self, request_id: int, matched_to_username: str) -> bool:
        r = self._items.get(request_id)
        if not r:
            return False
        r.matched_to_username = matched_to_username
        r.matched_at = datetime.utcnow()  # <—— 关键：写入匹配时间
        return True

    def list_matched_since(self, since_dt: datetime) -> List[Request]:
        return sorted(
            [
                r for r in self._items.values()
                if r.matched_to_username and r.matched_at and r.matched_at >= since_dt
            ],
            key=lambda x: x.matched_at,
            reverse=True
        )