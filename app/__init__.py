from flask import Flask
from .config import Config
from .entity.user_repository import InMemoryUserRepository

def create_app() -> Flask:
    """Flask application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)


    # Register blueprints (Boundary layer)

    from .boundary.landing import bp as landing_bp
    app.register_blueprint(landing_bp)

    # User Admin
    from .boundary.create_user_account import bp as create_user_bp
    app.register_blueprint(create_user_bp, url_prefix="/admin")

    from .boundary.user_admin_login import bp as admin_login_bp
    app.register_blueprint(admin_login_bp, url_prefix="/admin")

    from .boundary.user_admin_home import bp as user_admin_home_bp
    app.register_blueprint(user_admin_home_bp, url_prefix="/admin")

    from .boundary.view_user_account import bp as view_user_account_bp
    app.register_blueprint(view_user_account_bp, url_prefix="/admin")

    from .boundary.update_user_account import bp as update_user_account_bp
    app.register_blueprint(update_user_account_bp, url_prefix="/admin")

    from .boundary.suspend_user_account import bp as suspend_user_account_bp
    app.register_blueprint(suspend_user_account_bp, url_prefix="/admin")

    from .boundary.search_user_account import bp as search_user_account_bp
    app.register_blueprint(search_user_account_bp, url_prefix="/admin")

    from .boundary.create_user_profile import bp as create_user_profile_bp
    app.register_blueprint(create_user_profile_bp, url_prefix="/admin")

    from .boundary.view_user_profile import bp as view_user_profile_bp
    app.register_blueprint(view_user_profile_bp, url_prefix="/admin")

    from .boundary.update_user_profile import bp as update_user_profile_bp
    app.register_blueprint(update_user_profile_bp, url_prefix="/admin")

    from .boundary.search_user_profile import bp as search_user_profile_bp
    app.register_blueprint(search_user_profile_bp, url_prefix="/admin")

    from .boundary.suspend_user_profile import bp as suspend_user_profile_bp
    app.register_blueprint(suspend_user_profile_bp, url_prefix="/admin")

    # PIN
    from .boundary.pin_login import bp as pin_login_bp
    app.register_blueprint(pin_login_bp, url_prefix="/pin")

    from .boundary.pin_home import bp as pin_home_bp
    app.register_blueprint(pin_home_bp, url_prefix="/pin")

    from .boundary.pin_create_request import bp as pin_create_request_bp
    app.register_blueprint(pin_create_request_bp, url_prefix="/pin")

    from .boundary.pin_view_request import bp as pin_view_request_bp
    app.register_blueprint(pin_view_request_bp, url_prefix="/pin")

    from .boundary.pin_update_request import bp as pin_update_request_bp
    app.register_blueprint(pin_update_request_bp, url_prefix="/pin")

    from .boundary.pin_delete_request import bp as pin_delete_request_bp
    app.register_blueprint(pin_delete_request_bp, url_prefix="/pin")

    from .boundary.pin_search_request import bp as pin_search_request_bp
    app.register_blueprint(pin_search_request_bp, url_prefix="/pin")

    # PM
    from .boundary.pm_login import bp as pm_login_bp
    app.register_blueprint(pm_login_bp, url_prefix="/pm")

    from .boundary.pm_home import bp as pm_home_bp
    app.register_blueprint(pm_home_bp, url_prefix="/pm")

    from .boundary.pm_create_category import bp as pm_create_category_bp
    app.register_blueprint(pm_create_category_bp, url_prefix="/pm")

    from .boundary.pm_view_categories import bp as pm_view_categories_bp
    app.register_blueprint(pm_view_categories_bp, url_prefix="/pm")

    from .boundary.pm_update_category import bp as pm_update_category_bp
    app.register_blueprint(pm_update_category_bp, url_prefix="/pm")

    # CSR
    from .boundary.csr_login import bp as csr_login_bp
    app.register_blueprint(csr_login_bp, url_prefix="/csr")

    from .boundary.csr_home import bp as csr_home_bp
    app.register_blueprint(csr_home_bp, url_prefix="/csr")

    from .boundary.csr_search_request import bp as csr_search_request_bp
    app.register_blueprint(csr_search_request_bp, url_prefix="/csr")

    # Jinja globals / filters can be added here if needed
    return app
