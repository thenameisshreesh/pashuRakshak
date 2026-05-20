"""
Scheme application routes – multi-step submit, update, list, resubmit.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId

from app.extensions import db
from app.utils.helpers import (
    serialize_doc, serialize_docs, paginate_query,
    now_utc, make_response_body, to_object_id,
)
from app.utils.constants import (
    STATUS_PENDING, STATUS_UNDER_REVIEW, STATUS_APPROVED,
    STATUS_REJECTED, STATUS_RESUBMITTED,
    NOTIF_APPLICATION_STATUS,
    AUDIT_APPLICATION_SUBMIT, AUDIT_APPLICATION_UPDATE,
    STEP_BASIC_DETAILS, STEP_DOCUMENTS, STEP_CATTLE_PROOF, TOTAL_STEPS,
    ROLE_FARMER,
)
from app.middleware.auth_guard import any_authenticated, staff_required, farmer_required
from app.utils.helpers import get_client_ip

applications_bp = Blueprint("applications", __name__, url_prefix="/api/applications")


def _create_notification(user_id, title, body, notif_type=NOTIF_APPLICATION_STATUS):
    """Helper to insert a notification document."""
    db.notifications.insert_one({
        "user_id": user_id,
        "title": title,
        "body": body,
        "type": notif_type,
        "read": False,
        "created_at": now_utc(),
    })


# ─── Submit Application (Multi-Step) ─────────────────────────
@applications_bp.route("/submit", methods=["POST"])
@farmer_required
def submit_application():
    """Submit or update a multi-step scheme application.

    Body: { scheme_id, step, data: {...} }
    Step 1 creates the application; steps 2-3 update it.
    """
    user_id = get_jwt_identity()
    body = request.get_json(silent=True) or {}
    step = int(body.get("step", 1))
    scheme_id = body.get("scheme_id", "")
    step_data = body.get("data", {})

    if not scheme_id:
        return jsonify(make_response_body(False, "scheme_id is required")[0]), 400

    scheme_oid = to_object_id(scheme_id)
    if not scheme_oid or not db.schemes.find_one({"_id": scheme_oid}):
        return jsonify(make_response_body(False, "Invalid scheme_id")[0]), 400

    if step == STEP_BASIC_DETAILS:
        # Check for existing draft
        existing = db.applications.find_one({
            "farmer_id": user_id,
            "scheme_id": scheme_id,
            "status": {"$in": [STATUS_PENDING, STATUS_RESUBMITTED]},
        })
        if existing:
            # Update existing draft
            db.applications.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "step1": step_data,
                    "current_step": step,
                    "updated_at": now_utc(),
                }},
            )
            app_doc = db.applications.find_one({"_id": existing["_id"]})
            return jsonify(make_response_body(True, "Step 1 updated", serialize_doc(app_doc))[0]), 200

        # Create new application
        app_doc = {
            "farmer_id": user_id,
            "scheme_id": scheme_id,
            "status": STATUS_PENDING,
            "current_step": step,
            "step1": step_data,
            "step2": {},
            "step3": {},
            "documents": [],
            "validation_history": [],
            "rejection_reason": "",
            "rejection_notes": "",
            "reviewed_by": None,
            "created_at": now_utc(),
            "updated_at": now_utc(),
        }
        result = db.applications.insert_one(app_doc)
        app_doc["_id"] = result.inserted_id

        # Audit
        db.audit_logs.insert_one({
            "user_id": user_id,
            "action": AUDIT_APPLICATION_SUBMIT,
            "details": f"Application submitted for scheme {scheme_id} (Step 1)",
            "ip_address": get_client_ip(request),
            "timestamp": now_utc(),
        })

        return jsonify(make_response_body(True, "Application created (Step 1)", serialize_doc(app_doc))[0]), 201

    # Steps 2 & 3 — update existing application
    application_id = body.get("application_id", "")
    if not application_id:
        return jsonify(make_response_body(False, "application_id required for steps 2+")[0]), 400

    app_oid = to_object_id(application_id)
    if not app_oid:
        return jsonify(make_response_body(False, "Invalid application_id")[0]), 400

    app_doc = db.applications.find_one({"_id": app_oid, "farmer_id": user_id})
    if not app_doc:
        return jsonify(make_response_body(False, "Application not found")[0]), 404

    step_key = f"step{step}"
    update = {
        step_key: step_data,
        "current_step": step,
        "updated_at": now_utc(),
    }

    # If final step, mark ready for review
    if step == TOTAL_STEPS:
        update["status"] = STATUS_PENDING
        update["current_step"] = TOTAL_STEPS

    db.applications.update_one({"_id": app_oid}, {"$set": update})

    # Audit
    db.audit_logs.insert_one({
        "user_id": user_id,
        "action": AUDIT_APPLICATION_UPDATE,
        "details": f"Application {application_id} updated (Step {step})",
        "ip_address": get_client_ip(request),
        "timestamp": now_utc(),
    })

    updated = db.applications.find_one({"_id": app_oid})
    return jsonify(make_response_body(True, f"Step {step} saved", serialize_doc(updated))[0]), 200


# ─── Resubmit Rejected Application ──────────────────────────
@applications_bp.route("/<app_id>/resubmit", methods=["PUT"])
@farmer_required
def resubmit_application(app_id):
    """Allow a farmer to edit and resubmit a rejected application."""
    user_id = get_jwt_identity()
    app_oid = to_object_id(app_id)
    if not app_oid:
        return jsonify(make_response_body(False, "Invalid application ID")[0]), 400

    app_doc = db.applications.find_one({"_id": app_oid, "farmer_id": user_id})
    if not app_doc:
        return jsonify(make_response_body(False, "Application not found")[0]), 404

    if app_doc["status"] != STATUS_REJECTED:
        return jsonify(make_response_body(False, "Only rejected applications can be resubmitted")[0]), 400

    body = request.get_json(silent=True) or {}
    update = {
        "status": STATUS_RESUBMITTED,
        "rejection_reason": "",
        "rejection_notes": "",
        "current_step": body.get("current_step", TOTAL_STEPS),
        "updated_at": now_utc(),
    }
    # Allow updating step data
    for s in ["step1", "step2", "step3"]:
        if s in body:
            update[s] = body[s]

    db.applications.update_one({"_id": app_oid}, {"$set": update})

    _create_notification(
        user_id,
        "Application Resubmitted",
        f"Your application has been resubmitted for review.",
    )

    updated = db.applications.find_one({"_id": app_oid})
    return jsonify(make_response_body(True, "Application resubmitted", serialize_doc(updated))[0]), 200


# ─── List Applications ──────────────────────────────────────
@applications_bp.route("", methods=["GET"])
@any_authenticated
def list_applications():
    """List applications – farmers see their own, staff see all."""
    claims = get_jwt()
    user_id = get_jwt_identity()
    role = claims.get("role", "")

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    status_filter = request.args.get("status", "").strip()
    scheme_filter = request.args.get("scheme_id", "").strip()

    query = {}
    if role == ROLE_FARMER:
        query["farmer_id"] = user_id
    if status_filter:
        query["status"] = status_filter
    if scheme_filter:
        query["scheme_id"] = scheme_filter

    result = paginate_query(db.applications, query, page, per_page, sort_field="updated_at")
    return jsonify(make_response_body(True, "Applications fetched", result)[0]), 200


# ─── Get Single Application ─────────────────────────────────
@applications_bp.route("/<app_id>", methods=["GET"])
@any_authenticated
def get_application(app_id):
    """Get a single application by ID."""
    app_oid = to_object_id(app_id)
    if not app_oid:
        return jsonify(make_response_body(False, "Invalid application ID")[0]), 400

    claims = get_jwt()
    user_id = get_jwt_identity()
    role = claims.get("role", "")

    query = {"_id": app_oid}
    if role == ROLE_FARMER:
        query["farmer_id"] = user_id

    app_doc = db.applications.find_one(query)
    if not app_doc:
        return jsonify(make_response_body(False, "Application not found")[0]), 404

    return jsonify(make_response_body(True, "Application fetched", serialize_doc(app_doc))[0]), 200


# ─── Add Documents to Application ───────────────────────────
@applications_bp.route("/<app_id>/documents", methods=["POST"])
@farmer_required
def add_document(app_id):
    """Add a document reference (GridFS file_id) to an application."""
    user_id = get_jwt_identity()
    app_oid = to_object_id(app_id)
    if not app_oid:
        return jsonify(make_response_body(False, "Invalid application ID")[0]), 400

    app_doc = db.applications.find_one({"_id": app_oid, "farmer_id": user_id})
    if not app_doc:
        return jsonify(make_response_body(False, "Application not found")[0]), 404

    body = request.get_json(silent=True) or {}
    doc_entry = {
        "file_id": body.get("file_id", ""),
        "doc_type": body.get("doc_type", "other"),
        "filename": body.get("filename", ""),
        "uploaded_at": now_utc().isoformat(),
    }

    db.applications.update_one(
        {"_id": app_oid},
        {"$push": {"documents": doc_entry}, "$set": {"updated_at": now_utc()}},
    )
    updated = db.applications.find_one({"_id": app_oid})
    return jsonify(make_response_body(True, "Document added", serialize_doc(updated))[0]), 200
