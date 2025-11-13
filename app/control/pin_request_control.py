from dataclasses import dataclass
from typing import List
from ..entity.request import Request
from ..extensions import request_repo

class RequestNotFoundError(Exception):
    pass

@dataclass
class PinRequestControl:
    repo = request_repo

    def list_for_user(self, pin_user_id: int) -> List[Request]:
        """List all requests from a user with a specific PIN."""
        return self.repo.list_for_user(pin_user_id)

    def get_for_user(self, pin_user_id: int, request_id: int) -> Request:
        """Retrieve a specific request belonging to the current PIN"""
        req = self.repo.get(request_id)
        if not req or req.pin_user_id != pin_user_id:
            raise RequestNotFoundError("Request not found.")
        return req
