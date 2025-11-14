# app/control/csr_save_volunteer_request_control.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RequestRow:
    id: Optional[int]
    title: str
    category: str
    owner_username: str
    status: str
    description: str

class CSRSaveVolunteerRequestControl:
    """
    - list_available(): 返回尚未被保存到 shortlist 的所有请求
    - save_to_shortlist(req_id): 保存并返回 (ok, msg)
    """
    def __init__(self, request_repo, user_repo, shortlist_repo) -> None:
        self._req_repo = request_repo
        self._user_repo = user_repo
        self._shortlist = shortlist_repo

    def list_available(self) -> List[RequestRow]:
        users = self._user_repo.list_all()
        id_to_username = {u.id: getattr(u, "username", "") for u in users}

        items = self._req_repo.list_all()
        rows: List[RequestRow] = []
        for r in items:
            rid = getattr(r, "id", None)
            if rid is None:
                continue
            if self._shortlist.is_saved(rid):
                continue  # 已在 shortlist 的不显示

            category = getattr(r, "category", "") or getattr(r, "category_name", "")
            owner = id_to_username.get(getattr(r, "pin_user_id", None), "")
            rows.append(RequestRow(
                id=rid,
                title=getattr(r, "title", ""),
                category=category,
                owner_username=owner,
                status=getattr(r, "status", "Open"),
                description=getattr(r, "description", "")
            ))

        rows.sort(key=lambda x: (x.id is None, x.id))
        return rows

    def save_to_shortlist(self, request_id: int) -> tuple[bool, str]:
        # 尝试找到该 request
        target = None
        get_by_id = getattr(self._req_repo, "get_by_id", None)
        if callable(get_by_id):
            target = get_by_id(request_id)
        if target is None:
            for r in self._req_repo.list_all():
                if getattr(r, "id", None) == request_id:
                    target = r
                    break
        if target is None:
            return False, "Request not found."

        if self._shortlist.is_saved(request_id):
            return True, "Already in shortlist."

        self._shortlist.add(request_id)
        return True, "Saved to shortlist."
