from ..entity.user_profile_repository import InMemoryUserProfileRepository
from .create_user_profile_control import DEFAULT_PROFILES

class ViewUserProfileControl:
    """Provides a simple control layer for viewing all UserProfiles"""

    def __init__(self, repo: InMemoryUserProfileRepository) -> None:
        self.repo = repo
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        """
        Defensive measures include ensuring that the four default profiles exist
        (if they don't already).
        """
        for name in DEFAULT_PROFILES:
            if self.repo.get_by_name(name) is None:
                self.repo.add(name)

    def list_all(self):
        """Return all UserProfiles in the repository"""
        return self.repo.get_all()
