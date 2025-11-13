from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ServiceCategory:
    id: int
    name: str
    status: str = "Active"  # Active / Suspended

class InMemoryCategoryRepository:
    def __init__(self) -> None:
        self._items: List[ServiceCategory] = []
        self._next_id = 1
        # Default category (consistent with the PIN dropdown)
        for n in [
            "Grocery Assistance",
            "Medical Escort",
            "Home Cleaning",
            "Meal Delivery",
            "Transportation Support",
        ]:
            self.add(n)

    def _normalize(self, s: str) -> str:
        return " ".join(s.strip().split()).lower()

    def get_all(self) -> List[ServiceCategory]:
        return list(self._items)

    def exists(self, name: str) -> bool:
        key = self._normalize(name)
        return any(self._normalize(x.name) == key for x in self._items)

    def add(self, name: str) -> ServiceCategory:
        if not name or not name.strip():
            raise ValueError("Category name cannot be empty.")
        if self.exists(name):
            raise ValueError("Category already exists.")
        it = ServiceCategory(id=self._next_id, name=name.strip())
        self._next_id += 1
        self._items.append(it)
        return it

    def get_by_id(self, cid: int) -> Optional[ServiceCategory]:
        return next((x for x in self._items if x.id == cid), None)

    def update_name(self, cid: int, new_name: str) -> ServiceCategory:
        if not new_name or not new_name.strip():
            raise ValueError("Category name cannot be empty.")
        it = self.get_by_id(cid)
        if not it:
            raise ValueError("Category not found.")
        key = self._normalize(new_name)
        if any(self._normalize(x.name) == key and x.id != cid for x in self._items):
            raise ValueError("Category with the same name already exists.")
        it.name = new_name.strip()
        return it

    def suspend(self, cid: int) -> ServiceCategory:
        it = self.get_by_id(cid)
        if not it:
            raise ValueError("Category not found.")
        it.status = "Suspended"
        return it

    def find_by_name(self, name: str):
        """按名称（不区分大小写/两侧空白）查找已存在的分类。找不到返回 None。"""
        key = (name or "").strip().casefold()
        for c in self.get_all():
            if (c.name or "").strip().casefold() == key:
                return c
        return None

    def rename(self, cat_id: int, new_name: str) -> None:
        """
        将 ID=cat_id 的分类重命名为 new_name。
        校验：非空；目标存在；新名字不与其它分类重名（忽略大小写）。
        失败时抛 ValueError，成功时原地修改并返回 None。
        """
        new_name = (new_name or "").strip()
        if not new_name:
            raise ValueError("Category name cannot be empty.")

        cat = self.get_by_id(cat_id)  # 这里用你类里已有的 get_by_id
        if not cat:
            raise ValueError("Category not found.")

        # 与其它分类判重（忽略大小写）
        existed = self.find_by_name(new_name)
        if existed and existed.id != cat_id:
            raise ValueError(f"Category '{new_name}' already exists.")

        cat.name = new_name
        # 如果你是 dict 存储，原对象已更新；若需要持久化其他存储，这里顺带写回
