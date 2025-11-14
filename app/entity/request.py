from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Request:
    id: int
    pin_user_id: int
    title: str
    category: str
    description: str
    status: str = "Open"
    created_at: datetime = field(default_factory=datetime.utcnow)

    matched_to_username: Optional[str] = None
    matched_at: Optional[datetime] = None
