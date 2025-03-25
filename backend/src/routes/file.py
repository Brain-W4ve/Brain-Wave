from flask import Blueprint, request, jsonify, send_file
from ..utils.utils import validate_schema
from ..utils.auth_utils import encode_auth_token, token_required
from src.db import Session_Factory
from ..models import File
from src.os_storage import minio_client, BUCKET_NAME
from werkzeug.utils import secure_filename
import uuid
from ..schemas.file import FileMetadataSchema, FileUploadSchema
import os

file_bp = Blueprint("file", __name__)


file_upload_schema = FileUploadSchema()
file_metadata_schema = FileMetadataSchema(many=True)


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

    return new_file.id, object_key 

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

    file_id, _ = upload_to_minio(user_id, file.stream, file.filename, file.content_type)

    return jsonify({
        "status": "success",
        "message": "File uploaded",
        "file_id": file_id
    }), 201

@file_bp.route("/files")
@token_required
def list_files(user_id):
    with Session_Factory() as session_:
        user_files = session_.query(File).filter_by(user_id=user_id).all()

        files_data = file_metadata_schema.dump(user_files)

        return jsonify({
            "status": "success",
            "files": files_data
        })


def get_download_url(user_id, file_id):
    # Retrieve the file from the database
    with Session_Factory() as session_:
        file = session_.query(File).filter_by(id=file_id, user_id=user_id).first()

        if not file:
            return jsonify({
                "status": "fail",
                "message": "File not found"
            }), 404
        
        # Generate presigned URL from MinIO
        download_url = minio_client.presigned_get_object(
            BUCKET_NAME, 
            file.object_key,
            response_headers={
                "response-content-disposition": f'attachment; filename="{file.filename}"'
            }
        )

    return download_url

"""We delegate the download to minio, following best practices"""
@file_bp.route("/download/<int:file_id>")
@token_required
def download_file(user_id, file_id):
    # Get the download URL using the utility function
    download_url = get_download_url(user_id, file_id)

    # Return the download URL
    if isinstance(download_url, tuple):  # Check if it's an error response (tuple contains status and message)
        return download_url  # Return the error response directly

    return jsonify({
        "status": "success",
        "download_url": download_url
    })