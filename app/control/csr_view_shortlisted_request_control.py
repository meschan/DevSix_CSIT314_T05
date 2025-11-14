# app/control/csr_view_shortlisted_request_control.py
# app/control/csr_view_shortlisted_request_control.py
from typing import List, Optional
from datetime import datetime
from ..entity.request import Request
from ..extensions import request_repo, shortlist_repo, user_repo


class CSRViewShortlistedRequestControl:
    """
    只处理“查看/计数”和“匹配”两件事。保持已有方法名不变：
      - list_shortlisted(...)
      - view_one(...)
      - match_one(...)
    """

    # ====== 已有：列出当前 CSR 的 shortlist ======
    def list_shortlisted(self, csr_username: str) -> List[Request]:
        """
        返回当前 CSR 保存到 shortlist 的所有请求。
        兼容两种 shortlist_repo 实现（全局/按用户）。
        """
        # 兼容：如果有 per-user 接口，优先用；否则退化为全局 ids
        if hasattr(shortlist_repo, "list_ids_for"):
            ids = list(shortlist_repo.list_ids_for(csr_username))
        else:
            ids = list(shortlist_repo.list_all_ids())

        # 取出请求实体；仓库已提供 get_by_id/list_all/update 等接口
        # （见 InMemoryRequestRepository 中的 get_by_id/list_all/update）。:contentReference[oaicite:0]{index=0}
        out: List[Request] = []
        for rid in ids:
            req = request_repo.get_by_id(int(rid))
            if req is not None:
                out.append(req)

        id2name = {u.id: getattr(u, "username", "") for u in user_repo.list_all()}
        for r in out:
            owner_id = (
                    getattr(r, "owner_id", None)
                    or getattr(r, "pin_user_id", None)
            )
            owner_name = (
                    getattr(r, "owner_username", None)
                    or getattr(r, "pin_username", None)
                    or id2name.get(owner_id, "")
            )
            setattr(r, "owner_username", owner_name)
            setattr(r, "display_owner", owner_name)  # 模板若用 display_owner 也能显示

        # 排序一下更友好
        out.sort(key=lambda r: (getattr(r, "created_at", ""), getattr(r, "id", 0)))
        return out

    # ====== 新增：对单条 shortlist request 进行“view 计数 +1” ======
    def view_one(self, csr_username: str, request_id: int) -> Optional[int]:
        """
        若该请求在当前 CSR 的 shortlist 内，则将其 views 累加 1 并保存。
        返回最新 views；否则返回 None。
        """
        # 只允许查看自己 shortList 里的（兼容两种实现）
        in_my_shortlist = (
            shortlist_repo.is_saved_for(csr_username, request_id)
            if hasattr(shortlist_repo, "is_saved_for")
            else shortlist_repo.is_saved(request_id)  # :contentReference[oaicite:1]{index=1}
        )
        if not in_my_shortlist:
            return None

        req = request_repo.get_by_id(int(request_id))
        if req is None:
            return None

        # 安全累加
        current = getattr(req, "views", 0)
        setattr(req, "views", int(current) + 1)

        request_repo.update(req)  # 持久化到内存仓库（update 已提供）。:contentReference[oaicite:2]{index=2}
        return req.views

    # ====== 新增：匹配（将 request 分配给某个 PIN） ======
    def match_one(self, csr_username: str, request_id: int, target_pin_username: str) -> tuple[bool, str]:
        """
        规则：
          1) 目标 PIN 不能是创建该 request 的 PIN；
          2) 已匹配过（matched_to 有值）则不再匹配；
          3) 仅允许从 shortlist 中发起匹配。
        返回 (ok, message)。
        """
        # 仍只允许从自己的 shortlist 操作
        can_operate = (
            shortlist_repo.is_saved_for(csr_username, request_id)
            if hasattr(shortlist_repo, "is_saved_for")
            else shortlist_repo.is_saved(request_id)
        )
        if not can_operate:
            return False, "This request is not in your shortlist."

        req = request_repo.get_by_id(int(request_id))
        if req is None:
            return False, "Request does not exist."

        owner = getattr(req, "pin_username", None) or getattr(req, "owner_username", None)
        if not target_pin_username:
            return False, "Please choose a PIN user."
        if owner and target_pin_username == owner:
            return False, "Cannot match to the same PIN who created this request."

        if getattr(req, "matched_to", None):
            return False, f"Already matched to {req.matched_to}."

        # 设置匹配对象并保存
        setattr(req, "matched_to", target_pin_username)
        # ⭐ 关键：记录匹配完成时间（供 PM 日报使用）
        setattr(req, "matched_at", datetime.now())
        # 可选：如果你希望在列表里看到状态变化
        setattr(req, "status", "Matched")

        request_repo.update(req)
        return True, f"Matched to {target_pin_username}."

    # ====== 帮助函数：可选，供边界层取 PIN 候选列表 ======
    def candidates_pins(self, exclude_username: Optional[str] = None) -> list[str]:
        """
        返回所有 PIN 用户名列表，排除创建者。
        """
        pins = []
        for u in user_repo.list_all():
            role_str = str(getattr(u, "role", "")).lower()
            # 兼容 Enum 或字符串
            if "pin" in role_str:
                uname = getattr(u, "username", "")
                if exclude_username and uname == exclude_username:
                    continue
                pins.append(uname)
        pins.sort()
        return pins















#can run but no match

'''from dataclasses import dataclass
from typing import List, Optional
from flask import session

@dataclass
class ShortlistedRow:
    id: Optional[int]
    title: str
    category: str
    owner_username: str
    status: str
    description: str
    views: int
    created_at: str

class CSRViewShortlistedRequestControl:
    """
    - list_shortlisted(): 读取 shortlist 里的 request_id，组装成可渲染行
    - add_view(req_id): 对该 request 计数 +1
    """
    def __init__(self, request_repo, user_repo, shortlist_repo) -> None:
        self._req_repo = request_repo
        self._user_repo = user_repo
        self._shortlist = shortlist_repo

    def _get_request_by_id(self, request_id: int):
        # 优先用 get_by_id；没有就退化到遍历
        get_by_id = getattr(self._req_repo, "get_by_id", None)
        if callable(get_by_id):
            return get_by_id(request_id)
        for r in self._req_repo.list_all():
            if getattr(r, "id", None) == request_id:
                return r
        return None

    def list_shortlisted(self) -> List[ShortlistedRow]:
        # id -> username 字典
        users = self._user_repo.list_all()
        id_to_username = {u.id: getattr(u, "username", "") for u in users}

        rows: List[ShortlistedRow] = []
        for rid in self._shortlist.list_all_ids():
            r = self._get_request_by_id(int(rid))
            if not r:
                # 若某条被删了，悄悄忽略
                continue

            category = getattr(r, "category", "") or getattr(r, "category_name", "")
            owner = id_to_username.get(getattr(r, "pin_user_id", None), "")
            rows.append(ShortlistedRow(
                id=getattr(r, "id", None),
                title=getattr(r, "title", ""),
                category=category,
                owner_username=owner,
                status=getattr(r, "status", "Open"),
                description=getattr(r, "description", ""),
                views=int(getattr(r, "views", 0)),
                created_at=str(getattr(r, "created_at", "")),
            ))

        rows.sort(key=lambda x: (x.id is None, x.id))
        return rows

    def add_view(self, request_id: int) -> tuple[bool, str]:
        r = self._get_request_by_id(request_id)
        if not r:
            return False, "Request not found."

        # 优先调用仓库的 increment_views；没有就手动 +1 后 update
        incr = getattr(self._req_repo, "increment_views", None)
        if callable(incr):
            incr(request_id)
            return True, "View recorded."

        # 退化：直接修改实体并交给 update
        current = int(getattr(r, "views", 0))
        setattr(r, "views", current + 1)
        upd = getattr(self._req_repo, "update", None)
        if callable(upd):
            upd(r)
            return True, "View recorded."

        # 如果连 update 都没有，就算了（不报错以免影响流程）
        return True, "View recorded."

'''