from flask import Blueprint, request, jsonify, send_file
from src.utils.auth_utils import token_required
from src.os_storage import minio_client, BUCKET_NAME
from src.grpc import model_manager_pb2
from src.grpc_service import stub
from src.db import Session_Factory
from ..models import File
import uuid
import tempfile

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

        # Generate a unique output key for the processed file
        object_key = f"{user_id}/{uuid.uuid4()}-processed.json"
        processed_filename = object_key.split("/")[-1]

        # Download the file from MinIO
        file_stream = minio_client.get_object(BUCKET_NAME, file.object_key)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(temp_file.name, "wb") as temp_f:
            for data in file_stream.stream(32 * 1024):  # 32 KB chunks
                temp_f.write(data)
        
        # Create gRPC request with the file data
        with open(temp_file.name, "rb") as file_to_process:
            grpc_request = model_manager_pb2.ProcessRequest(
                model_name=model_name,
                file_data=file_to_process.read(),  # Send file content for processing
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
                content_type="application/json",  # Adjust based on your actual file type
                object_key=object_key,
                user_id=user_id
            )
            session_.add(processed_file)
            session_.commit()
            session_.refresh(processed_file)

        # Fetch the processed file from MinIO
        processed_file_stream = minio_client.get_object(BUCKET_NAME, processed_file.object_key)

        # Send the processed file to the user
        return send_file(
            processed_file_stream,
            as_attachment=True,
            download_name=processed_filename,  # Filename for the download
            mimetype="application/json"  # You can adjust the MIME type accordingly
        )

    except Exception as e:
        return jsonify({"status": "fail", "message": f"Processing error: {str(e)}"}), 500
