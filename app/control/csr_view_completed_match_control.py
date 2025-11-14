# control/csr_view_completed_match_control.py
from typing import Any, Dict, List
from ..extensions import request_repo  # 你的单例仓库名按实际调整

def _get(obj: Any, *names: str, default=""):
    """同时兼容 dict / 对象属性 / dataclass 的取值。"""
    for n in names:
        if hasattr(obj, n):
            v = getattr(obj, n, None)
            if v not in (None, ""):
                return v
        try:
            v = obj[n]  # type: ignore[index]
            if v not in (None, ""):
                return v
        except Exception:
            pass
    return default

class CSRViewCompletedMatchControl:
    def __init__(self) -> None:
        self._request_repo = request_repo

    def _is_matched(self, r: Any) -> bool:
        # 兼容 matched_to / matched_to_username 两种字段命名
        return bool(_get(r, "matched_to", "matched_to_username", default=""))

    def _pack_row(self, r: Any) -> Dict[str, Any]:
        return {
            "id":              _get(r, "id"),
            "title":           _get(r, "title"),
            "category_name":   _get(r, "category", "category_name"),
            "owner_username":  _get(r, "pin_username", "owner_username"),
            "matched_to":      _get(r, "matched_to", "matched_to_username"),
            "created_at":      _get(r, "created_at"),
        }

    def list_all(self) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for r in self._request_repo.list_all():
            if self._is_matched(r):
                rows.append(self._pack_row(r))
        # 可选：按创建时间/ID排序；没有 created_at 就按 id
        rows.sort(key=lambda x: (str(x.get("created_at", "")), x.get("id", 0)))
        return rows


