"""
Role-based access control decorators for route protection.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from app.utils.constants import ROLE_ADMIN, ROLE_OFFICER, ROLE_FARMER, STAFF_ROLES


def role_required(*allowed_roles):
    """Decorator that restricts access to users with specific roles.

    Usage:
        @role_required(ROLE_ADMIN, ROLE_OFFICER)
        def admin_only_route():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role", "")
            if user_role not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": f"Access denied. Required role(s): {', '.join(allowed_roles)}",
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn):
    """Shortcut decorator: admin only."""
    @wraps(fn)
    @role_required(ROLE_ADMIN)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper


def staff_required(fn):
    """Shortcut decorator: admin or officer."""
    @wraps(fn)
    @role_required(ROLE_ADMIN, ROLE_OFFICER)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper


def farmer_required(fn):
    """Shortcut decorator: farmer only."""
    @wraps(fn)
    @role_required(ROLE_FARMER)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper


def any_authenticated(fn):
    """Shortcut decorator: any logged-in user."""
    @wraps(fn)
    @role_required(ROLE_ADMIN, ROLE_OFFICER, ROLE_FARMER)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper
