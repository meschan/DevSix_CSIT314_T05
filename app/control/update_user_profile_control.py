from dataclasses import dataclass
from typing import List, Optional
from ..entity.user_repository import UserRepository
from ..entity.user_profile_repository import InMemoryUserProfileRepository
from ..extensions import user_repo, user_profile_repo  # Make sure you are using the same repo instance.
from ..entity.user_account import Role

@dataclass
class UpdateUserProfileResult:
    ok: bool
    message: str

class UpdateUserProfileControl:
    def __init__(
        self,
        user_repo: UserRepository = user_repo,
        profile_repo: InMemoryUserProfileRepository = user_profile_repo,
    ) -> None:
        self._user_repo = user_repo
        self._profile_repo = profile_repo

    def get_form_data(self):
        """
        Return：
        - All user accounts (used for the username dropdown)
        - All user profiles (including default and newly created ones).
        """
        users = self._user_repo.list_all()
        profiles = self._profile_repo.get_all()
        return users, profiles

    # --- Internal utility: Find profiles in the get_all() results by ID ---
    def _find_profile_by_id(self, profile_id: int):
        for p in self._profile_repo.get_all():
            if p.id == profile_id:
                return p
        return None

    # 把 Profile.name → Role enumerate
    def _to_role_enum(self, profile_name: str) -> Optional[Role]:
        name = (profile_name or "").strip().lower()
        mapping = {
            "user admin": Role.USER_ADMIN,
            "pin": Role.PIN,
            "csr rep": Role.CSR_REP,
            "platform manager": Role.PLATFORM_MANAGER,
        }
        return mapping.get(name)

    def update_profile_for_user(self, username: str, profile_id: int) -> UpdateUserProfileResult:
        # 1) Find users
        user = self._user_repo.get_by_username(username)
        if not user:
            return UpdateUserProfileResult(False, f"User '{username}' does not exist.")

        # 2) Find profile
        profile = self._find_profile_by_id(profile_id)
        if not profile:
            return UpdateUserProfileResult(False, "Selected profile does not exist.")

        role_enum = self._to_role_enum(profile.name)
        if role_enum is None:
            return UpdateUserProfileResult(False, f"Unsupported profile: '{profile.name}'.")

        # 3) Update: This simply changes the user's role_name to profile.name.
        user.role = role_enum
        self._user_repo.update(user)

        return UpdateUserProfileResult(True, f"User '{username}' profile has been updated to '{profile.name}'.")
