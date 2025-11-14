# app/entity/report_repository.py
from __future__ import annotations
from typing import Dict, List, Optional
from .report import Report

class InMemoryReportRepository:
    def __init__(self) -> None:
        self._items: Dict[int, Report] = {}
        self._seq: int = 1

    # 供“生成报表”使用
    def add(self, report: Report) -> Report:
        report.id = self._seq
        self._items[self._seq] = report
        self._seq += 1
        return report

    # 供“删除/列表”使用
    def list_all(self) -> List[Report]:
        # 按创建时间倒序更直观
        return sorted(self._items.values(), key=lambda r: r.created_at, reverse=True)

    def list_by_period(self, period: str) -> List[Report]:
        return [r for r in self._items.values() if r.period == period]

    def get_by_id(self, report_id: int) -> Optional[Report]:
        return self._items.get(report_id)

    def delete_by_id(self, report_id: int) -> bool:
        if report_id in self._items:
            del self._items[report_id]
            return True
        return False
