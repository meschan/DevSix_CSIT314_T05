'''from dataclasses import dataclass
from werkzeug.security import generate_password_hash

@dataclass
class PinUser:
    id: int
    username: str
    password_hash: str
    full_name: str
    phone: str
    address: str


class InMemoryPinRepository:
    """
    A database is simulated using an in-memory dictionary;
     3-4 fixed accounts are created when the project starts.
    """
    def __init__(self):
        self._users = {}
        self._seed_data()

    def _seed_data(self):
        # To test
        users = [
            PinUser(
                id=1,
                username="lily001",
                password_hash=generate_password_hash("Pin@123"),
                full_name="Lily Tan",
                phone="65 8123-0001",
                address="Blk 10 ABC Street #01-01",
            ),
            PinUser(
                id=2,
                username="tom002",
                password_hash=generate_password_hash("Pin@123"),
                full_name="Tom Lee",
                phone="65 8123-0002",
                address="Blk 20 DEF Street #02-02",
            ),
            PinUser(
                id=3,
                username="yong003",
                password_hash=generate_password_hash("Pin@123"),
                full_name="Yong Chen",
                phone="65 8123-0003",
                address="Blk 30 GHI Street #03-03",
            ),
            PinUser(
                id=4,
                username="may004",
                password_hash=generate_password_hash("Pin@123"),
                full_name="May Lim",
                phone="65 8123-0004",
                address="Blk 40 JKL Street #04-04",
            ),
        ]

        for user in users:
            self._users[user.username.lower()] = user

    # ====== Externally provided query interface ======
    def find_by_username(self, username: str) -> PinUser | None:
        if not username:
            return None
        return self._users.get(username.lower())
'''