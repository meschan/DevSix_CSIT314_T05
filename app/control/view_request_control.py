from typing import List, Optional
from ..entity.request import Request
from ..extensions import request_repo


class ViewRequestControl:
    def __init__(self, repo=request_repo) -> None:
        self.repo = repo

    def list_for_pin(self, pin_user_id: int) -> List[Request]:
        """Return all requests for this PIN user"""
        return self.repo.get_all_for_user(pin_user_id)

    '''def get_all_for_user(self, pin_user_id: int) -> List[Request]:
        return [r for r in self._items.values() if r.pin_user_id == pin_user_id]'''

    def list_for_user(self, pin_user_id: int) -> List[Request]:
        return self.repo.get_all_for_user(pin_user_id)

    def get_detail(self, req_id: int, pin_user_id: int) -> Optional[Request]:
        """
        Used when viewing individual item details, and also for verifying ownership.
        """
        req = self.repo.get(req_id)
        if not req:
            return None
        if req.pin_user_id != pin_user_id:
            return None
        return req
