from typing import Dict, List
from .request import Request

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
