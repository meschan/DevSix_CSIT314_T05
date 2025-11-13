from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Role(str, Enum):
    USER_ADMIN = "user admin"
    PIN = "pin"
    CSR_REP = "csr rep"
    PLATFORM_MANAGER = "platform manager"

@dataclass
class UserAccount:
    """Domain entity for a user account. Password is stored as a hash."""
    id: Optional[int]          # Will be assigned by repository/DB
    username: str
    email: str
    phone_number: str
    address: str
    role: Role
    password_hash: str
    status: str = "Active"
