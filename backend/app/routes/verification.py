"""
Verification routes – approve / reject applications with dropdown reasons.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId

from app.extensions import db
from app.utils.helpers import serialize_doc, now_utc, make_response_body, to_object_id, get_client_ip
from app.utils.constants import (
    STATUS_PENDING, STATUS_UNDER_REVIEW, STATUS_APPROVED,
    STATUS_REJECTED, STATUS_RESUBMITTED,
    REJECTION_REASONS,
    NOTIF_APPLICATION_STATUS, NOTIF_VALIDATION_COMPLETE,
    AUDIT_APPLICATION_APPROVE, AUDIT_APPLICATION_REJECT,
)
from app.middleware.auth_guard import staff_required
from app.services.validation_service import allocate_tags

verification_bp = Blueprint("verification", __name__, url_prefix="/api/verification")


@verification_bp.route("/rejection-reasons", methods=["GET"])
@staff_required
def get_rejection_reasons():
    """Return the list of predefined rejection reasons for the dropdown."""
    return jsonify(make_response_body(True, "Rejection reasons", REJECTION_REASONS)[0]), 200


@verification_bp.route("/<app_id>/review", methods=["PUT"])
@staff_required
def set_under_review(app_id):
    """Mark an application as under review."""
    app_oid = to_object_id(app_id)
    if not app_oid:
        return jsonify(make_response_body(False, "Invalid application ID")[0]), 400

    app_doc = db.applications.find_one({"_id": app_oid})
    if not app_doc:
        return jsonify(make_response_body(False, "Application not found")[0]), 404

    if app_doc["status"] not in (STATUS_PENDING, STATUS_RESUBMITTED):
        return jsonify(make_response_body(False, f"Cannot review an application with status '{app_doc['status']}'")[0]), 400

    officer_id = get_jwt_identity()
    claims = get_jwt()

    db.applications.update_one({"_id": app_oid}, {"$set": {
        "status": STATUS_UNDER_REVIEW,
        "reviewed_by": officer_id,
        "updated_at": now_utc(),
    }, "$push": {
        "validation_history": {
            "date": now_utc(),
            "officer_id": officer_id,
            "officer_name": claims.get("name", ""),
            "action": "under_review",
            "notes": "Application taken for review",
        },
    }})

    # Notify farmer
    _notify(app_doc["farmer_id"], "Application Under Review",
            "Your application is now being reviewed by an officer.")

    updated = db.applications.find_one({"_id": app_oid})
    return jsonify(make_response_body(True, "Application set to under review", serialize_doc(updated))[0]), 200


@verification_bp.route("/<app_id>/approve", methods=["PUT"])
@staff_required
def approve_application(app_id):
    """Approve an application and allocate RFID tags."""
    app_oid = to_object_id(app_id)
    if not app_oid:
        return jsonify(make_response_body(False, "Invalid application ID")[0]), 400

    app_doc = db.applications.find_one({"_id": app_oid})
    if not app_doc:
        return jsonify(make_response_body(False, "Application not found")[0]), 404

    if app_doc["status"] not in (STATUS_UNDER_REVIEW, STATUS_PENDING, STATUS_RESUBMITTED):
        return jsonify(make_response_body(False, f"Cannot approve an application with status '{app_doc['status']}'")[0]), 400

    officer_id = get_jwt_identity()
    claims = get_jwt()
    body = request.get_json(silent=True) or {}
    notes = body.get("notes", "Application approved")

    # Get farmer cattle count for RFID tag allocation
    farmer = db.users.find_one({"_id": ObjectId(app_doc["farmer_id"])})
    cattle_count = farmer.get("cattle_count", 0) if farmer else 0

    # Generate farmer code
    farmer_code = f"FARM{str(app_doc['farmer_id'])[-3:].upper()}"

    # Allocate RFID tags
    allocated_tags = []
    if cattle_count > 0:
        allocated_tags = allocate_tags(app_doc["farmer_id"], farmer_code, cattle_count)

    db.applications.update_one({"_id": app_oid}, {"$set": {
        "status": STATUS_APPROVED,
        "reviewed_by": officer_id,
        "approved_at": now_utc(),
        "rfid_tags_allocated": len(allocated_tags),
        "updated_at": now_utc(),
    }, "$push": {
        "validation_history": {
            "date": now_utc(),
            "officer_id": officer_id,
            "officer_name": claims.get("name", ""),
            "action": "approved",
            "notes": notes,
        },
    }})

    # Audit
    db.audit_logs.insert_one({
        "user_id": officer_id,
        "action": AUDIT_APPLICATION_APPROVE,
        "details": f"Approved application {app_id}. Allocated {len(allocated_tags)} RFID tags.",
        "ip_address": get_client_ip(request),
        "timestamp": now_utc(),
    })

    # Notify farmer
    _notify(app_doc["farmer_id"], "Application Approved! 🎉",
            f"Your application has been approved. {len(allocated_tags)} RFID tags have been allocated.")

    updated = db.applications.find_one({"_id": app_oid})
    return jsonify(make_response_body(True, "Application approved", {
        "application": serialize_doc(updated),
        "rfid_tags_allocated": len(allocated_tags),
    })[0]), 200


@verification_bp.route("/<app_id>/reject", methods=["PUT"])
@staff_required
def reject_application(app_id):
    """Reject an application with a reason from the dropdown."""
    app_oid = to_object_id(app_id)
    if not app_oid:
        return jsonify(make_response_body(False, "Invalid application ID")[0]), 400

    app_doc = db.applications.find_one({"_id": app_oid})
    if not app_doc:
        return jsonify(make_response_body(False, "Application not found")[0]), 404

    if app_doc["status"] not in (STATUS_UNDER_REVIEW, STATUS_PENDING, STATUS_RESUBMITTED):
        return jsonify(make_response_body(False, f"Cannot reject an application with status '{app_doc['status']}'")[0]), 400

    officer_id = get_jwt_identity()
    claims = get_jwt()
    body = request.get_json(silent=True) or {}
    reason = body.get("reason", "")
    notes = body.get("notes", "")

    if not reason:
        return jsonify(make_response_body(False, "Rejection reason is required")[0]), 400

    db.applications.update_one({"_id": app_oid}, {"$set": {
        "status": STATUS_REJECTED,
        "reviewed_by": officer_id,
        "rejection_reason": reason,
        "rejection_notes": notes,
        "rejected_at": now_utc(),
        "updated_at": now_utc(),
    }, "$push": {
        "validation_history": {
            "date": now_utc(),
            "officer_id": officer_id,
            "officer_name": claims.get("name", ""),
            "action": "rejected",
            "notes": f"Reason: {reason}. {notes}",
        },
    }})

    # Audit
    db.audit_logs.insert_one({
        "user_id": officer_id,
        "action": AUDIT_APPLICATION_REJECT,
        "details": f"Rejected application {app_id}. Reason: {reason}",
        "ip_address": get_client_ip(request),
        "timestamp": now_utc(),
    })

    # Notify farmer
    _notify(app_doc["farmer_id"], "Application Rejected",
            f"Your application has been rejected. Reason: {reason}. You may edit and resubmit.")

    updated = db.applications.find_one({"_id": app_oid})
    return jsonify(make_response_body(True, "Application rejected", serialize_doc(updated))[0]), 200


def _notify(user_id, title, body):
    """Insert a notification for the farmer."""
    db.notifications.insert_one({
        "user_id": user_id,
        "title": title,
        "body": body,
        "type": NOTIF_APPLICATION_STATUS,
        "read": False,
        "created_at": now_utc(),
    })
