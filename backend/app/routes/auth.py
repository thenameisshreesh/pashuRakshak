"""
Authentication routes – login / register / profile for farmers and officers.
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from bson import ObjectId

from app.extensions import db
from app.utils.helpers import serialize_doc, now_utc, make_response_body, get_client_ip
from app.utils.constants import (
    ROLE_FARMER,
    ROLE_OFFICER,
    ROLE_ADMIN,
    ALL_ROLES,
    AUDIT_LOGIN,
    AUDIT_REGISTER,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# ─── Farmer Registration ─────────────────────────────────────
@auth_bp.route("/register/farmer", methods=["POST"])
def register_farmer():
    """Register a new farmer with mobile + password."""
    data = request.get_json(silent=True) or {}
    required = ["name", "mobile", "password"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify(make_response_body(False, f"Missing fields: {', '.join(missing)}")[0]), 400

    mobile = data["mobile"].strip()
    if db.users.find_one({"mobile": mobile}):
        return jsonify(make_response_body(False, "Mobile number already registered")[0]), 409

    user_doc = {
        "name": data["name"].strip(),
        "mobile": mobile,
        "password": generate_password_hash(data["password"]),
        "role": ROLE_FARMER,
        "city": data.get("city", ""),
        "state": data.get("state", ""),
        "district": data.get("district", ""),
        "address": data.get("address", ""),
        "cattle_count": int(data.get("cattle_count", 0)),
        "land_acres": float(data.get("land_acres", 0)),
        "aadhaar": data.get("aadhaar", ""),
        "bank_account": data.get("bank_account", ""),
        "ifsc": data.get("ifsc", ""),
        "created_at": now_utc(),
        "updated_at": now_utc(),
        "is_active": True,
    }
    result = db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)

    # Audit log
    db.audit_logs.insert_one({
        "user_id": user_id,
        "action": AUDIT_REGISTER,
        "details": f"Farmer {data['name']} registered with mobile {mobile}",
        "ip_address": get_client_ip(request),
        "timestamp": now_utc(),
    })

    # Generate tokens
    additional_claims = {"role": ROLE_FARMER, "name": user_doc["name"]}
    access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user_id, additional_claims=additional_claims)

    return jsonify(make_response_body(True, "Farmer registered successfully", {
        "user_id": user_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    })[0]), 201


# ─── Officer Registration (Admin only in production, open for seeding) ───
@auth_bp.route("/register/officer", methods=["POST"])
def register_officer():
    """Register a new officer with username + password."""
    data = request.get_json(silent=True) or {}
    required = ["name", "username", "password"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify(make_response_body(False, f"Missing fields: {', '.join(missing)}")[0]), 400

    username = data["username"].strip().lower()
    if db.users.find_one({"username": username}):
        return jsonify(make_response_body(False, "Username already taken")[0]), 409

    role = data.get("role", ROLE_OFFICER)
    if role not in (ROLE_OFFICER, ROLE_ADMIN):
        role = ROLE_OFFICER

    user_doc = {
        "name": data["name"].strip(),
        "username": username,
        "password": generate_password_hash(data["password"]),
        "role": role,
        "department": data.get("department", "Animal Husbandry"),
        "designation": data.get("designation", "Field Officer"),
        "email": data.get("email", ""),
        "mobile": data.get("mobile", ""),
        "created_at": now_utc(),
        "updated_at": now_utc(),
        "is_active": True,
    }
    result = db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)

    # Audit log
    db.audit_logs.insert_one({
        "user_id": user_id,
        "action": AUDIT_REGISTER,
        "details": f"Officer {data['name']} registered as {role}",
        "ip_address": get_client_ip(request),
        "timestamp": now_utc(),
    })

    additional_claims = {"role": role, "name": user_doc["name"]}
    access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user_id, additional_claims=additional_claims)

    return jsonify(make_response_body(True, "Officer registered successfully", {
        "user_id": user_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    })[0]), 201


# ─── Login ────────────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    """Unified login – farmers use mobile, officers use username."""
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    user = None

    # Try mobile login (farmer)
    if data.get("mobile"):
        user = db.users.find_one({"mobile": data["mobile"].strip()})
    # Try username login (officer/admin)
    elif data.get("username"):
        user = db.users.find_one({"username": data["username"].strip().lower()})
    else:
        return jsonify(make_response_body(False, "Provide mobile or username")[0]), 400

    if not user or not check_password_hash(user["password"], password):
        return jsonify(make_response_body(False, "Invalid credentials")[0]), 401

    if not user.get("is_active", True):
        return jsonify(make_response_body(False, "Account is deactivated")[0]), 403

    user_id = str(user["_id"])
    additional_claims = {"role": user["role"], "name": user["name"]}
    access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user_id, additional_claims=additional_claims)

    # Audit log
    db.audit_logs.insert_one({
        "user_id": user_id,
        "action": AUDIT_LOGIN,
        "details": f"{user['role'].capitalize()} {user['name']} logged in",
        "ip_address": get_client_ip(request),
        "timestamp": now_utc(),
    })

    user_data = serialize_doc(user)
    user_data.pop("password", None)

    return jsonify(make_response_body(True, "Login successful", {
        "user": user_data,
        "access_token": access_token,
        "refresh_token": refresh_token,
    })[0]), 200


# ─── Token Refresh ────────────────────────────────────────────
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Issue a new access token using a valid refresh token."""
    identity = get_jwt_identity()
    claims = get_jwt()
    additional_claims = {"role": claims.get("role", ""), "name": claims.get("name", "")}
    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    return jsonify(make_response_body(True, "Token refreshed", {
        "access_token": access_token,
    })[0]), 200


# ─── Profile ─────────────────────────────────────────────────
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Return the authenticated user's profile."""
    user_id = get_jwt_identity()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify(make_response_body(False, "User not found")[0]), 404
    user_data = serialize_doc(user)
    user_data.pop("password", None)
    return jsonify(make_response_body(True, "Profile fetched", user_data)[0]), 200


@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update the authenticated user's profile."""
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    # Fields that can be updated
    allowed = ["name", "city", "state", "district", "address", "cattle_count",
               "land_acres", "aadhaar", "bank_account", "ifsc", "email",
               "department", "designation"]
    update_fields = {k: data[k] for k in allowed if k in data}
    if "cattle_count" in update_fields:
        update_fields["cattle_count"] = int(update_fields["cattle_count"])
    if "land_acres" in update_fields:
        update_fields["land_acres"] = float(update_fields["land_acres"])
    update_fields["updated_at"] = now_utc()

    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
    user = db.users.find_one({"_id": ObjectId(user_id)})
    user_data = serialize_doc(user)
    user_data.pop("password", None)
    return jsonify(make_response_body(True, "Profile updated", user_data)[0]), 200
