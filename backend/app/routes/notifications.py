from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime
from ..extensions import get_db
from ..utils.helpers import serialize_doc, paginate

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('', methods=['GET'])
@jwt_required()
def list_notifications():
    db = get_db()
    user_id = get_jwt_identity()
    
    query = {"user_id": ObjectId(user_id)}
    
    read_filter = request.args.get('read')
    if read_filter is not None:
        query['read'] = read_filter.lower() == 'true'
        
    notifications_cursor = db.notifications.find(query).sort("created_at", -1)
    notifications, pagination_meta = paginate(notifications_cursor, request)
    
    for notif in notifications:
        serialize_doc(notif)
        
    return jsonify({"notifications": notifications, "meta": pagination_meta}), 200

@notifications_bp.route('/<notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_read(notification_id):
    db = get_db()
    user_id = get_jwt_identity()
    try:
        result = db.notifications.update_one(
            {"_id": ObjectId(notification_id), "user_id": ObjectId(user_id)},
            {"$set": {"read": True}}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Notification not found"}), 404
        return jsonify({"message": "Notification marked as read"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_read():
    db = get_db()
    user_id = get_jwt_identity()
    try:
        db.notifications.update_many(
            {"user_id": ObjectId(user_id), "read": False},
            {"$set": {"read": True}}
        )
        return jsonify({"message": "All notifications marked as read"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    db = get_db()
    user_id = get_jwt_identity()
    try:
        count = db.notifications.count_documents({"user_id": ObjectId(user_id), "read": False})
        return jsonify({"unread_count": count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
