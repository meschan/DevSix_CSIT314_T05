"""Test helpers and environment configuration."""

from __future__ import annotations

import sys
import types
from pathlib import Path

# Ensure the project root is importable as ``app`` when running pytest from the repo root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _ensure_flask_stub() -> None:
    """Provide a very small Flask stub when the real package is unavailable."""

    try:  # pragma: no cover - exercise the real package when present.
        import flask  # type: ignore  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    stub = types.ModuleType("flask")

    class _DummyBlueprint:  # noqa: D401 - simple stub class.
        def __init__(self, *args, **kwargs) -> None:
            self.name = args[0] if args else "dummy"

        def route(self, *args, **kwargs):  # pragma: no cover - blueprint stub.
            def decorator(func):
                return func

            return decorator

    stub.Blueprint = _DummyBlueprint
    stub.request = types.SimpleNamespace()
    stub.session = {}
    stub.Flask = type("Flask", (), {})
    stub.render_template = lambda *args, **kwargs: None
    stub.redirect = lambda location: location
    stub.url_for = lambda endpoint, **values: f"/{endpoint}"

    def _flash(*args, **kwargs) -> None:  # pragma: no cover - placeholder.
        return None

    stub.flash = _flash

    sys.modules.setdefault("flask", stub)


_ensure_flask_stub()


def _ensure_werkzeug_stub() -> None:
    """Provide a tiny stub of :mod:`werkzeug.security` when unavailable."""

    try:  # pragma: no cover - prefer the real implementation when installed.
        from werkzeug.security import check_password_hash  # type: ignore  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    werkzeug_mod = types.ModuleType("werkzeug")
    security_mod = types.ModuleType("werkzeug.security")

    def generate_password_hash(password: str, *_args, **_kwargs) -> str:
        return f"stub-hash::{password}"

    def check_password_hash(hashed: str, password: str) -> bool:
        return hashed == generate_password_hash(password)

    security_mod.generate_password_hash = generate_password_hash
    security_mod.check_password_hash = check_password_hash

    werkzeug_mod.security = security_mod

    sys.modules.setdefault("werkzeug", werkzeug_mod)
    sys.modules.setdefault("werkzeug.security", security_mod)


_ensure_werkzeug_stub()

