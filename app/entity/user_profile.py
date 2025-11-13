from dataclasses import dataclass

@dataclass
class UserProfile:
    id: int
    name: str  # like 'User Admin'
    status: str = "Active"

