from typing import Dict, Set
from ..entity.request import Request
from ..extensions import request_repo, category_repo




class RequestValidationError(Exception):
    """Includes field error information"""

    def __init__(self, errors: Dict[str, str]) -> None:
        self.errors = errors
        super().__init__("Invalid request data")


class CreateRequestControl:
    def __init__(self, repo=request_repo) -> None:
        self.repo = repo

    def _active_categories(self) -> Set[str]:
        """
        Retrieve the set of currently available (Active) category names
         from the shared repository for validation and backfilling.
        """
        return {c.name for c in category_repo.get_all() if c.status == "Active"}

    def create(self, pin_user_id: int, title: str, category: str,
               description: str) -> Request:
        errors: Dict[str, str] = {}

        title = (title or "").strip()
        category = (category or "").strip()
        description = (description or "").strip()

        if not title:
            errors["title"] = "Title is required."
        elif len(title) < 3:
            errors["title"] = "Title must be at least 3 characters."

        allowed = self._active_categories()
        if category not in allowed:
            errors["category"] = "Please select a valid service category."

        if not description:
            errors["description"] = "Description is required."
        elif len(description) < 10:
            errors["description"] = "Description must be at least 10 characters."

        if errors:
            raise RequestValidationError(errors)

        req = Request(
            id=0,  # It will be reassigned in repo.add
            pin_user_id=pin_user_id,
            title=title,
            category=category,
            description=description,
        )
        return self.repo.add(req)
