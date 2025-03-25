from flask import Blueprint, request, jsonify
from src.utils.auth_utils import token_required
from src.routes.file import get_download_url, upload_to_minio
from src.grpc import model_manager_pb2
from src.grpc_service import stub
from src.db import Session_Factory
from ..models import File
import uuid

process_bp = Blueprint("process", __name__)

@process_bp.route("/process/<int:file_id>", methods=["POST"])
@token_required
def process_file(user_id, file_id):
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"status": "fail", "message": "Invalid JSON or missing Content-Type"}), 400

        model_name = data.get("model")
        if not model_name:
            return jsonify({"status": "fail", "message": "Model name is required"}), 400

        # Get the original file's download URL
        download_url = get_download_url(user_id, file_id)
        if isinstance(download_url, tuple):  # Handle errors
            return download_url

        # Generate a unique output key for the processed file
        object_key = f"{user_id}/{uuid.uuid4()}-processed.json"
        processed_filename = object_key.split("/")[-1]

        # Create gRPC request
        grpc_request = model_manager_pb2.ProcessRequest(
            model_name=model_name,
            download_url=download_url,
            output_object_key=object_key
        )

        # Call gRPC service
        grpc_response = stub.ProcessFile(grpc_request)

        if grpc_response.status != "success":
            return jsonify({"status": "fail", "message": grpc_response.message}), 500

        # Store the processed file metadata in the database (without re-uploading)
        with Session_Factory() as session_:
            processed_file = File(
                filename=processed_filename,
                content_type="application/octet-stream",
                object_key=object_key,
                user_id=user_id
            )
            session_.add(processed_file)
            session_.commit()
            session_.refresh(processed_file)

        # Return the processed file metadata with MinIO download URL
        return jsonify({
            "status": "success",
            "message": "File processed successfully",
            "file_id": processed_file.id,
            "download_url": get_download_url(user_id, processed_file.id)
        })

    except Exception as e:
        return jsonify({"status": "fail", "message": f"Processing error: {str(e)}"}), 500
