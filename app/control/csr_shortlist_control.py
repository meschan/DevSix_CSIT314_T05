from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import List

from ..entity.request import Request
from ..extensions import request_repo, csr_shortlist_repo, user_repo


class CSRShortlistControl:
    """Controller for managing CSR representative shortlists."""

    def __init__(self, req_repo=request_repo, shortlist_repo=csr_shortlist_repo, usr_repo=user_repo) -> None:
        self._request_repo = req_repo
        self._shortlist_repo = shortlist_repo
        self._user_repo = usr_repo

    def save_to_shortlist(self, csr_user_id: int, opportunity_id: int) -> str:
        """Save a volunteer opportunity to the CSR rep's shortlist.

        Returns a status string: ``"added"`` when the opportunity was saved,
        ``"exists"`` when it was already present, and ``"missing"`` when the
        opportunity could not be found.
        """

        if csr_user_id is None:
            raise ValueError("CSR user id is required")

        try:
            request = self._request_repo.get(opportunity_id)
        except KeyError:
            return "missing"

        added = self._shortlist_repo.add(csr_user_id, request.id)
        return "added" if added else "exists"

    def get_shortlist(self, csr_user_id: int) -> List[SimpleNamespace]:
        """Return the list of requests saved by the CSR representative."""

        ids = self._shortlist_repo.get_all_ids(csr_user_id)
        shortlisted_requests: List[Request] = []
        for opportunity_id in ids:
            try:
                shortlisted_requests.append(self._request_repo.get(opportunity_id))
            except KeyError:
                # The request may have been deleted; skip silently.
                continue

        # Present the newest saved opportunities first for easier review.
        def sort_key(req: Request):
            created = getattr(req, "created_at", None)
            if isinstance(created, datetime):
                return created
            return getattr(req, "id", 0)

        shortlisted_requests.sort(key=sort_key, reverse=True)
        return [self._to_view_model(req) for req in shortlisted_requests]

    def _to_view_model(self, request: Request) -> SimpleNamespace:
        owner_name = ""
        if hasattr(self._user_repo, "get_by_id"):
            owner = self._user_repo.get_by_id(getattr(request, "pin_user_id", None))
            if owner:
                owner_name = getattr(owner, "username", "") or getattr(owner, "email", "")

        return SimpleNamespace(
            id=request.id,
            title=getattr(request, "title", ""),
            category=getattr(request, "category", ""),
            display_owner=owner_name,
            pin_user_id=getattr(request, "pin_user_id", ""),
            status=getattr(request, "status", "Open"),
            description=getattr(request, "description", ""),
            created_at=getattr(request, "created_at", ""),
        )
