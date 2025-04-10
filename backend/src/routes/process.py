from flask import Blueprint, request, jsonify, send_file
from src.utils.auth_utils import token_required
from src.os_storage import minio_client, BUCKET_NAME
from src.grpc import model_manager_pb2
from src.grpc_service import stub
from src.db import Session_Factory
from ..models import File, ProcessedFile
import uuid
from datetime import datetime, timezone

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

        # Get the file metadata from the database
        with Session_Factory() as session_:
            file = session_.query(File).get(file_id)
            if not file:
                return jsonify({"status": "fail", "message": "File not found"}), 404

        # Generate unique output key and filename
        object_key = f"{user_id}/{uuid.uuid4()}-processed.json"
        processed_filename = object_key.split("/")[-1]

        # Create gRPC request
        grpc_request = model_manager_pb2.ProcessRequest(
            model_name=model_name,
            object_key=file.object_key,
            output_object_key=object_key
        )

        # Call gRPC service
        grpc_response = stub.ProcessFile(grpc_request)

        if grpc_response.status != "success":
            return jsonify({"status": "fail", "message": grpc_response.message}), 500

        # Save metadata of the processed file (but not the model metadata itself)
        with Session_Factory() as session_:
            processed_file_entry = ProcessedFile(
                original_file_id=file.id,
                processed_filename=processed_filename,
                model_id=1,
                processed_date=datetime.now(timezone.utc)
            )
            session_.add(processed_file_entry)
            session_.commit()

        # Fetch processed file from storage
        processed_file_stream = minio_client.get_object(BUCKET_NAME, object_key)

        # Send file to client
        return send_file(
            processed_file_stream,
            as_attachment=True,
            download_name=processed_filename,
            mimetype="application/json"
        )

    except Exception as e:
        return jsonify({"status": "fail", "message": f"Processing error: {str(e)}"}), 500