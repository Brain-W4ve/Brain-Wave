from flask import Blueprint, request, jsonify, send_file
from ..utils.utils import validate_schema
from ..utils.auth_utils import encode_auth_token, token_required
from src.db import Session_Factory
from ..models import File
from src.os_storage import minio_client, BUCKET_NAME
from werkzeug.utils import secure_filename
import uuid
from ..schemas.file import (
    # FileMetadataSchema, 
    FileUploadSchema,
    FileSummarySchema,
    FileDetailSchema
)
import os

file_bp = Blueprint("file", __name__)


file_upload_schema = FileUploadSchema()
# file_metadata_schema = FileMetadataSchema(many=True)
file_summary_schema = FileSummarySchema(many=True)
file_detail_schema = FileDetailSchema()


def upload_to_minio(user_id, file_stream, filename, content_type):
    """Uploads a file to MinIO and saves metadata in the database."""
    object_key = f"{user_id}/{uuid.uuid4()}-{secure_filename(filename)}"
    file_size = os.fstat(file_stream.fileno()).st_size

    # Upload to MinIO
    minio_client.put_object(
        BUCKET_NAME,
        object_name=object_key,
        data=file_stream,
        length=file_size,
        content_type=content_type,
        part_size=10 * 1024 * 1024  # 10MB
    )

    # Save file metadata in the database
    with Session_Factory() as session_:
        new_file = File(
            filename=filename,
            content_type=content_type,
            object_key=object_key,
            user_id=user_id
        )
        session_.add(new_file)
        session_.commit()
        session_.refresh(new_file)

    return new_file, object_key 

@file_bp.route("/upload", methods=["POST"])
@token_required
def upload_file(user_id):
    """Uploads a file and stores metadata."""
    if "file" not in request.files:
        return jsonify({"status": "fail", "message": "No file uploaded"}), 400

    file = request.files["file"]

    file_data, error = validate_schema(file_upload_schema, {"file": file})
    if error:
        return error

    new_file, _ = upload_to_minio(user_id, file.stream, file.filename, file.content_type)

    return jsonify({
        "status": "success",
        "message": "File uploaded",
        "file_id": new_file.id,
        "object_key": new_file.object_key
    }), 201

@file_bp.route("/files")
@token_required
def list_files(user_id):
    with Session_Factory() as session_:
        user_files = session_.query(File).filter_by(user_id=user_id).all()

        files_data = file_summary_schema.dump(user_files)

        return jsonify({
            "status": "success",
            "files": files_data
        })


@file_bp.route("/download/<int:file_id>")
@token_required
def download_file(user_id, file_id):
    """Fetches a file from MinIO and returns it as a response."""
    
    # Retrieve the file metadata from the database
    with Session_Factory() as session_:
        file = session_.query(File).filter_by(id=file_id, user_id=user_id).first()

        if not file:
            return jsonify({
                "status": "fail",
                "message": "File not found"
            }), 404

        # Fetch the file from MinIO
        try:
            file_stream = minio_client.get_object(BUCKET_NAME, file.object_key)
        except Exception as e:
            return jsonify({
                "status": "fail",
                "message": f"Failed to fetch the file from MinIO: {str(e)}"
            }), 500

        # Send the file as a response to the user
        return send_file(
            file_stream, 
            as_attachment=True, 
            download_name=file.filename,  # Use 'download_name' instead of 'attachment_filename'
            mimetype=file.content_type
        )
    
@file_bp.route("/file/<int:file_id>")
@token_required
def get_file_info(user_id, file_id):
    """Returns metadata for a specific file"""
    with Session_Factory() as session_:
        file = session_.query(File).filter_by(id=file_id, user_id=user_id).first()

        if not file:
            return jsonify({
                "status": "fail",
                "message": "File not found",
            }), 404
        
        file_data = file_detail_schema.dump(file)
        return jsonify({
            "status": "success",
            "file": file_data
        }), 200