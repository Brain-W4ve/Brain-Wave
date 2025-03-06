from flask import Blueprint, request, jsonify, send_file
from ..utils.utils import validate_schema
from ..utils.auth_utils import encode_auth_token, token_required
from src.db import Session_Factory
from ..models import File
from src.os_storage import minio_client, BUCKET_NAME
from werkzeug.utils import secure_filename
import uuid
from io import BytesIO

file_bp = Blueprint("file", __name__)


@file_bp.route("/upload", method=["POST"])
@token_required
def uplodad_file(user_id):
    # validate file with marshmallow

    with Session_Factory() as session_:
        if "file" not in request.files:
            return jsonify({
                "status": "fail",
                "message": "No file uploaded"
            }), 400
        
        
        file = request.files["file"]
        filename = secure_filename(file.filename)
        content_type = file.content_type

        object_key = f"{user_id}/{uuid.uuid4()}-{filename}"

        # Upload file to minIo
        minio_client.put_object(
            BUCKET_NAME,
            object_name=object_key,
            data=file.stream,
            length=-1,
            content_type=content_type,
            part_size=10 * 1024 * 1024
        )

        # Store metadata in DB
        new_file = File(filename=filename, content_type=content_type, object_key=object_key, user_id=user_id)
        session_.add(new_file)
        session_.commit()
    return jsonify({
        "status": "successs",
        "message": "File uploaded",
        "file_id": new_file.id
    }), 201

@file_bp.route("/files")
@token_required
def upload_file(user_id):
    with Session_Factory() as session_:
        user_files = session_.query(File).filter_by(user_id=user_id).all()

        # serialize with marshmallow, not like this
        files_data = [
            {
                "id": file.id,
                "filename": file.filename,
                "content_type": file.content_type,
                "download_url": f"/download/{file.id}",
                "uploaded_at": file.upload_date
            }
            for file in user_files
        ]

        return jsonify({
            "status": "success",
            "files": files_data
        })

@file_bp.route("/download/<int:file_    id>")
@token_required
def upload_file(user_id, file_id):
    with Session_Factory() as session_:
        file = session_.query(File).filter_by(id=file_id, user_id=user_id).first()

        if not file:
            return jsonify({
                "status": "fail",
                "message": "File not found",
            }), 404
        
        # fetch file from minio
        response = minio_client.get_object(BUCKET_NAME, file.object_key)

        return send_file(
            BytesIO(response.read()),
            mimetype=file.content_type,
            as_attachment=True,
            download_name=file.filename
        )
