'''from typing import Any, Dict, List, Optional, Iterable

class CsrSearchCompletedMatchControl:
    """
    搜索所有已完成 match 的请求（全站视角）。
    依赖：request_repo（必须），可选：category_repo、user_repo（用于补充用户名）
    """

    def __init__(self, request_repo, category_repo=None, user_repo=None):
        self._request_repo = request_repo
        self._category_repo = category_repo
        self._user_repo = user_repo

    # ---------- 对外 API ----------

    # 收集所有category
    def _all_category_names(self) -> list[str]:
        names = set()

        # 1) 如果你有 category 仓库（例如 self._category_repo），优先从这里拿
        if hasattr(self, "_category_repo") and hasattr(self._category_repo, "list_all"):
            try:
                for c in (self._category_repo.list_all() or []):
                    name = self._get(c, "name", "category_name", "title")
                    if name:
                        names.add(str(name))
            except Exception:
                pass

        # 2) 兜底：从所有 request 里提取
        if hasattr(self, "_request_repo") and hasattr(self._request_repo, "list_all"):
            try:
                for r in (self._request_repo.list_all() or []):
                    name = self._get(r, "category", "category_name")
                    if name:
                        names.add(str(name))
            except Exception:
                pass

        # 3) 如果你把 “已完成匹配的请求” 是从其它仓库拿的，也可以再补充一遍：
        if hasattr(self, "_shortlist_repo") and hasattr(self._shortlist_repo, "list_all"):
            try:
                for r in (self._shortlist_repo.list_all() or []):
                    name = self._get(r, "category", "category_name")
                    if name:
                        names.add(str(name))
            except Exception:
                pass

        # 排序并在最前面加上 All
        all_names = sorted(n for n in names if n)
        return ["All"] + all_names

    def search_by_category(self, category: Optional[str]) -> List[Dict[str, Any]]:
        """按分类筛选所有 '已匹配' 的请求（全站）。"""
        category = (category or "").strip()
        rows: List[Dict[str, Any]] = []

        for r in self._safe_list_all():
            if not self._is_matched(r):
                continue
            if category and category != "All":
                if self._category(r) != category:
                    continue
            rows.append(self._pack_row(r))

        # 按创建时间或 id 轻度排序，便于阅读
        rows.sort(key=lambda x: (x.get("created") or "", x.get("id") or 0))
        return rows

    # ---------- 内部工具 ----------

    def _safe_list_all(self):
        try:
            data = self._request_repo.list_all()
            return list(data) if isinstance(data, (list, tuple)) else [data]
        except Exception:
            return []

    @staticmethod
    def _get(r, *names: str, default=None):
        # 既支持 dict，也支持对象（dataclass / 普通对象）
        for n in names:
            if isinstance(r, dict):
                if n in r and r[n] not in (None, ""):
                    return r[n]
            else:
                val = getattr(r, n, None)
                if val not in (None, ""):
                    return val
        return default

    def _id(self, r):            return self._get(r, "id", "req_id")
    def _title(self, r):         return str(self._get(r, "title", default=""))
    def _category(self, r):      return str(self._get(r, "category", "category_name", default=""))
    def _created(self, r):       return self._get(r, "created_at", "created", default="")

    def _owner_id(self, r):
        # 你的 request 里通常是 pin_user_id；也有可能叫 owner_id
        return self._get(r, "pin_user_id", "owner_id")

    def _owner_name(self, r) -> str:
        # 优先取 request 已带的用户名；否则尝试从 user_repo 反查
        name = self._get(r, "owner_username", "pin_username", default=None)
        if name:
            return str(name)
        if self._user_repo and hasattr(self._user_repo, "get_by_id"):
            uid = self._owner_id(r)
            try:
                u = self._user_repo.get_by_id(uid)
                n = self._get(u or {}, "username", default=None)
                if n:
                    return str(n)
            except Exception:
                pass
        return ""

    def _matched_to(self, r) -> str:
        # 可能字段：matched_to_username / matched_to / matched_username
        return str(self._get(r, "matched_to_username", "matched_to", "matched_username", default=""))

    def _is_matched(self, r) -> bool:
        """
        约定：存在 matched_to / matched_to_username / matched_flag / status == 'Matched' 即视为已匹配
        """
        if self._get(r, "matched_to_username", "matched_to", "matched_username", default=None):
            return True
        flag = self._get(r, "matched_flag", "is_matched", default=None)
        if isinstance(flag, bool) and flag:
            return True
        status = str(self._get(r, "status", default="")).lower()
        return status == "matched"

    def _pack_row(self, r: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": self._id(r),
            "title": self._title(r),
            "category": self._category(r),
            "owner": self._owner_name(r),
            "matched_to": self._matched_to(r),
            "created": self._created(r),
        }
'''

# app/control/csr_search_completed_match_control.py
'''from typing import Any, Dict, List, Optional, Iterable

class CsrSearchCompletedMatchControl:
    def __init__(self, request_repo, user_repo=None):
        self._request_repo = request_repo
        self._user_repo = user_repo

    # ---------- 提供给 boundary 的方法 ----------

    def _all_category_names(self) -> List[str]:
        names = set()
        for r in self._safe_list_all():
            if not self._matched_flag(r):
                continue
            cat = self._category(r)
            if cat:
                names.add(cat)
        return sorted(names)

    def search_by_category(self, category_name: Optional[str]) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for r in self._safe_list_all():
            if not self._matched_flag(r):
                continue
            if category_name and self._category(r) != category_name:
                continue
            rows.append(self._pack_row(r))
        return rows

    # ---------- 兼容型取字段 ----------

    @staticmethod
    def _get(r: Any, *names: str, default: Any = None) -> Any:
        for n in names:
            if isinstance(r, dict) and n in r:
                return r[n]
            if hasattr(r, n):
                try:
                    return getattr(r, n)
                except Exception:
                    pass
        return default

    def _safe_list_all(self) -> List[Any]:
        repo = self._request_repo
        if hasattr(repo, "list_all"):
            items = repo.list_all()
        elif hasattr(repo, "get_all"):
            items = repo.get_all()
        elif hasattr(repo, "values"):
            items = list(repo.values())
        else:
            items = []
        if isinstance(items, Iterable) and not isinstance(items, list):
            items = list(items)
        return items or []

    def _id(self, r: Any) -> Any:
        return self._get(r, "id", "request_id")

    def _title(self, r: Any) -> str:
        return str(self._get(r, "title", default="") or "")

    def _category(self, r: Any) -> str:
        return str(self._get(r, "category", "category_name", default="") or "")

    def _owner_id(self, r: Any) -> Any:
        return self._get(r, "pin_user_id", "owner_id", default=None)

    def _owner_name(self, r: Any) -> str:
        # 先看请求里是否带用户名
        name = self._get(r, "owner_username", "pin_username", default=None)
        if name:
            return str(name)
        # 再通过 user_repo 反查
        uid = self._owner_id(r)
        if uid and self._user_repo:
            if hasattr(self._user_repo, "get_username_by_id"):
                u = self._user_repo.get_username_by_id(uid)
                if u:
                    return str(u)
            if hasattr(self._user_repo, "get_by_id"):
                u = self._user_repo.get_by_id(uid)
                if u:
                    return str(self._get(u, "username", default=""))
        return ""

    def _matched_to(self, r: Any) -> str:
        name = self._get(
            r,
            "matched_to_username",
            "matched_to",
            "matched_username",
            "matched_pin_username",
            default="",
        )
        return str(name or "")

    def _created(self, r: Any) -> str:
        return str(self._get(r, "created_at", "created", default="") or "")

    def _matched_flag(self, r: Any) -> bool:
        if self._matched_to(r):
            return True
        status = str(self._get(r, "status", default="") or "")
        return status.lower() in {"matched", "completed"}

    def _pack_row(self, r: Any) -> Dict[str, Any]:
        return {
            "id": self._id(r),
            "title": self._title(r),
            "category": self._category(r),
            "owner": self._owner_name(r),
            "matched_to": self._matched_to(r),
            "created_at": self._created(r),
        }
'''


# control/csr_search_completed_match_control.py
# 说明：控制器从“分类仓库”拿全部分类，从“请求仓库”拿已匹配请求

from typing import Any, Dict, List
from ..extensions import request_repo, category_repo  # 用你项目里已暴露的单例


def _safe_get(obj: Any, *names: str, default: Any = "") -> Any:
    """同时兼容 dict / dataclass / 对象属性的取值方式。"""
    for n in names:
        # 对象属性
        if hasattr(obj, n):
            v = getattr(obj, n, None)
            if v not in (None, ""):
                return v
        # 映射类型
        try:
            v = obj[n]  # type: ignore[index]
            if v not in (None, ""):
                return v
        except Exception:
            pass
    return default

class CSRSearchCompletedMatchControl:
    def __init__(self) -> None:
        self._request_repo = request_repo
        self._category_repo = category_repo

    # ---- 分类：从“分类仓库”拿权威列表（包含 PM 新增） ----
    def all_category_names(self) -> List[str]:
        # category_repo.get_all() 返回包含 name 的对象列表
        # 这里确保顺序稳定并在模板里额外渲染 "All"
        return [c.name for c in self._category_repo.get_all()]

    # ---- 行打包 & 过滤逻辑 ----
    def _is_matched(self, r: Any) -> bool:
        # 兼容多种字段命名：matched_to / matched_to_username
        return bool(_safe_get(r, "matched_to", "matched_to_username", default=""))

    def _pack_row(self, r: Any) -> Dict[str, Any]:
        return {
            "id":            _safe_get(r, "id"),
            "title":         _safe_get(r, "title"),
            "category_name": _safe_get(r, "category", "category_name"),
            "owner_username": _safe_get(r, "pin_username", "owner_username"),
            "matched_to":    _safe_get(r, "matched_to", "matched_to_username"),
            "created_at":    _safe_get(r, "created_at"),
        }

    def list_all_matched(self) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for r in self._request_repo.list_all():   # 你的仓库已有 list_all
            if self._is_matched(r):
                rows.append(self._pack_row(r))
        return rows

    def search_by_category(self, category_name: str) -> List[Dict[str, Any]]:
        rows = self.list_all_matched()
        cat = (category_name or "").strip()
        if cat and cat != "All":
            rows = [r for r in rows if (r.get("category_name") or "") == cat]
        return rows

