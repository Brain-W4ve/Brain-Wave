from flask import Blueprint, request, jsonify, send_file
from ..utils.utils import validate_schema
from ..utils.auth_utils import encode_auth_token, token_required
from src.db import Session_Factory
from ..models import File
from src.os_storage import minio_client, BUCKET_NAME
from werkzeug.utils import secure_filename
import uuid
from io import BytesIO
from ..schemas.file import FileMetadataSchema, FileUploadSchema
import os

file_bp = Blueprint("file", __name__)


file_upload_schema = FileUploadSchema()
file_metadata_schema = FileMetadataSchema(many=True)

@file_bp.route("/upload", methods=["POST"])
@token_required
def upload_file(user_id):
    # validate file with marshmallow
    if "file" not in request.files:
        return jsonify({
            "status": "fail",
            "message": "No file uploaded"
        }), 400
    
    file = request.files["file"]
  

    file_data, error = validate_schema(file_upload_schema, {"file": file})
    if error:
        return error

    filename = secure_filename(file.filename)
    content_type = file.content_type
    file_size = os.fstat(file.fileno()).st_size
    object_key = f"{user_id}/{uuid.uuid4()}-{filename}"

    # Upload file to minIo
    minio_client.put_object(
        BUCKET_NAME,
        object_name=object_key,
        data=file.stream,
        length=file_size,
        content_type=content_type,
        part_size=10 * 1024 * 1024
    )

    # # Store metadata in DB
    with Session_Factory() as session_:
        new_file = File(filename=filename, content_type=content_type, object_key=object_key, user_id=user_id)
        session_.add(new_file)
        session_.commit()
        session_.refresh(new_file)

    return jsonify({
        "status": "successs",
        "message": "File uploaded",
        "file_id": new_file.id
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

""" Previous implementation, this gives us more control on auth but has more overhead on flask"""
# @file_bp.route("/download/<int:file_id>")
# @token_required
# def download_files(user_id, file_id):
#     with Session_Factory() as session_:
#         file = session_.query(File).filter_by(id=file_id, user_id=user_id).first()

#         if not file:
#             return jsonify({
#                 "status": "fail",
#                 "message": "File not found",
#             }), 404
        
#         # fetch file from minio
#         response = minio_client.get_object(BUCKET_NAME, file.object_key)

#         file_data = BytesIO(response.read())
#         response.close()
#         response.release_conn()

#         return send_file(
#             file_data,
#             mimetype=file.content_type,
#             as_attachment=True,
#             download_name=file.filename
#         )

"""We delegate the download to minio, following best practices"""
@file_bp.route("/download/<int:file_id>")
@token_required
def download_file(user_id, file_id):
    with Session_Factory() as session_:
        file = session_.query(File).filter_by(id=file_id, user_id=user_id).first()

        if not file:
            return jsonify({
                "status": "fail",
                "messsage": "File not found"
            }), 404
        
        download_url = minio_client.presigned_get_object(
            BUCKET_NAME, 
            file.object_key,
            response_headers={
                "response-content-disposition": f'attachment; filename="{file.filename}"'
            }    
        )

        return jsonify({
            "status": "success",
            "download_url": download_url
        })
