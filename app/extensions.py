# Placeholder for future extensions, e.g. SQLAlchemy, Migrate, Bcrypt, etc.
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
from flask import request
from .entity.user_repository import InMemoryUserRepository
from .entity.user_profile_repository import InMemoryUserProfileRepository
'''from .entity.pin_repository import InMemoryPinRepository'''
from .entity.request_repository import InMemoryRequestRepository
from .entity.csr_shortlist_repository import InMemoryCsrShortlistRepository
from .entity.category import InMemoryCategoryRepository

# Globally unique repository instance
user_repo = InMemoryUserRepository()
user_profile_repo = InMemoryUserProfileRepository()
'''pin_repo = InMemoryPinRepository()'''
request_repo = InMemoryRequestRepository()
category_repo = InMemoryCategoryRepository()
csr_shortlist_repo = InMemoryCsrShortlistRepository()


