import re
from typing import Dict
from ..entity.user_profile_repository import InMemoryUserProfileRepository

DEFAULT_PROFILES = ["User Admin", "PIN", "CSR Rep", "Platform Manager"]

class DuplicateProfileError(Exception):
    pass

class ValidationError(Exception):
    """Carry field-level error information"""
    def __init__(self, errors: Dict[str, str]):
        super().__init__("Validation failed")
        self.errors = errors

class CreateUserProfileControl:
    def __init__(self, repo: InMemoryUserProfileRepository) -> None:
        self.repo = repo
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        """Ensure that the four default profiles are present."""
        for name in DEFAULT_PROFILES:
            if self.repo.get_by_name(name) is None:
                self.repo.add(name)

    def _validate_name(self, name: str) -> None:
        errors: Dict[str, str] = {}
        if not name:
            errors["name"] = "Profile name is required."
        elif len(name) < 2 or len(name) > 40:
            errors["name"] = "Profile name must be 2–40 characters."
        elif not re.fullmatch(r"[A-Za-z ]+", name):
            errors["name"] = "Only letters and spaces are allowed."
        if errors:
            raise ValidationError(errors)

    def create(self, name: str):
        name = (name or "").strip()
        self._validate_name(name)

        if self.repo.get_by_name(name) is not None:
            raise DuplicateProfileError("This profile already exists.")
        return self.repo.add(name)
