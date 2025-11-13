# app/control/pm_login_control.py
from dataclasses import dataclass
from typing import Optional
from ..entity.user_account import UserAccount, Role
from ..entity.user_repository import UserRepository
from ..extensions import user_repo
from werkzeug.security import check_password_hash


class PMAuthenticationError(Exception):
    pass


@dataclass
class PMLoginResult:
    user: UserAccount


class PMLoginControl:
    def __init__(self, repo: UserRepository = user_repo) -> None:
        self._repo = repo

    def authenticate(self, username: str, password: str) -> PMLoginResult:
        """
        仅允许 Platform Manager 登录；Suspended 一律拒绝。
        """
        user: Optional[UserAccount] = self._repo.get_by_username(username)
        if not user:
            raise PMAuthenticationError("User does not exist.")

        # 状态判断：被 Suspend 的账号不允许登录（与 suspend 页面一致）
        # suspend/activate 改 status 的实现见你现有的 suspend 代码。:contentReference[oaicite:0]{index=0}
        if user.status.lower() == "suspended":
            raise PMAuthenticationError("Account is suspended. Please contact an administrator.")

        # 角色判断：必须是 Platform Manager
        if (isinstance(user.role, Role) and user.role != Role.PLATFORM_MANAGER) or \
           (not isinstance(user.role, Role) and str(user.role).lower() != "platform manager"):
            raise PMAuthenticationError("Only Platform Manager can sign in here.")

        if not user.password_hash or not check_password_hash(user.password_hash, password):
            raise PMAuthenticationError("Invalid username or password.")

        return PMLoginResult(user=user)










'''from dataclasses import dataclass
from typing import Optional
from werkzeug.security import check_password_hash
from ..entity.user_account import UserAccount, Role
from ..entity.user_repository import UserRepository
from ..extensions import user_repo


class PlatformManagerAuthenticationError(Exception):
    """Raised when PM login fails."""
    pass


@dataclass
class AuthResult:
    user: UserAccount


class PmLoginControl:
    def __init__(self, repo: UserRepository = user_repo) -> None:
        self._repo = repo

    def authenticate(self, username: str, password: str) -> UserAccount:
        """Verify username/password, make sure role is Platform Manager,
        and that the account is not suspended."""
        user: Optional[UserAccount] = self._repo.get_by_username(username)
        if not user:
            raise PlatformManagerAuthenticationError("Invalid username or password.")

        # 先检查状态
        # 只允许 Active（或你也可以写成 if user.status.lower() != "active"）
        if user.status.lower() != "active":
            raise PlatformManagerAuthenticationError("Your account is suspended.")

        # 角色必须为 Platform Manager
        if user.role != Role.PLATFORM_MANAGER:
            raise PlatformManagerAuthenticationError(
                "You are not registered as a Platform Manager."
            )

        # 验证口令
        if not check_password_hash(user.password_hash, password):
            raise PlatformManagerAuthenticationError("Invalid username or password.")

        return user

'''







'''from dataclasses import dataclass
from typing import Optional

from werkzeug.security import check_password_hash

from ..entity.user_account import UserAccount, Role
from ..entity.user_repository import UserRepository
from ..extensions import user_repo


class PlatformManagerAuthenticationError(Exception):
    """The exception thrown when PM login fails."""
    pass


@dataclass
class AuthResult:
    user: UserAccount


class PmLoginControl:
    def __init__(self, repo: UserRepository = user_repo) -> None:
        self._repo = repo

    def authenticate(self, username: str, password: str) -> UserAccount:
        """
        Verify the username and password, and ensure that the role is Platform Manager.
        A PlatformManagerAuthenticationError is thrown when login fails.
        """
        # Find accounts by username (you can also use find_by_username_or_email).
        user: Optional[UserAccount] = self._repo.get_by_username(username)

        if not user:
            raise PlatformManagerAuthenticationError("Invalid username or password.")

        # 只允许 Active
        if user.status.lower() != "active":
            raise PlatformManagerAuthenticationError("Your account is suspended.")

        # Check if the role is Platform Manager
        if user.role != Role.PLATFORM_MANAGER:
            raise PlatformManagerAuthenticationError(
                "You are not registered as a Platform Manager."
            )

        # Verify password
        if not check_password_hash(user.password_hash, password):
            raise PlatformManagerAuthenticationError("Invalid username or password.")

        return user
'''