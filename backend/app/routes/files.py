from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import io
from bson import ObjectId
from ..extensions import get_db, get_fs
from ..services.image_service import compress_image

files_bp = Blueprint('files', __name__)

@files_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    fs = get_fs()
    
    if 'file' not in request.files:
        return jsonify({"error": "No file in request"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No filename"}), 400
        
    try:
        file_data = file.read()
        content_type = file.content_type
        
        # Image compression if applicable
        if content_type and content_type.startswith('image/'):
            file_data = compress_image(file_data)
            content_type = 'image/jpeg'  # standard output of our compression
            
        file_id = fs.put(
            file_data,
            filename=file.filename,
            content_type=content_type,
            metadata={
                "farmer_id": ObjectId(get_jwt_identity()),
                "uploaded_at": datetime.utcnow() if 'datetime' in globals() else io.sys.modules['datetime'].datetime.utcnow()
            }
        )
        
        return jsonify({
            "message": "File uploaded successfully",
            "file_id": str(file_id),
            "filename": file.filename,
            "content_type": content_type
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@files_bp.route('/<file_id>', methods=['GET'])
def get_file(file_id):
    fs = get_fs()
    try:
        grid_out = fs.get(ObjectId(file_id))
        return send_file(
            io.BytesIO(grid_out.read()),
            mimetype=grid_out.content_type,
            as_attachment=False,
            download_name=grid_out.filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@files_bp.route('/<file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    fs = get_fs()
    try:
        fs.delete(ObjectId(file_id))
        return jsonify({"message": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
