from flask import Blueprint, request, jsonify
from ..utils.utils import validate_schema
from ..utils.auth_utils import encode_auth_token, token_required
from src.db import Session_Factory
from ..models import User
from werkzeug.utils import secure_filename

file_bp = Blueprint("file", __name__)


@file_bp.route("/upload", method=["POST"])
@token_required
def uplodad_file(user_id):
    # validate file

    with Session_Factory() as session_:
        # user = session_.query(User).filter_by(id=user_id).first()
        if "file" not in request.files:
            return jsonify({
                "status": "fail",
                "message": "No file uploaded"
            }), 400
        
        file = request.files["file"]
        filename = secure_filename(file.filename)

@file_bp.route("/files")
@token_required
def upload_file(user_id):
    ...


@file_bp.route("/download/<int:file_id>")
@token_required
def upload_file(user_id, file_id):
    ...