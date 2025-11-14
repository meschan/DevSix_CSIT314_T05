from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RequestRow:
    id: Optional[int]
    title: str
    category: str
    owner_username: str
    status: str
    description: str
    created_at: str
    views: int  # 新增：给页面展示

class CSRViewVolunteerRequestControl:
    def __init__(self, request_repo, user_repo) -> None:
        self._req_repo = request_repo
        self._user_repo = user_repo

    def list_all_rows(self) -> List[RequestRow]:
        """将所有 Request 汇总为可渲染的行，并把 pin_user_id → username。"""
        users = self._user_repo.list_all()
        id_to_username = {u.id: getattr(u, "username", "") for u in users}

        items = self._req_repo.list_all()  # 继续用你已有的接口

        rows: List[RequestRow] = []
        for r in items:
            category = getattr(r, "category", "") or getattr(r, "category_name", "")
            owner = id_to_username.get(getattr(r, "pin_user_id", None), "")
            rows.append(
                RequestRow(
                    id=getattr(r, "id", None),
                    title=getattr(r, "title", ""),
                    category=category,
                    owner_username=owner,
                    status=getattr(r, "status", "Open"),
                    description=getattr(r, "description", ""),
                    created_at=str(getattr(r, "created_at", "")),
                    views=int(getattr(r, "views", 0)),  # 默认 0
                )
            )
        rows.sort(key=lambda x: (x.id is None, x.id))
        return rows

    # 新增：不改旧方法名，只补一个“计数+1”的小方法供 boundary 调用
    def add_view(self, request_id: int) -> bool:
        """
        找到 id==request_id 的 request，把其 views +1 后更新。
        不强依赖特定仓库方法：若没有 get_by_id，就从 list_all 遍历；最后调用 update(r)。
        """
        target = None
        # 若你的仓库有 get_by_id 可优先用：
        get_by_id = getattr(self._req_repo, "get_by_id", None)
        if callable(get_by_id):
            target = get_by_id(request_id)
        if target is None:
            for r in self._req_repo.list_all():
                if getattr(r, "id", None) == request_id:
                    target = r
                    break
        if target is None:
            return False

        current = int(getattr(target, "views", 0))
        setattr(target, "views", current + 1)

        # 若仓库有 update 方法，调用之；没有就当内存对象已变更（in-memory 也会生效）
        upd = getattr(self._req_repo, "update", None)
        if callable(upd):
            upd(target)
        return True









# NO VIEW FUNCTION so PIN cannot view requests views

'''from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RequestRow:
    id: Optional[int]
    title: str
    category: str
    owner_username: str
    status: str
    description: str
    created_at: str

class CSRViewVolunteerRequestControl:
    def __init__(self, request_repo, user_repo) -> None:
        self._req_repo = request_repo
        self._user_repo = user_repo

    def list_all_rows(self) -> List[RequestRow]:
        """将所有 Request 汇总为可渲染的行，并把 pin_user_id → username。"""
        # 1) 取出用户，建立 id->username 索引
        users = self._user_repo.list_all()
        id_to_username = {u.id: getattr(u, "username", "") for u in users}

        # 2) 取出所有 request（不改你的仓库/实体方法名）
        items = self._req_repo.list_all()

        rows: List[RequestRow] = []
        for r in items:
            # 兼容不同字段名
            category = getattr(r, "category", "") or getattr(r, "category_name", "")
            owner = id_to_username.get(getattr(r, "pin_user_id", None), "")
            rows.append(
                RequestRow(
                    id=getattr(r, "id", None),
                    title=getattr(r, "title", ""),
                    category=category,
                    owner_username=owner,
                    status=getattr(r, "status", "Open"),
                    description=getattr(r, "description", ""),
                    created_at=str(getattr(r, "created_at", "")),
                )
            )
        # 你也可以按时间/ID排序；这里按 id 升序
        rows.sort(key=lambda x: (x.id is None, x.id))
        return rows
'''