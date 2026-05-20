"""
PashuRakshak Backend - Application Factory
Smart Livestock Verification & Government Grant Monitoring System
"""
from flask import Flask
from flask_cors import CORS
from .config import config_by_name
from .extensions import init_extensions


def create_app(config_name="development"):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    init_extensions(app)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    _register_blueprints(app)

    # Initialize database with seed data
    with app.app_context():
        from .seed import init_seed_data
        init_seed_data()

    return app


def _register_blueprints(app):
    """Register all route blueprints."""
    from .routes.auth import auth_bp
    from .routes.farmers import farmers_bp
    from .routes.schemes import schemes_bp
    from .routes.applications import applications_bp
    from .routes.verification import verification_bp
    from .routes.rfid import rfid_bp
    from .routes.raids import raids_bp
    from .routes.scanning import scanning_bp
    from .routes.files import files_bp
    from .routes.reports import reports_bp
    from .routes.notifications import notifications_bp
    from .routes.analytics import analytics_bp
    from .routes.audit import audit_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(farmers_bp, url_prefix='/api/farmers')
    app.register_blueprint(schemes_bp, url_prefix='/api/schemes')
    app.register_blueprint(applications_bp, url_prefix='/api/applications')
    app.register_blueprint(verification_bp, url_prefix='/api/verification')
    app.register_blueprint(rfid_bp, url_prefix='/api/rfid')
    app.register_blueprint(raids_bp, url_prefix='/api/raids')
    app.register_blueprint(scanning_bp, url_prefix='/api/scanning')
    app.register_blueprint(files_bp, url_prefix='/api/files')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(audit_bp, url_prefix='/api/audit')
