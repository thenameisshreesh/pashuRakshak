from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime
from ..extensions import get_db
from ..utils.helpers import serialize_doc, paginate
from ..middleware.auth_guard import role_required

audit_bp = Blueprint('audit', __name__)

@audit_bp.route('', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_audit_logs():
    db = get_db()
    query = {}
    
    action = request.args.get('action')
    if action:
        query['action'] = action
        
    user_id = request.args.get('user_id')
    if user_id:
        try:
            query['user_id'] = ObjectId(user_id)
        except Exception:
            pass
            
    audit_cursor = db.audit_logs.find(query).sort("timestamp", -1)
    logs, pagination_meta = paginate(audit_cursor, request)
    
    for log in logs:
        user = db.users.find_one({"_id": log["user_id"]}, {"name": 1, "role": 1})
        log["user_name"] = user["name"] if user else "System/Unknown"
        log["user_role"] = user["role"] if user else "system"
        serialize_doc(log)
        
    return jsonify({"audit_logs": logs, "meta": pagination_meta}), 200

@audit_bp.route('', methods=['POST'])
@jwt_required()
def create_audit_entry():
    db = get_db()
    data = request.get_json() or {}
    action = data.get('action')
    details = data.get('details')
    
    if not action or not details:
        return jsonify({"error": "Action and details are required"}), 400
        
    try:
        log = {
            "user_id": ObjectId(get_jwt_identity()),
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow()
        }
        db.audit_logs.insert_one(log)
        return jsonify({"message": "Audit log entry created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
