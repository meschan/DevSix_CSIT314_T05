from dataclasses import dataclass
from typing import List, Optional
from ..extensions import category_repo
from ..entity.category import ServiceCategory

@dataclass
class UpdateResult:
    ok: bool
    message: str

class PMUpdateCategoryControl:
    def list_categories(self) -> List[ServiceCategory]:
        # 统一列表展示（按名称排序）
        cats = category_repo.get_all()
        return sorted(cats, key=lambda c: (c.name or "").lower())

    def get_category(self, cat_id: int) -> Optional[ServiceCategory]:
        # 进入编辑页用
        return category_repo.get_by_id(cat_id)

    def rename(self, cat_id: int, new_name: str) -> UpdateResult:
        new_name = (new_name or "").strip()
        if not new_name:
            return UpdateResult(False, "Category name cannot be empty.")
        try:
            category_repo.rename(cat_id, new_name)  # 需在你的仓库里实现/已有该方法
        except ValueError as e:
            return UpdateResult(False, str(e))
        return UpdateResult(True, f"Category has been renamed to '{new_name}'.")
