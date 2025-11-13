from werkzeug.security import check_password_hash
from ..entity.user_repository import UserRepository
from ..entity.user_account import Role

class AuthenticationError(Exception):
    """Raised when username or password is incorrect."""
    pass


class UserAdminLoginControl:
    """
    Control layer for Admin Login use case.
    Handles verifying username/password from repository.
    """

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate(self, username: str, password: str):
        # 1. Find users by username or email
        user = self.repo.find_by_username_or_email(username, username)
        if not user:
            raise AuthenticationError("Username does not exist.")

        # 2. block suspended accounts
        if getattr(user, "status", "Active") == "Suspended":
            raise AuthenticationError("This account has been suspended.")

        # 3. Check if the password matches
        if not check_password_hash(user.password_hash, password):
            raise AuthenticationError("Incorrect password.")

        # 4. Check the role
        if user.role != Role.USER_ADMIN:
            raise AuthenticationError("This account is not a User Admin.")

        return user
