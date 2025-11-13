from __future__ import annotations

from app.control.create_request_control import CreateRequestControl
from app.control.csr_search_request_control import CSRSearchRequestControl
from app.control.csr_shortlist_control import CSRShortlistControl
from app.extensions import csr_shortlist_repo, request_repo


def _reset_repositories() -> None:
    request_repo._items.clear()  # type: ignore[attr-defined]
    request_repo._next_id = 1  # type: ignore[attr-defined]
    csr_shortlist_repo._shortlists.clear()  # type: ignore[attr-defined]


def test_csr_can_view_and_shortlist_requests():
    _reset_repositories()

    create_control = CreateRequestControl()
    created = create_control.create(
        pin_user_id=5,
        title="Community Clean-up",
        category="Grocery Assistance",
        description="Looking for volunteers to support seniors with grocery runs.",
    )

    search_control = CSRSearchRequestControl()
    results = search_control.list_all_requests()
    assert any(row.id == created.id for row in results)

    shortlist_control = CSRShortlistControl()
    status = shortlist_control.save_to_shortlist(csr_user_id=42, opportunity_id=created.id)
    assert status == "added"

    saved = shortlist_control.get_shortlist(42)
    assert len(saved) == 1
    assert saved[0].id == created.id
    assert saved[0].pin_user_id == created.pin_user_id
