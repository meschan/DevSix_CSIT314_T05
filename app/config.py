import os

class Config:
    # Secret key is required for session/flash messages and CSRF if added later
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    # Later you can put SQLALCHEMY_DATABASE_URI or other DB settings here