import logging
import grpc
from concurrent import futures
import model_manager_pb2
import model_manager_pb2_grpc
from model_factory import model_factory
from os_storage import minio_client, BUCKET_NAME
import tempfile
from pathlib import Path
import requests
import os
import mimetypes

from models.u_net import U_Net

# Enable logging for gRPC
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB per chunk

class ModelManagerServicer(model_manager_pb2_grpc.ModelManagerServicer):
    def ProcessFile(self, request, context):
        logger.debug(f"Received ProcessFile request with model_name={request.model_name}, download_url={request.download_url}, output_object_key={request.output_object_key}")

        model_name = request.model_name
        download_url = request.download_url
        output_object_key = request.output_object_key

        # Get the model
        # model = model_factory.get_model(model_name)
        model = U_Net()
        if not model:
            logger.error(f"Model '{model_name}' not found")
            return model_manager_pb2.ProcessResponse(
                status="fail", 
                message=f"Model '{model_name}' not found", 
                object_key=""
            )

        # Download file using presigned URL
        temp_dir = tempfile.mkdtemp()
        file_path = Path(temp_dir) / "input.acq"
        try:
            with requests.get(download_url, stream=True) as response:
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(CHUNK_SIZE):
                        f.write(chunk)
        except requests.RequestException as e:
            logger.error(f"Failed to download file: {str(e)}")
            return model_manager_pb2.ProcessResponse(
                status="fail", 
                message=f"Failed to download file: {str(e)}", 
                object_key=""
            )

        # Process file
        resulting_file_path = model.process(file_path)
        print(resulting_file_path)

        # Upload processed file to MinIO
        try:
            file_size = os.path.getsize(resulting_file_path)
            content_type = mimetypes.guess_type(resulting_file_path)[0] or "application/octet-stream"

            minio_client.fput_object(
                BUCKET_NAME,
                object_name=output_object_key,
                file_path=str(resulting_file_path),
                content_type=content_type
            )
            logger.info(f"Successfully uploaded processed file to MinIO with object key: {output_object_key}")
        except Exception as e:
            logger.error(f"Failed to upload processed file: {str(e)}")
            return model_manager_pb2.ProcessResponse(
                status="fail",
                message=f"Failed to upload processed file: {str(e)}",
                object_key=""
            )

        # Clean up temp files
        os.remove(file_path)
        os.remove(resulting_file_path)

        logger.info(f"File processed successfully with model: {model_name}")
        return model_manager_pb2.ProcessResponse(
            status="success", 
            message=f"Successfully processed with model: {model_name}", 
            object_key=output_object_key
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_manager_pb2_grpc.add_ModelManagerServicer_to_server(ModelManagerServicer(), server)
    server.add_insecure_port("[::]:50051")
    logger.info("Starting Model Manager server on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
