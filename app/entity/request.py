from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Request:
    id: int
    pin_user_id: int
    title: str
    category: str
    description: str
    status: str = "Open"
    created_at: datetime = field(default_factory=datetime.utcnow)
