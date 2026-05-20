"""
Government scheme CRUD and listing routes.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId

from app.extensions import db
from app.utils.helpers import serialize_doc, serialize_docs, paginate_query, now_utc, make_response_body, to_object_id
from app.middleware.auth_guard import staff_required, any_authenticated

schemes_bp = Blueprint("schemes", __name__, url_prefix="/api/schemes")


@schemes_bp.route("", methods=["GET"])
@jwt_required()
def list_schemes():
    """List all government schemes with optional pagination."""
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    search = request.args.get("search", "").strip()

    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}

    active_only = request.args.get("active", "").lower()
    if active_only == "true":
        query["is_active"] = True

    result = paginate_query(db.schemes, query, page, per_page, sort_field="created_at")
    return jsonify(make_response_body(True, "Schemes fetched", result)[0]), 200


@schemes_bp.route("/<scheme_id>", methods=["GET"])
@jwt_required()
def get_scheme(scheme_id):
    """Get a single scheme by ID."""
    oid = to_object_id(scheme_id)
    if not oid:
        return jsonify(make_response_body(False, "Invalid scheme ID")[0]), 400

    scheme = db.schemes.find_one({"_id": oid})
    if not scheme:
        return jsonify(make_response_body(False, "Scheme not found")[0]), 404

    return jsonify(make_response_body(True, "Scheme fetched", serialize_doc(scheme))[0]), 200


@schemes_bp.route("", methods=["POST"])
@staff_required
def create_scheme():
    """Create a new government scheme (staff only)."""
    data = request.get_json(silent=True) or {}
    required = ["name", "min_cattle", "validations_required", "sponsor"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify(make_response_body(False, f"Missing fields: {', '.join(missing)}")[0]), 400

    scheme_doc = {
        "name": data["name"].strip(),
        "description": data.get("description", ""),
        "min_cattle": int(data["min_cattle"]),
        "validations_required": int(data["validations_required"]),
        "sponsor": data["sponsor"].strip(),
        "grant_amount": float(data.get("grant_amount", 0)),
        "eligibility_criteria": data.get("eligibility_criteria", ""),
        "required_documents": data.get("required_documents", []),
        "is_active": True,
        "created_at": now_utc(),
        "updated_at": now_utc(),
    }
    result = db.schemes.insert_one(scheme_doc)

    scheme_doc["_id"] = result.inserted_id
    return jsonify(make_response_body(True, "Scheme created", serialize_doc(scheme_doc))[0]), 201


@schemes_bp.route("/<scheme_id>", methods=["PUT"])
@staff_required
def update_scheme(scheme_id):
    """Update an existing scheme."""
    oid = to_object_id(scheme_id)
    if not oid:
        return jsonify(make_response_body(False, "Invalid scheme ID")[0]), 400

    data = request.get_json(silent=True) or {}
    allowed = ["name", "description", "min_cattle", "validations_required",
               "sponsor", "grant_amount", "eligibility_criteria",
               "required_documents", "is_active"]
    update_fields = {k: data[k] for k in allowed if k in data}
    if "min_cattle" in update_fields:
        update_fields["min_cattle"] = int(update_fields["min_cattle"])
    if "validations_required" in update_fields:
        update_fields["validations_required"] = int(update_fields["validations_required"])
    if "grant_amount" in update_fields:
        update_fields["grant_amount"] = float(update_fields["grant_amount"])
    update_fields["updated_at"] = now_utc()

    result = db.schemes.update_one({"_id": oid}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify(make_response_body(False, "Scheme not found")[0]), 404

    scheme = db.schemes.find_one({"_id": oid})
    return jsonify(make_response_body(True, "Scheme updated", serialize_doc(scheme))[0]), 200


@schemes_bp.route("/<scheme_id>", methods=["DELETE"])
@staff_required
def delete_scheme(scheme_id):
    """Soft-delete a scheme."""
    oid = to_object_id(scheme_id)
    if not oid:
        return jsonify(make_response_body(False, "Invalid scheme ID")[0]), 400

    result = db.schemes.update_one(
        {"_id": oid},
        {"$set": {"is_active": False, "updated_at": now_utc()}},
    )
    if result.matched_count == 0:
        return jsonify(make_response_body(False, "Scheme not found")[0]), 404

    return jsonify(make_response_body(True, "Scheme deactivated")[0]), 200
