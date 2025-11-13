from typing import List, Set
from ..entity.request import Request
from ..extensions import request_repo, category_repo


class RequestNotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass



class PinUpdateRequestControl:
    def __init__(self, repo=request_repo) -> None:
        self._repo = repo

    def active_categories(self) -> List[str]:
        """
        Provided to the HTML dropdown: A list of currently active service category names.
        """
        return [c.name for c in category_repo.get_all() if c.status == "Active"]

    def _allowed_set(self) -> Set[str]:
        return set(self.active_categories())

    def list_requests_for_user(self, pin_user_id: int) -> List[Request]:
        """
        Update entry point: First,
        list all requests from the current PIN user.
        """
        return self._repo.get_all_for_user(pin_user_id)

    def get_request_for_edit(self, req_id: int, pin_user_id: int) -> Request:
        """Get a request when opening the editing page"""
        req = self._repo.get(req_id)
        if req is None:
            raise ValueError(f"Request id {req_id} not found")
        if req.pin_user_id != pin_user_id:
            raise PermissionError("You are not allowed to edit this request.")

        return req

    def update_request(
            self,
            req_id: int,
            pin_user_id: int,
            title: str,
            service_category: str,
            description: str,
    ) -> Request:
        # First, retrieve the original request.
        req = self._repo.get(req_id)
        if req is None:
            raise ValueError(f"Request id {req_id} not found")
        if req.pin_user_id != pin_user_id:
            raise PermissionError("You are not allowed to edit this request.")

        # check
        errors = {}
        title = (title or "").strip()
        service_category = (service_category or "").strip()
        description = (description or "").strip()

        if not title:
            errors["title"] = "Title is required."
        elif len(title) < 3:
            errors["title"] = "Title must be at least 3 characters."

        allowed = self._allowed_set()
        if service_category not in allowed:
            errors["category"] = "Please select a valid service category."

        if not description:
            errors["description"] = "Description is required."
        elif len(description) < 10:
            errors["description"] = "Description must be at least 10 characters."

        if errors:
            raise ValidationError(str(errors))

        # Modify fields
        req.title = title.strip()
        req.category = service_category
        req.description = description.strip()

        # Save back to warehouse
        return self._repo.update(req)

