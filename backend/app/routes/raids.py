from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
from ..extensions import get_db
from ..middleware.auth_guard import role_required
from ..utils.helpers import serialize_doc, paginate

raids_bp = Blueprint('raids', __name__)

@raids_bp.route('', methods=['POST'])
@jwt_required()
@role_required('admin', 'officer')
def schedule_raid():
    db = get_db()
    data = request.get_json() or {}
    
    farmer_id = data.get('farmer_id')
    scheme_id = data.get('scheme_id')
    officer_id = data.get('officer_id')
    application_id = data.get('application_id')
    date_str = data.get('date')  # YYYY-MM-DD
    time_str = data.get('time')  # HH:MM
    
    if not all([farmer_id, scheme_id, officer_id, application_id, date_str, time_str]):
        return jsonify({"error": "Missing required fields"}), 400
        
    try:
        raid = {
            "farmer_id": ObjectId(farmer_id),
            "scheme_id": ObjectId(scheme_id),
            "officer_id": ObjectId(officer_id),
            "application_id": ObjectId(application_id),
            "date": date_str,
            "time": time_str,
            "status": "scheduled",
            "created_at": datetime.utcnow()
        }
        
        result = db.raids.insert_one(raid)
        raid_id = result.inserted_id
        
        # Create notification for farmer
        notification = {
            "user_id": ObjectId(farmer_id),
            "title": "Officer Raid Scheduled",
            "body": f"A validation raid has been scheduled for your application on {date_str} at {time_str}.",
            "type": "raid_scheduled",
            "read": False,
            "created_at": datetime.utcnow()
        }
        db.notifications.insert_one(notification)
        
        # Create audit log
        audit_log = {
            "user_id": ObjectId(get_jwt_identity()),
            "action": "schedule_raid",
            "details": f"Scheduled raid for farmer {farmer_id} on {date_str}",
            "timestamp": datetime.utcnow()
        }
        db.audit_logs.insert_one(audit_log)
        
        return jsonify({"message": "Raid scheduled successfully", "raid_id": str(raid_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@raids_bp.route('', methods=['GET'])
@jwt_required()
def list_raids():
    db = get_db()
    role = request.args.get('role')
    user_id = get_jwt_identity()
    
    query = {}
    if role == 'farmer':
        query['farmer_id'] = ObjectId(user_id)
    elif role == 'officer':
        query['officer_id'] = ObjectId(user_id)
        
    status = request.args.get('status')
    if status:
        query['status'] = status
        
    raids_cursor = db.raids.find(query).sort("created_at", -1)
    raids, pagination_meta = paginate(raids_cursor, request)
    
    # Populate references
    for raid in raids:
        farmer = db.users.find_one({"_id": raid["farmer_id"]}, {"name": 1, "mobile": 1})
        scheme = db.schemes.find_one({"_id": raid["scheme_id"]}, {"name": 1})
        officer = db.users.find_one({"_id": raid["officer_id"]}, {"name": 1})
        
        raid["farmer_name"] = farmer["name"] if farmer else "Unknown"
        raid["farmer_mobile"] = farmer["mobile"] if farmer else "Unknown"
        raid["scheme_name"] = scheme["name"] if scheme else "Unknown"
        raid["officer_name"] = officer["name"] if officer else "Unknown"
        serialize_doc(raid)
        
    return jsonify({"raids": raids, "meta": pagination_meta}), 200

@raids_bp.route('/<raid_id>', methods=['GET'])
@jwt_required()
def get_raid(raid_id):
    db = get_db()
    try:
        raid = db.raids.find_one({"_id": ObjectId(raid_id)})
        if not raid:
            return jsonify({"error": "Raid not found"}), 404
            
        farmer = db.users.find_one({"_id": raid["farmer_id"]}, {"name": 1, "mobile": 1})
        scheme = db.schemes.find_one({"_id": raid["scheme_id"]}, {"name": 1})
        officer = db.users.find_one({"_id": raid["officer_id"]}, {"name": 1})
        
        raid["farmer_name"] = farmer["name"] if farmer else "Unknown"
        raid["farmer_mobile"] = farmer["mobile"] if farmer else "Unknown"
        raid["scheme_name"] = scheme["name"] if scheme else "Unknown"
        raid["officer_name"] = officer["name"] if officer else "Unknown"
        
        serialize_doc(raid)
        return jsonify(raid), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@raids_bp.route('/<raid_id>', methods=['PUT'])
@jwt_required()
@role_required('admin', 'officer')
def update_raid_status(raid_id):
    db = get_db()
    data = request.get_json() or {}
    status = data.get('status')
    
    if not status:
        return jsonify({"error": "Status is required"}), 400
        
    try:
        result = db.raids.update_one(
            {"_id": ObjectId(raid_id)},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Raid not found"}), 404
            
        return jsonify({"message": "Raid status updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
