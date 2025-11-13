# app/control/csr_search_request_control.py
from types import SimpleNamespace
from flask import render_template
from ..extensions import request_repo, user_repo          # 你们全局注册的仓库实例（方案B）

class CSRSearchRequestControl:
    """CSR 侧：查看所有 PIN 创建的请求"""
    def __init__(self, req_repo=request_repo, usr_repo=user_repo):
        self._repo = req_repo
        self._user_repo = usr_repo

    def list_all_requests(self):
        # 兼容不同仓库命名
        if hasattr(self._repo, "list_all"):
            items = self._repo.list_all()
        elif hasattr(self._repo, "get_all"):
            items = self._repo.get_all()
        else:
            items = []

            def pick(obj, *names, default=""):
                """从 obj（支持 dict / 对象）里依次取字段名；取不到返回 default。"""
                if isinstance(obj, dict):
                    for n in names:
                        if n in obj and obj[n] is not None:
                            return obj[n]
                    return default
                for n in names:
                    if hasattr(obj, n):
                        val = getattr(obj, n)
                        if val is not None:
                            return val
                return default

            rows = []
            for r in items:
                # 1) title：如果 r 就是字符串，直接用；否则从字段里取
                if isinstance(r, str):
                    title = r
                    rid = ""
                    category = ""
                    desc = ""
                    created_at = ""
                    owner = ""
                else:
                    title = pick(r, "title", "name", default="")
                    rid = pick(r, "id", "request_id", default="")
                    category = pick(r, "category", "category_name", default="")
                    desc = pick(r, "description", default="")
                    created_at = pick(r, "created_at", default="")
                    # owner：优先直接名字，其次用 id 查
                    owner = (pick(r, "owner_username", "pin_username", "username", default="")
                             or self._resolve_owner_by_id(pick(r, "owner_id", "user_id", default=None)))

                rows.append(SimpleNamespace(
                    id=rid,
                    title=title,
                    category=category,
                    display_owner=owner or "",
                    status=pick(r, "status", default="Open") if not isinstance(r, str) else "Open",
                    description=desc,
                    created_at=created_at,
                ))

            from flask import render_template
            return render_template("csr_search_request.html", requests=rows)

        def _resolve_owner_by_id(self, uid):
            if uid is None or not hasattr(self._user_repo, "get_by_id"):
                return ""
            u = self._user_repo.get_by_id(uid)
            if not u:
                return ""
            return getattr(u, "username", "") or getattr(u, "email", "")