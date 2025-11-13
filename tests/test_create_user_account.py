import pytest
from app.control.create_user_account_control import CreateUserAccountControl, ValidationError, ConflictError
from app.entity.user_repository import InMemoryUserRepository

def test_happy_path():
    c = CreateUserAccountControl(InMemoryUserRepository())
    u = c.create_user_account("alice", "a@ex.com", "+1234567", "Wonderland 1", "user", "supersecret")
    assert u.id == 1 and u.username == "alice"

def test_duplicate():
    c = CreateUserAccountControl(InMemoryUserRepository())
    c.create_user_account("bob", "b@ex.com", "1112222", "Street 1", "user", "supersecret")
    with pytest.raises(ConflictError):
        c.create_user_account("bob", "b@ex.com", "1112222", "Street 1", "user", "supersecret")

def test_validation():
    c = CreateUserAccountControl(InMemoryUserRepository())
    with pytest.raises(ValidationError):
        c.create_user_account("aa", "bad", "12", "x", "invalid", "1")
