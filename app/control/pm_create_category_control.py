# app/control/pm_create_category_control.py
from dataclasses import dataclass
from typing import List
from ..extensions import category_repo
from ..entity.category import ServiceCategory

@dataclass
class CreateCategoryResult:
    ok: bool
    message: str

class PMCreateCategoryControl:
    def list_categories(self) -> List[ServiceCategory]:
        """用于页面侧显示/调试，也可不展示。"""
        return category_repo.get_all()

    def create(self, name: str) -> CreateCategoryResult:
        name = (name or "").strip()
        if not name:
            return CreateCategoryResult(False, "Category name cannot be empty.")
        try:
            category_repo.add(name)  # 内置了重名/空名校验
        except ValueError as e:
            return CreateCategoryResult(False, str(e))
        return CreateCategoryResult(True, f"Category '{name}' has been created.")
