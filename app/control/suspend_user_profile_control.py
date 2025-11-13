from dataclasses import dataclass
from typing import List, Optional
from ..entity.user_profile_repository import InMemoryUserProfileRepository
from ..entity.user_profile import UserProfile
from ..extensions import user_profile_repo

@dataclass
class SuspendProfileResult:
    ok: bool
    message: str
    profile: Optional[UserProfile] = None

class SuspendUserProfileControl:
    def __init__(self, profile_repo: InMemoryUserProfileRepository = user_profile_repo) -> None:
        self._profile_repo = profile_repo

    def list_profiles(self) -> List[UserProfile]:
        """
        Returns all user profiles (4 default values + newly created ones)
        for use in the dropdown list.
        """
        return self._profile_repo.get_all()

    def suspend(self, profile_id: int) -> SuspendProfileResult:
        """
        Set the status of the specified profile to 'Suspended'.
        """
        profiles = self._profile_repo.get_all()

        target: Optional[UserProfile] = None
        for p in profiles:
            if p.id == profile_id:
                target = p
                break

        if not target:
            return SuspendProfileResult(False, "Selected user profile does not exist.", None)

        if target.status == "Suspended":
            return SuspendProfileResult(False,
                                       f"User profile '{target.name}' is already suspended.",
                                       target)

        target.status = "Suspended"

        return SuspendProfileResult(True,
                                    f"User profile '{target.name}' has been suspended.",
                                    target)
