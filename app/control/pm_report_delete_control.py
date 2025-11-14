# app/control/pm_report_delete_control.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List
from ..entity.report_repository import InMemoryReportRepository
from ..entity.report import Report


@dataclass
class DeleteResult:
    ok: bool
    message: str

class PMReportDeleteControl:
    def __init__(self, report_repo: InMemoryReportRepository) -> None:
        self.report_repo = report_repo

    def list_reports(self) -> List[Report]:
        """
        返回所有已生成的日报/周报/月报。若还未生成过，则返回空列表。
        """
        return self.report_repo.list_all()

    def delete_report(self, report_id: int) -> DeleteResult:
        if report_id <= 0:
            return DeleteResult(False, "Invalid report id.")
        ok = self.report_repo.delete_by_id(report_id)
        if ok:
            return DeleteResult(True, "Report deleted successfully.")
        return DeleteResult(False, "Report not found or already deleted.")
