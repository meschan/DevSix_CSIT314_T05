# app/control/suspend_user_account_control.py
from dataclasses import dataclass
from typing import List, Optional

from ..entity.user_repository import UserRepository
from ..extensions import user_repo

@dataclass
class SuspendUAResult:
    ok: bool
    message: str

class SuspendUserAccountControl:
    def __init__(self, repo: UserRepository = user_repo) -> None:
        self.repo = repo

    def list_all_users(self) -> List:
        """用于下拉框/列表显示"""
        return self.repo.list_all()

    def suspend(self, username: str) -> SuspendUAResult:
        return self._set_status(username, target="Suspended")

    def activate(self, username: str) -> SuspendUAResult:
        return self._set_status(username, target="Active")

    def _set_status(self, username: str, target: str) -> SuspendUAResult:
        user = self.repo.get_by_username(username)
        if not user:
            return SuspendUAResult(False, f"User '{username}' does not exist.")

        if user.status == target:
            # 根据目标状态返回更自然的提示
            if target == "Suspended":
                return SuspendUAResult(False, f"User '{username}' is already suspended.")
            else:
                return SuspendUAResult(False, f"User '{username}' is already active.")

        user.status = target
        self.repo.update(user)

        if target == "Suspended":
            return SuspendUAResult(True, f"User '{username}' has been suspended.")
        else:
            return SuspendUAResult(True, f"User '{username}' has been reactivated (Active).")


    '''def suspend(self, username: str) -> SuspendUAResult:
        user = self.repo.get_by_username(username)
        if not user:
            return SuspendUAResult(False, f"User '{username}' does not exist.")
        if user.status == "Suspended":
            return SuspendUAResult(False, f"User '{username}' is already suspended.")
        user.status = "Suspended"
        self.repo.update(user)
        return SuspendUAResult(True, f"User '{username}' has been suspended.")'''
