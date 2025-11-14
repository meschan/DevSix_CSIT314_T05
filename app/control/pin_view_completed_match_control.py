# control/pin_view_completed_match_control.py
from typing import Any, Dict, List, Tuple
from flask import session

class PinViewCompletedMatchControl:
    """
    只读聚合：把与当前 PIN 相关的 completed-match 分两组返回：
      - matched_to_me: 别人的 request 被分配给了我
      - my_matched: 我创建的 request 被分配给了其他 PIN
    说明：
      1) 不改变任何已有仓库/方法名；仅用“宽松取字段”的方式读取。
      2) 与 search 版的思路一致，只是移除了筛选表单。
    """

    def __init__(self, request_repo, user_repo):
        # 复用你现有的 repo 实例；名字不变
        self._request_repo = request_repo
        self._user_repo = user_repo

    # ----------------- 对外方法（给页面用） -----------------
    def list_all(self) -> Dict[str, List[Dict[str, Any]]]:
        current_name = session.get("pin_username", "")
        current_id = session.get("pin_user_id")

        # 安全拿到 name 映射（userid -> username），便于 owner_id 转名字
        id2name = self._id2name()

        matched_to_me: List[Dict[str, Any]] = []
        my_matched:   List[Dict[str, Any]] = []

        # 扫描系统内的所有 request（跨所有 PIN）
        for r in self._safe_list_all():
            # 只考虑已经完成匹配的 request（有 matched_to）
            matched_to = self._r_matched_to(r)
            if not matched_to:
                continue

            owner_name = self._r_owner_name(r) or id2name.get(self._r_owner_id(r), "")

            # 1) 别人的 request 分配给了我
            if matched_to == current_name and owner_name and owner_name != current_name:
                matched_to_me.append(self._pack_row(r, owner_name, matched_to))

            # 2) 我发的 request 分配给了别人
            if owner_name == current_name and matched_to and matched_to != current_name:
                my_matched.append(self._pack_row(r, owner_name, matched_to))

        return {
            "matched_to_me": matched_to_me,
            "my_matched": my_matched,
        }

    # ----------------- 内部工具（宽松读取字段名） -----------------
    def _safe_list_all(self):
        """
        从 request_repo 安全取出“所有请求”：
          - list_all() -> list[Request或dict]
          - 若是 dict 存储（id -> Request），取 .values()
        """
        repo = self._request_repo
        if hasattr(repo, "list_all"):
            data = repo.list_all()
            # 有些 list_all 直接返回 dict.values() / list，本处统一转 list
            return list(data)
        if hasattr(repo, "values"):  # 兼容 {id: Request} 的内存存储
            return list(repo.values())
        return []

    def _get(self, obj, *names, default=""):
        """
        宽松取字段：
          - 如果 obj 是 dict：优先用 dict.get
          - 如果 obj 是对象：用 getattr
        只要取到的值不为 None / "" 就返回，否则继续尝试下一个候选名。
        """
        for n in names:
            if isinstance(obj, dict):
                v = obj.get(n, None)
            else:
                v = getattr(obj, n, None)
            if v not in (None, ""):
                return v
        return default

    def _r_id(self, r: Dict[str, Any]) -> Any:
        return self._get(r, "id", "request_id", default="")

    def _r_title(self, r: Dict[str, Any]) -> str:
        return str(self._get(r, "title", default=""))

    def _r_category(self, r: Dict[str, Any]) -> str:
        return str(self._get(r, "category", "category_name", default=""))

    def _r_owner_id(self, r: Dict[str, Any]) -> Any:
        # 你数据里通常是 pin_user_id；也兼容 owner_id
        return self._get(r, "pin_user_id", "owner_id", default=None)

    def _r_owner_name(self, r: Dict[str, Any]) -> str:
        # 有些场景你已经把 owner_username 放进 request 里了
        return str(self._get(r, "owner_username", "pin_username", default=""))

    def _r_matched_to(self, r: Dict[str, Any]) -> str:
        # 你之前在 CSR match 时常用 matched_to / matched_to_username
        return str(self._get(r, "matched_to", "matched_to_username", "assigned_to", default=""))

    def _r_created_at(self, r: Dict[str, Any]) -> str:
        return str(self._get(r, "created_at", "created", default=""))

    def _id2name(self) -> Dict[Any, str]:
        """
        根据 request 中出现过的 pin_user_id，到 user_repo 查 username，
        得到 {user_id -> username} 的宽松映射。
        """
        mapping: Dict[Any, str] = {}
        reqs = self._safe_list_all()

        # 从 request 里先捞 owner_id
        for r in reqs:
            uid = self._r_owner_id(r)
            if uid is None or uid in mapping:
                continue

            # 两种读取方式都兼容
            name = None
            if hasattr(self._user_repo, "get_username_by_id"):
                name = self._user_repo.get_username_by_id(uid)
            elif hasattr(self._user_repo, "get_by_id"):
                u = self._user_repo.get_by_id(uid)
                if u:
                    name = getattr(u, "username", None) or getattr(u, "name", None)

            if name:
                mapping[uid] = name

        return mapping

    def _pack_row(self, r: Dict[str, Any], owner_name: str, matched_to: str) -> Dict[str, Any]:
        return {
            "id":        self._r_id(r),
            "title":     self._r_title(r),
            "category":  self._r_category(r),
            "owner":     owner_name,
            "matched_to": matched_to,
            "status":    str(self._get(r, "status", default="Open")),
            "created":   self._r_created_at(r),
        }
