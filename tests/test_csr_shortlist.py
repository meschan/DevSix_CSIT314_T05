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
    assert any(row.id == created.id for row in saved)

    saved_entry = next(row for row in saved if row.id == created.id)
    assert saved_entry.pin_user_id == created.pin_user_id
    assert saved_entry.is_saved is True


def test_csr_shortlist_marks_unsaved_requests():
    _reset_repositories()

    create_control = CreateRequestControl()
    first = create_control.create(
        pin_user_id=10,
        title="Library Assistance",
        category="Grocery Assistance",
        description="Need volunteers to assist with library cataloguing and checkouts.",
    )
    second = create_control.create(
        pin_user_id=11,
        title="Community Kitchen",
        category="Meal Delivery",
        description="Help prepare and deliver meals for the weekly soup kitchen night.",
    )

    shortlist_control = CSRShortlistControl()
    shortlist_control.save_to_shortlist(csr_user_id=7, opportunity_id=first.id)

    results = shortlist_control.get_shortlist(7)

    ids = {row.id for row in results}
    assert {first.id, second.id} <= ids

    first_row = next(row for row in results if row.id == first.id)
    second_row = next(row for row in results if row.id == second.id)
    assert first_row.is_saved is True
    assert second_row.is_saved is False
