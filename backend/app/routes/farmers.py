"""
Farmer management routes – CRUD, listing, search.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId

from app.extensions import db
from app.utils.helpers import serialize_doc, serialize_docs, paginate_query, now_utc, make_response_body, to_object_id
from app.utils.constants import ROLE_FARMER
from app.middleware.auth_guard import staff_required, any_authenticated

farmers_bp = Blueprint("farmers", __name__, url_prefix="/api/farmers")


@farmers_bp.route("", methods=["GET"])
@staff_required
def list_farmers():
    """List all farmers with pagination and optional search."""
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    search = request.args.get("search", "").strip()
    state = request.args.get("state", "").strip()
    city = request.args.get("city", "").strip()

    query = {"role": ROLE_FARMER}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"mobile": {"$regex": search, "$options": "i"}},
            {"aadhaar": {"$regex": search, "$options": "i"}},
        ]
    if state:
        query["state"] = {"$regex": state, "$options": "i"}
    if city:
        query["city"] = {"$regex": city, "$options": "i"}

    result = paginate_query(db.users, query, page, per_page, sort_field="created_at")
    # Remove password from each farmer
    for item in result["items"]:
        item.pop("password", None)

    return jsonify(make_response_body(True, "Farmers fetched", result)[0]), 200


@farmers_bp.route("/<farmer_id>", methods=["GET"])
@any_authenticated
def get_farmer(farmer_id):
    """Get a single farmer by ID."""
    oid = to_object_id(farmer_id)
    if not oid:
        return jsonify(make_response_body(False, "Invalid farmer ID")[0]), 400

    farmer = db.users.find_one({"_id": oid, "role": ROLE_FARMER})
    if not farmer:
        return jsonify(make_response_body(False, "Farmer not found")[0]), 404

    data = serialize_doc(farmer)
    data.pop("password", None)
    return jsonify(make_response_body(True, "Farmer fetched", data)[0]), 200


@farmers_bp.route("/<farmer_id>", methods=["PUT"])
@staff_required
def update_farmer(farmer_id):
    """Update a farmer's details (staff only)."""
    oid = to_object_id(farmer_id)
    if not oid:
        return jsonify(make_response_body(False, "Invalid farmer ID")[0]), 400

    data = request.get_json(silent=True) or {}
    allowed = ["name", "city", "state", "district", "address", "cattle_count",
               "land_acres", "aadhaar", "bank_account", "ifsc", "is_active"]
    update_fields = {k: data[k] for k in allowed if k in data}
    if "cattle_count" in update_fields:
        update_fields["cattle_count"] = int(update_fields["cattle_count"])
    if "land_acres" in update_fields:
        update_fields["land_acres"] = float(update_fields["land_acres"])
    update_fields["updated_at"] = now_utc()

    result = db.users.update_one({"_id": oid, "role": ROLE_FARMER}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify(make_response_body(False, "Farmer not found")[0]), 404

    farmer = db.users.find_one({"_id": oid})
    farmer_data = serialize_doc(farmer)
    farmer_data.pop("password", None)
    return jsonify(make_response_body(True, "Farmer updated", farmer_data)[0]), 200


@farmers_bp.route("/<farmer_id>", methods=["DELETE"])
@staff_required
def delete_farmer(farmer_id):
    """Soft-delete a farmer (deactivate)."""
    oid = to_object_id(farmer_id)
    if not oid:
        return jsonify(make_response_body(False, "Invalid farmer ID")[0]), 400

    result = db.users.update_one(
        {"_id": oid, "role": ROLE_FARMER},
        {"$set": {"is_active": False, "updated_at": now_utc()}},
    )
    if result.matched_count == 0:
        return jsonify(make_response_body(False, "Farmer not found")[0]), 404

    return jsonify(make_response_body(True, "Farmer deactivated")[0]), 200


@farmers_bp.route("/search", methods=["GET"])
@staff_required
def search_farmers():
    """Search farmers by name, mobile or Aadhaar."""
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify(make_response_body(False, "Query parameter 'q' required")[0]), 400

    farmers = db.users.find({
        "role": ROLE_FARMER,
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"mobile": {"$regex": q, "$options": "i"}},
            {"aadhaar": {"$regex": q, "$options": "i"}},
        ],
    }).limit(20)

    results = serialize_docs(farmers)
    for r in results:
        r.pop("password", None)

    return jsonify(make_response_body(True, "Search results", results)[0]), 200


@farmers_bp.route("/stats", methods=["GET"])
@staff_required
def farmer_stats():
    """Get aggregated farmer statistics."""
    total = db.users.count_documents({"role": ROLE_FARMER})
    active = db.users.count_documents({"role": ROLE_FARMER, "is_active": True})

    pipeline = [
        {"$match": {"role": ROLE_FARMER, "is_active": True}},
        {"$group": {
            "_id": None,
            "total_cattle": {"$sum": "$cattle_count"},
            "total_land": {"$sum": "$land_acres"},
            "avg_cattle": {"$avg": "$cattle_count"},
        }},
    ]
    agg = list(db.users.aggregate(pipeline))
    stats = agg[0] if agg else {"total_cattle": 0, "total_land": 0, "avg_cattle": 0}
    stats.pop("_id", None)
    stats["total_farmers"] = total
    stats["active_farmers"] = active

    return jsonify(make_response_body(True, "Farmer stats", stats)[0]), 200
