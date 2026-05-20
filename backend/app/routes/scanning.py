from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
from ..extensions import get_db
from ..middleware.auth_guard import role_required
from ..utils.helpers import serialize_doc
from ..services.validation_service import validate_scan_session

scanning_bp = Blueprint('scanning', __name__)

@scanning_bp.route('/session/start', methods=['POST'])
@jwt_required()
@role_required('admin', 'officer')
def start_session():
    db = get_db()
    data = request.get_json() or {}
    raid_id = data.get('raid_id')
    officer_id = get_jwt_identity()
    
    if not raid_id:
        return jsonify({"error": "Raid ID is required"}), 400
        
    try:
        raid = db.raids.find_one({"_id": ObjectId(raid_id)})
        if not raid:
            return jsonify({"error": "Raid not found"}), 404
            
        session = {
            "raid_id": ObjectId(raid_id),
            "officer_id": ObjectId(officer_id),
            "farmer_id": raid["farmer_id"],
            "scheme_id": raid["scheme_id"],
            "application_id": raid["application_id"],
            "status": "active",
            "started_at": datetime.utcnow(),
            "ended_at": None,
            "scanned_tags": []
        }
        
        result = db.scan_sessions.insert_one(session)
        session_id = result.inserted_id
        
        db.raids.update_one({"_id": ObjectId(raid_id)}, {"$set": {"status": "in_progress"}})
        
        return jsonify({"message": "Scan session started", "session_id": str(session_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scanning_bp.route('/tag', methods=['POST'])
def submit_tag():
    db = get_db()
    data = request.get_json() or {}
    session_id = data.get('session_id')
    tag_id = data.get('tag_id')
    
    if not session_id or not tag_id:
        return jsonify({"error": "Session ID and Tag ID are required"}), 400
        
    try:
        session = db.scan_sessions.find_one({"_id": ObjectId(session_id)})
        if not session:
            return jsonify({"error": "Scan session not found"}), 404
            
        if session["status"] != "active":
            return jsonify({"error": "Scan session is not active"}), 400
            
        # Check duplicate scan in this session
        existing_log = db.scan_logs.find_one({"session_id": ObjectId(session_id), "tag_id": tag_id})
        if existing_log:
            return jsonify({
                "status": existing_log["status"],
                "message": "Tag already scanned in this session",
                "tag_id": tag_id
            }), 200
            
        # Validate tag ownership against allocation boundary
        allocation = db.rfid_allocations.find_one({
            "farmer_id": session["farmer_id"],
            "scheme_id": session["scheme_id"]
        })
        
        status = "suspicious"
        if allocation and tag_id in allocation.get("tag_ids", []):
            status = "matched"
        else:
            # Check if this tag belongs to any other farmer (duplicate/corruption check)
            any_allocation = db.rfid_allocations.find_one({"tag_ids": tag_id})
            if any_allocation:
                status = "suspicious"  # Belongs to someone else but brought here!
            else:
                status = "unmatched"  # Unknown external tag
                
        # Insert log
        scan_log = {
            "session_id": ObjectId(session_id),
            "tag_id": tag_id,
            "status": status,
            "scanned_at": datetime.utcnow()
        }
        db.scan_logs.insert_one(scan_log)
        
        # Add to session scanned list
        db.scan_sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$addToSet": {"scanned_tags": tag_id}}
        )
        
        return jsonify({
            "status": status,
            "tag_id": tag_id,
            "message": "Scan recorded"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scanning_bp.route('/session/<session_id>/end', methods=['POST'])
@jwt_required()
@role_required('admin', 'officer')
def end_session(session_id):
    db = get_db()
    try:
        session = db.scan_sessions.find_one({"_id": ObjectId(session_id)})
        if not session:
            return jsonify({"error": "Scan session not found"}), 404
            
        if session["status"] != "active":
            return jsonify({"error": "Scan session is already ended"}), 400
            
        db.scan_sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"status": "completed", "ended_at": datetime.utcnow()}}
        )
        
        # Run validation logic
        results = validate_scan_session(session_id)
        
        # Create validation entry
        validation = {
            "application_id": session["application_id"],
            "raid_id": session["raid_id"],
            "session_id": ObjectId(session_id),
            "matched_count": len(results["matched"]),
            "total_allocated": results["summary"]["total_allocated"],
            "result": "pass" if len(results["matched"]) >= results["summary"]["total_allocated"] else "fail",
            "created_at": datetime.utcnow()
        }
        db.validations.insert_one(validation)
        
        # Update raid status
        db.raids.update_one({"_id": session["raid_id"]}, {"$set": {"status": "completed"}})
        
        # Create notification for farmer
        notification = {
            "user_id": session["farmer_id"],
            "title": "Cattle Validation Completed",
            "body": f"The validation scan results are ready. Status: {validation['result'].upper()} ({validation['matched_count']}/{validation['total_allocated']} matched).",
            "type": "validation_complete",
            "read": False,
            "created_at": datetime.utcnow()
        }
        db.notifications.insert_one(notification)
        
        # Audit log
        audit_log = {
            "user_id": ObjectId(get_jwt_identity()),
            "action": "end_scan_session",
            "details": f"Completed scan session {session_id} for raid {session['raid_id']}. Result: {validation['result']}",
            "timestamp": datetime.utcnow()
        }
        db.audit_logs.insert_one(audit_log)
        
        return jsonify({"message": "Session completed", "result": validation["result"], "summary": results["summary"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scanning_bp.route('/session/<session_id>/results', methods=['GET'])
@jwt_required()
def get_results(session_id):
    try:
        results = validate_scan_session(session_id)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
