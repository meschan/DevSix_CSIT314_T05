from typing import List
from ..entity.request import Request
from ..entity.request_repository import InMemoryRequestRepository
from .pin_request_control import RequestNotFoundError
from ..extensions import request_repo  # Sharing the same repo instance


class PinDeleteRequestControl:
    """
    The business logic responsible for handling PIN user deletion requests.
    """
    def __init__(self, repo = None) :
        self.repo = repo or request_repo

    def list_requests(self, pin_user_id: int) -> List[Request]:
        """List all requests from the current PIN user."""
        return self.repo.get_all_for_user(pin_user_id)

    def get_request(self, pin_user_id: int, req_id: int) -> Request:
        """Obtain a specific request from the user for use on the confirmation page."""
        req = self.repo.get_for_user(pin_user_id, req_id)
        if not req:
            raise RequestNotFoundError("The selected request was not found.")
        return req

    def delete_request(self, req_id: int) -> bool:
        return request_repo.delete(req_id)