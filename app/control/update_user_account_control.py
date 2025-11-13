# app/control/update_user_account_control.py

from dataclasses import dataclass
from typing import Optional
from werkzeug.security import generate_password_hash
import re

from ..entity.user_repository import UserRepository
from ..extensions import user_repo

@dataclass
class UpdateUAResult:
    ok: bool
    message: str

class UpdateUserAccountControl:
    def __init__(self, repo: UserRepository = user_repo) -> None:
        self.repo = repo

    def find_by_username(self, username: str):
        if not username:
            return None
        return self.repo.get_by_username(username)

    def _email_is_valid(self, email: str) -> bool:
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

    def _get_by_email(self, email: str):
        if hasattr(self.repo, "get_by_email"):
            return getattr(self.repo, "get_by_email")(email)
        if hasattr(self.repo, "list_all"):
            for u in self.repo.list_all():
                if u.email.lower() == email.lower():
                    return u
        return None

    def update_fields(
        self,
        username: str,
        new_phone: Optional[str],
        new_address: Optional[str],
        new_password: Optional[str],
        new_email: Optional[str],
    ) -> UpdateUAResult:
        user = self.repo.get_by_username(username)
        if not user:
            return UpdateUAResult(False, f"User '{username}' not found.")

        changed = False  # ← 新增：是否有改动

        # ---- phone ----
        if new_phone is not None:
            new_phone = new_phone.strip()
            if len(new_phone) == 0:
                return UpdateUAResult(False, "Phone number cannot be empty.")
            if new_phone != user.phone_number:
                user.phone_number = new_phone
                changed = True

        # ---- address ----
        if new_address is not None:
            new_address = new_address.strip()
            if len(new_address) == 0:
                return UpdateUAResult(False, "Address cannot be empty.")
            if new_address != user.address:
                user.address = new_address
                changed = True

        # ---- email（可选）----
        if new_email is not None:
            new_email = new_email.strip()
            if len(new_email) == 0:
                return UpdateUAResult(False, "Email cannot be empty.")
            if not self._email_is_valid(new_email):
                return UpdateUAResult(False, "Invalid email format.")
            if new_email.lower() != user.email.lower():
                # 唯一性（允许与自己相同）
                exists = self._get_by_email(new_email)
                if exists and exists.username != user.username:
                    return UpdateUAResult(False, "This email is already in use by another account.")
                user.email = new_email
                changed = True

        # ---- password（可选）----
        if new_password:
            if len(new_password) < 8:
                return UpdateUAResult(False, "Password must be at least 8 characters.")
            user.password_hash = generate_password_hash(new_password)
            changed = True

        if not changed:
            # 不落库，返回“无改动”
            return UpdateUAResult(False, "No changes detected.")

        self.repo.update(user)
        return UpdateUAResult(True, f"User '{username}' has been updated successfully.")
