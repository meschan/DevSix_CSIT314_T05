from __future__ import annotations

from typing import Dict, List, Set


class InMemoryCsrShortlistRepository:
    """Stores mappings of CSR reps to the opportunity IDs they have shortlisted."""

    def __init__(self) -> None:
        self._shortlists: Dict[int, Set[int]] = {}

    def add(self, csr_user_id: int, opportunity_id: int) -> bool:
        """Add an opportunity to the CSR rep's shortlist.

        Returns ``True`` when the opportunity was newly added and ``False`` when it
        was already present.
        """

        shortlist = self._shortlists.setdefault(csr_user_id, set())
        if opportunity_id in shortlist:
            return False
        shortlist.add(opportunity_id)
        return True

    def get_all_ids(self, csr_user_id: int) -> List[int]:
        """Return all opportunity IDs saved by the CSR rep."""

        return list(self._shortlists.get(csr_user_id, set()))

    def remove(self, csr_user_id: int, opportunity_id: int) -> bool:
        """Remove an opportunity from the CSR rep's shortlist."""

        shortlist = self._shortlists.get(csr_user_id)
        if not shortlist or opportunity_id not in shortlist:
            return False
        shortlist.remove(opportunity_id)
        if not shortlist:
            self._shortlists.pop(csr_user_id, None)
        return True
