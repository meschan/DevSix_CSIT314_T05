# app/control/view_user_account_control.py
from typing import List
from ..entity.user_account import UserAccount
from ..entity.user_repository import UserRepository
from ..extensions import user_repo  # 复用同一个仓库实例

class ViewUserAccountControl:
    """只负责读取所有 UserAccount，不做写操作。"""
    def __init__(self, repo: UserRepository = user_repo) -> None:
        self.repo = repo

    def list_all(self) -> List[UserAccount]:
        return self.repo.list_all()
