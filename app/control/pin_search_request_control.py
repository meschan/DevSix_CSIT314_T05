from typing import List
from ..entity.request import Request
from ..extensions import request_repo

class PinSearchRequestControl:

    def __init__(self, repo):
        self.repo = repo

    def search(self, pin_user_id: int, keyword: str) -> List[Request]:
        """
        Requests to search for current PIN users by keyword
        """
        keyword = (keyword or "").strip().lower()
        if not keyword:
            return []

        all_reqs = self.repo.get_all_for_user(pin_user_id)

        results = []
        for r in all_reqs:
            if (
                keyword in (r.title or "").lower()
                or keyword in (r.category or "").lower()
                or keyword in (r.description or "").lower()
            ):
                results.append(r)

        return results


