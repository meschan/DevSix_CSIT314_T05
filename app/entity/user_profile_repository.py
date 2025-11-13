from typing import Dict, List, Optional
from .user_profile import UserProfile

class InMemoryUserProfileRepository:
    def __init__(self) -> None:
        self._items: Dict[int, UserProfile] = {}
        self._next_id: int = 1

    def add(self, name: str) -> UserProfile:
        """Add a new profile type, insert it directly without validation."""
        profile = UserProfile(
            id=self._next_id,
            name=name,
            status="Active",
        )
        self._items[self._next_id] = profile
        self._next_id += 1
        return profile

    def get_by_name(self, name: str) -> Optional[UserProfile]:
        name_lower = name.strip().lower()
        for p in self._items.values():
            if p.name.lower() == name_lower:
                return p
        return None

    def get_all(self) -> List[UserProfile]:
        return list(self._items.values())


