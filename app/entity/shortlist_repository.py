# now can run!!!
from typing import Iterable, Set

class InMemoryShortlistRepository:
    """
    只保存已加入 shortlist 的 request_id 集合。
    """
    def __init__(self) -> None:
        self._ids: Set[int] = set()

    # 查询
    def is_saved(self, request_id: int) -> bool:
        return request_id in self._ids

    def list_all_ids(self) -> Iterable[int]:
        return list(self._ids)

    # 修改
    def add(self, request_id: int) -> None:
        self._ids.add(int(request_id))

    def remove(self, request_id: int) -> None:
        self._ids.discard(int(request_id))

    def clear(self) -> None:
        self._ids.clear()
















# dont remember maybe csr can save many times
'''from typing import Iterable, Set, Dict
from ..entity.request import Request
class InMemoryShortlistRepository:
    """
    只保存已加入 shortlist 的 request_id 集合。
    """
    def __init__(self) -> None:
        self._by_user: Dict[str, Set[int]] = {}
        self._global_ids: Set[int] = set()

    # 查询
    def is_saved(self, request_id: int) -> bool:
        return request_id in self._global_ids

    def list_all_ids(self) -> Iterable[int]:
        return list(self._global_ids)

    # 修改
    def add(self, request_id: int) -> None:
        self._global_ids.add(int(request_id))

    def remove(self, request_id: int) -> None:
        self._global_ids.discard(int(request_id))

    def clear(self) -> None:
        self._global_ids.clear()
        self._by_user.clear()

    # ---------- 新接口（按 CSR 用户名） ----------
    def _bucket(self, username: str) -> Set[int]:
        if username not in self._by_user:
            self._by_user[username] = set()
        return self._by_user[username]

    def is_saved_for(self, username: str, request_id: int) -> bool:
        return int(request_id) in self._bucket(username)

    def add_for(self, username: str, request_id: int) -> None:
        self._bucket(username).add(int(request_id))

    def remove_for(self, username: str, request_id: int) -> None:
        self._bucket(username).discard(int(request_id))

    def list_ids_for(self, username: str) -> Iterable[int]:
        return list(self._bucket(username))
'''
