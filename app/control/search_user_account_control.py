# app/control/search_user_account_control.py
from dataclasses import dataclass
from typing import List
from ..entity.user_repository import UserRepository
from ..extensions import user_repo


@dataclass
class SearchResult:
    keyword: str
    users: List


class SearchUserAccountControl:
    def __init__(self, repo: UserRepository = user_repo) -> None:
        self._repo = repo

    # 允许“role 或 username 或 email 或 phone_number”任一字段匹配
    def search(self, keyword: str) -> SearchResult:
        kw = (keyword or "").strip().lower()
        all_users = self._repo.list_all()

        if not kw:
            return SearchResult(keyword="", users=[])

        role_aliases = {
            "admin": "user admin",
            "user admin": "user admin",
            "pin": "pin",
            "csr": "csr rep",
            "csr rep": "csr rep",
            "manager": "platform manager",
            "platform manager": "platform manager",
        }

        # 如果看起来像 role，先把别名归一化
        normalized_role = role_aliases.get(kw)

        def _match(u) -> bool:
            # 角色匹配（不改实体，直接读 u.role.value）
            if normalized_role is not None:
                return u.role.value.lower() == normalized_role
            # 其他字段模糊匹配
            return (
                kw in (u.username or "").lower()
                or kw in (u.email or "").lower()
                or kw in (u.phone_number or "").lower()
                or kw in (u.role.value or "").lower()
            )

        matched = [u for u in all_users if _match(u)]
        return SearchResult(keyword=keyword, users=matched)
