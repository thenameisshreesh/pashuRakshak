from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId
from ..extensions import get_db
from ..utils.helpers import serialize_doc

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    db = get_db()
    try:
        total_farmers = db.users.count_documents({"role": "farmer"})
        total_schemes = db.schemes.count_documents({"active": True})
        pending_applications = db.applications.count_documents({"status": "pending"})
        active_raids = db.raids.count_documents({"status": "scheduled"})
        
        # Recent applications
        recent_apps_cursor = db.applications.find().sort("created_at", -1).limit(5)
        recent_apps = list(recent_apps_cursor)
        for app in recent_apps:
            farmer = db.users.find_one({"_id": app["farmer_id"]}, {"name": 1})
            scheme = db.schemes.find_one({"_id": app["scheme_id"]}, {"name": 1})
            app["farmer_name"] = farmer["name"] if farmer else "Unknown"
            app["scheme_name"] = scheme["name"] if scheme else "Unknown"
            serialize_doc(app)
            
        return jsonify({
            "total_farmers": total_farmers,
            "total_schemes": total_schemes,
            "pending_applications": pending_applications,
            "active_raids": active_raids,
            "recent_applications": recent_apps
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/cattle-attendance', methods=['GET'])
@jwt_required()
def get_cattle_attendance():
    # Return 12 months mock cattle attendance chart data
    data = [
        {"month": "Jan", "attendance_rate": 94.5},
        {"month": "Feb", "attendance_rate": 95.2},
        {"month": "Mar", "attendance_rate": 93.8},
        {"month": "Apr", "attendance_rate": 96.1},
        {"month": "May", "attendance_rate": 94.0},
        {"month": "Jun", "attendance_rate": 95.7},
        {"month": "Jul", "attendance_rate": 93.2},
        {"month": "Aug", "attendance_rate": 96.5},
        {"month": "Sep", "attendance_rate": 97.1},
        {"month": "Oct", "attendance_rate": 95.9},
        {"month": "Nov", "attendance_rate": 96.3},
        {"month": "Dec", "attendance_rate": 97.8}
    ]
    return jsonify(data), 200

@analytics_bp.route('/scheme-stats', methods=['GET'])
@jwt_required()
def get_scheme_stats():
    db = get_db()
    try:
        schemes = list(db.schemes.find({"active": True}))
        data = []
        for s in schemes:
            count = db.applications.count_documents({"scheme_id": s["_id"]})
            data.append({
                "scheme_name": s["name"],
                "applications_count": count
            })
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/validation-stats', methods=['GET'])
@jwt_required()
def get_validation_stats():
    db = get_db()
    try:
        passed = db.validations.count_documents({"result": "pass"})
        failed = db.validations.count_documents({"result": "fail"})
        total = passed + failed
        
        return jsonify([
            {"status": "Passed", "value": passed},
            {"status": "Failed", "value": failed}
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
