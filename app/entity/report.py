# app/entity/report.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Any, Optional

@dataclass
class Report:
    id: Optional[int]              # 由仓库赋值
    title: str                     # e.g. "Daily Matched Report (Last 24 hours)"
    period: str                    # "daily" | "weekly" | "monthly"
    created_at: datetime           # 生成时间（UTC 或本地，和你生成时保持一致）
    items: List[Any] = field(default_factory=list)  # 报表里展示的数据（可自定义结构）
