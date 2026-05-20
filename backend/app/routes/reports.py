from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import io
from bson import ObjectId
from ..extensions import get_db
from ..services.pdf_service import generate_validation_report

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/validation/<application_id>', methods=['GET'])
@jwt_required()
def download_validation_report(application_id):
    db = get_db()
    try:
        app = db.applications.find_one({"_id": ObjectId(application_id)})
        if not app:
            return jsonify({"error": "Application not found"}), 404
            
        farmer = db.users.find_one({"_id": app["farmer_id"]})
        scheme = db.schemes.find_one({"_id": app["scheme_id"]})
        
        if not farmer or not scheme:
            return jsonify({"error": "Farmer or scheme not found"}), 404
            
        # Get validation history (scan sessions completed)
        validations_cursor = db.validations.find({"application_id": ObjectId(application_id)}).sort("created_at", -1)
        validations = list(validations_cursor)
        
        # Populate officer names for the report
        validation_history = []
        for val in validations:
            # Find the scan session to get the officer
            session = db.scan_sessions.find_one({"_id": val["session_id"]})
            officer_name = "N/A"
            if session:
                officer = db.users.find_one({"_id": session["officer_id"]}, {"name": 1})
                if officer:
                    officer_name = officer["name"]
            
            validation_history.append({
                "date": val["created_at"],
                "officer_name": officer_name,
                "action": "Inspection Scan",
                "notes": f"Matched: {val['matched_count']}/{val['total_allocated']}. Result: {val['result'].upper()}"
            })
            
        pdf_bytes = generate_validation_report(farmer, scheme, app, validation_history)
        
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"validation_report_{application_id}.pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
