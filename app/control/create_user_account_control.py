import re
from typing import Tuple, Optional
from werkzeug.security import generate_password_hash
from ..entity.user_account import UserAccount, Role
from ..entity.user_repository import UserRepository

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[0-9+\-\s()]{7,20}$")

class ValidationError(Exception):
    """Raised when input fields are invalid."""
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message)
        self.field = field or "form"

class ConflictError(Exception):
    """Raised when duplicate user info is found in repository."""
    pass

class CreateUserAccountControl:
    """
    Control layer: orchestrates the use case 'Create new user account'.
    Boundary (route) calls this service. Entity (repository) persists data.
    """
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user_account(
        self,
        username: str,
        email: str,
        phone_number: str,
        address: str,
        role: str,
        password: str
    ) -> UserAccount:
        # 1) Validate inputs
        self._validate(username, email, phone_number, address, role, password)

        # 2) Check duplicates
        if self.repo.find_by_username_or_email(username, email):
            raise ConflictError("User with same username or email already exists.")

        # 3) Hash password
        password_hash = generate_password_hash(password)

        # 4) Create entity and persist via repository
        entity = UserAccount(
            id=None,
            username=username.strip(),
            email=email.strip().lower(),
            phone_number=phone_number.strip(),
            address=address.strip(),
            role=self._parse_role(role),
            password_hash=password_hash,
        )
        saved = self.repo.save(entity)
        return saved

    # -------- helpers --------
    def _validate(self, username, email, phone, address, role, password) -> None:
        if not username or len(username.strip()) < 3:
            raise ValidationError("Username must be at least 3 characters.", "username")
        if not email or not EMAIL_RE.match(email):
            raise ValidationError("Email format is invalid.", "email")
        if not phone or not PHONE_RE.match(phone):
            raise ValidationError("Phone number format is invalid.", "phone_number")
        if not address or len(address.strip()) < 5:
            raise ValidationError("Address is too short.", "address")
        if role.lower() not in {r.value for r in Role}:
            raise ValidationError("Role is not recognized.", "role")
        if not password or len(password) < 8:
            raise ValidationError("Password must be at least 8 characters.", "password")

    def _parse_role(self, role_str: str) -> Role:
        try:
            return Role(role_str.lower())
        except ValueError:
            # Should be unreachable due to validation
            raise ValidationError("Unsupported role.", "role")