from dataclasses import dataclass
from typing import List
from ..entity.user_repository import UserRepository
from ..entity.user_profile_repository import InMemoryUserProfileRepository
from ..extensions import user_repo, user_profile_repo


@dataclass
class SearchResult:
    profile_name: str
    users: List  # List[UserAccount]，


class SearchUserProfileControl:
    def __init__(
        self,
        user_repo: UserRepository = user_repo,
        profile_repo: InMemoryUserProfileRepository = user_profile_repo,
    ) -> None:
        self._user_repo = user_repo
        self._profile_repo = profile_repo

    # Used by boundary to render dropdown lists: retrieve all profiles
    def get_all_profiles(self):
        return self._profile_repo.get_all()

    # Quick tool: Find profiles by ID in the results of get_all()
    def _find_profile_by_id(self, profile_id: int):
        for p in self._profile_repo.get_all():
            if p.id == profile_id:
                return p
        return None

    def search(self, profile_id: int) -> SearchResult:
        """
        Find all users who currently own the profile based on profile_id.

        """
        profile = self._find_profile_by_id(profile_id)
        if not profile:
            raise ValueError("Selected profile does not exist.")

        target = profile.name.lower()

        all_users = self._user_repo.list_all()
        matched = []
        for u in all_users:
            role_text = str(getattr(u.role, "value", u.role)).lower()
            if target in role_text:
                matched.append(u)

        return SearchResult(profile_name=profile.name, users=matched)
