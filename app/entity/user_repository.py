from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from .user_account import UserAccount

class UserRepository(ABC):
    """Repository interface. Only Entity layer talks to data storage."""
    @abstractmethod
    def find_by_username_or_email(self, username: str, email: str) -> Optional[UserAccount]:
        pass

    @abstractmethod
    def save(self, user: UserAccount) -> UserAccount:
        """Persists and returns the saved user (with id)."""
        pass

    @abstractmethod
    def list_all(self) -> List[UserAccount]:
        """Returns to all user accounts in the system"""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserAccount]:
        """
        This function allows you to precisely search for a user
        by username and update that user's profile.
        """
        pass

class InMemoryUserRepository(UserRepository):
    """
    Simple in-memory repository used for early development and testing.
    Replace with a SQLAlchemyUserRepository later without touching Control/Boundary.
    """
    def __init__(self):
        self._items: Dict[int, UserAccount] = {}
        self._auto_id = 1

    def find_by_username_or_email(self, username: str, email: str) -> Optional[UserAccount]:
        for u in self._items.values():
            if u.username == username or u.email.lower() == email.lower():
                return u
        return None

    def save(self, user: UserAccount) -> UserAccount:
        user.id = self._auto_id
        self._items[self._auto_id] = user
        self._auto_id += 1
        return user

    def list_all(self) -> List[UserAccount]:
        """Return all user accounts."""
        return list(self._items.values())

    def get_by_username(self, username: str) -> Optional[UserAccount]:
        """Search for users by username."""
        for u in self._items.values():
            if u.username == username:
                return u
        return None

    def update(self, user: UserAccount) -> None:
        # Assuming the key is user.id, it is stored in _items.
        self._items[user.id] = user
