from werkzeug.security import check_password_hash
from dataclasses import dataclass
from typing import Optional
from ..entity.user_account import Role, UserAccount  # 仅类型提示
from ..entity.user_repository import UserRepository

class CsrAuthenticationError(Exception):
    pass

@dataclass
class CsrLoginControl:
    user_repo: UserRepository

    def authenticate(self, username: str, password: str) -> UserAccount:
        """
        仅允许 role == Role.CSR_REP 且 status == 'Active' 的用户登录。
        """
        user: Optional[UserAccount] = self.user_repo.get_by_username(username)
        if not user:
            raise CsrAuthenticationError("Invalid username or password.")

        # 角色检查
        if user.role != Role.CSR_REP:
            raise CsrAuthenticationError("This account is not a CSR Rep account.")

        # 状态检查（Suspended 不能登录）
        if getattr(user, "status", "Active").lower() != "active":
            raise CsrAuthenticationError("This account is suspended and cannot log in.")

        # 密码校验
        if not check_password_hash(user.password_hash, password):
            raise CsrAuthenticationError("Incorrect password.")

        return user
