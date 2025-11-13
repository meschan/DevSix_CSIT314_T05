from werkzeug.security import check_password_hash
from ..entity.user_repository import UserRepository
from ..entity.user_account import Role, UserAccount


class PinAuthenticationError(Exception):
    pass

class PinLoginControl:
    """
    Responsible for verifying PIN username/password
    """
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate(self, username: str, password: str) -> UserAccount:
        # 1. find user by username
        user = self.repo.get_by_username(username)
        if not user:
            raise PinAuthenticationError("Username does not exist.")

        # 2. block suspended accounts
        if getattr(user, "status", "Active") == "Suspended":
            raise PinAuthenticationError( "This account has been suspended.")

        # 3. ensure role is PIN
        if user.role != Role.PIN:
            raise PinAuthenticationError("This account is not a PIN user.")

        # 4. Verify password
        if not check_password_hash(user.password_hash, password):
            raise PinAuthenticationError("Incorrect password.")

        # 5. Return user entity
        return user
