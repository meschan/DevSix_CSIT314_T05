from typing import List
from ..extensions import category_repo
from ..entity.category import ServiceCategory

class PMViewCategoriesControl:
    def list_categories(self) -> List[ServiceCategory]:
        """
        返回全部分类（默认 + 新创建）。你也可以在这里排序。
        """
        cats = category_repo.get_all()
        # 按名称排序（忽略大小写）；如果你想按创建时间排，改这里即可
        return sorted(cats, key=lambda c: (c.name or "").lower())
