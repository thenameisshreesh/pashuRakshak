"""
RFID tag management routes – allocation, boundary check, tag listing.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId

from app.extensions import db
from app.utils.helpers import serialize_doc, serialize_docs, now_utc, make_response_body, to_object_id, get_client_ip
from app.utils.constants import (
    TAG_STATUS_ACTIVE, TAG_STATUS_INACTIVE, TAG_STATUS_LOST,
    NOTIF_TAG_ALLOCATED, AUDIT_TAG_ALLOCATE,
)
from app.middleware.auth_guard import staff_required, any_authenticated
from app.services.validation_service import allocate_tags, check_boundary

rfid_bp = Blueprint("rfid", __name__, url_prefix="/api/rfid")


@rfid_bp.route("/allocate", methods=["POST"])
@staff_required
def allocate_rfid_tags():
    """Manually allocate RFID tags for a farmer.

    Body: { farmer_id, count, farmer_code? }
    """
    body = request.get_json(silent=True) or {}
    farmer_id = body.get("farmer_id", "")
    count = int(body.get("count", 0))

    if not farmer_id or count <= 0:
        return jsonify(make_response_body(False, "farmer_id and count (>0) required")[0]), 400

    farmer_oid = to_object_id(farmer_id)
    if not farmer_oid:
        return jsonify(make_response_body(False, "Invalid farmer_id")[0]), 400

    farmer = db.users.find_one({"_id": farmer_oid})
    if not farmer:
        return jsonify(make_response_body(False, "Farmer not found")[0]), 404

    farmer_code = body.get("farmer_code", f"FARM{farmer_id[-3:].upper()}")
    tags = allocate_tags(farmer_id, farmer_code, count)

    officer_id = get_jwt_identity()

    # Audit
    db.audit_logs.insert_one({
        "user_id": officer_id,
        "action": AUDIT_TAG_ALLOCATE,
        "details": f"Allocated {count} RFID tags for farmer {farmer_id}",
        "ip_address": get_client_ip(request),
        "timestamp": now_utc(),
    })

    # Notify farmer
    db.notifications.insert_one({
        "user_id": farmer_id,
        "title": "RFID Tags Allocated",
        "body": f"{count} RFID tags have been allocated to your cattle.",
        "type": NOTIF_TAG_ALLOCATED,
        "read": False,
        "created_at": now_utc(),
    })

    return jsonify(make_response_body(True, f"{count} tags allocated", {
        "farmer_id": farmer_id,
        "tags_allocated": count,
        "tags": [serialize_doc(t) for t in tags],
    })[0]), 201


@rfid_bp.route("/tags/<farmer_id>", methods=["GET"])
@any_authenticated
def get_farmer_tags(farmer_id):
    """Get all RFID tags for a farmer."""
    tags = list(db.rfid_tags.find({"farmer_id": farmer_id}))
    return jsonify(make_response_body(True, "Tags fetched", serialize_docs(tags))[0]), 200


@rfid_bp.route("/boundary/<farmer_id>", methods=["GET"])
@any_authenticated
def get_boundary(farmer_id):
    """Get the RFID boundary (allocated tag set) for a farmer."""
    boundary = db.rfid_boundaries.find_one({"farmer_id": farmer_id})
    if not boundary:
        return jsonify(make_response_body(False, "No boundary found for this farmer")[0]), 404
    return jsonify(make_response_body(True, "Boundary fetched", serialize_doc(boundary))[0]), 200


@rfid_bp.route("/boundary-check", methods=["POST"])
@any_authenticated
def boundary_check():
    """Check if a tag belongs to a farmer's boundary.

    Body: { farmer_id, tag_id }
    """
    body = request.get_json(silent=True) or {}
    farmer_id = body.get("farmer_id", "")
    tag_id = body.get("tag_id", "")

    if not farmer_id or not tag_id:
        return jsonify(make_response_body(False, "farmer_id and tag_id required")[0]), 400

    result = check_boundary(farmer_id, tag_id)
    color_map = {"matched": "green", "unmatched": "red", "suspicious": "orange"}

    return jsonify(make_response_body(True, "Boundary check complete", {
        "tag_id": tag_id,
        "farmer_id": farmer_id,
        "result": result,
        "color": color_map.get(result, "red"),
    })[0]), 200


@rfid_bp.route("/tags/<tag_id>/status", methods=["PUT"])
@staff_required
def update_tag_status(tag_id):
    """Update a single tag's status (active/inactive/lost)."""
    body = request.get_json(silent=True) or {}
    new_status = body.get("status", "")

    if new_status not in (TAG_STATUS_ACTIVE, TAG_STATUS_INACTIVE, TAG_STATUS_LOST):
        return jsonify(make_response_body(False, f"Invalid status. Use: {TAG_STATUS_ACTIVE}, {TAG_STATUS_INACTIVE}, {TAG_STATUS_LOST}")[0]), 400

    result = db.rfid_tags.update_one(
        {"tag_id": tag_id},
        {"$set": {"status": new_status, "updated_at": now_utc()}},
    )
    if result.matched_count == 0:
        return jsonify(make_response_body(False, "Tag not found")[0]), 404

    tag = db.rfid_tags.find_one({"tag_id": tag_id})
    return jsonify(make_response_body(True, "Tag status updated", serialize_doc(tag))[0]), 200
