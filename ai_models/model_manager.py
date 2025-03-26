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
        logger.debug(f"Received ProcessFile request with model_name={request.model_name}, object_key={request.object_key}, output_object_key={request.output_object_key}")

        model_name = request.model_name
        object_key = request.object_key  # Object key of the file stored in MinIO
        output_object_key = request.output_object_key  # Object key for the processed file

        # Get the model (use your logic to load the model)
        model = U_Net()
        if not model:
            logger.error(f"Model '{model_name}' not found")
            return model_manager_pb2.ProcessResponse(
                status="fail", 
                message=f"Model '{model_name}' not found", 
                object_key=""
            )

        # Download the file from MinIO using the object_key
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, "input.acq")
        try:
            minio_client.fget_object(BUCKET_NAME, object_key, file_path)
            logger.info(f"Downloaded file from MinIO with object key: {object_key}")

            # Process the file with U_Net
            processed_file_path = model.process(Path(file_path))
            logger.info(f"Processed file at {processed_file_path}")

            # Upload processed file to MinIO
            try:
                file_size = os.path.getsize(processed_file_path)
                content_type = mimetypes.guess_type(processed_file_path)[0] or "application/octet-stream"

                minio_client.fput_object(
                    BUCKET_NAME,
                    object_name=output_object_key,
                    file_path=processed_file_path,
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
            os.remove(processed_file_path)

            logger.info(f"File processed successfully with model: {model_name}")
            return model_manager_pb2.ProcessResponse(
                status="success", 
                message=f"Successfully processed with model: {model_name}", 
                object_key=output_object_key
            )

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            return model_manager_pb2.ProcessResponse(
                status="fail",
                message=f"Error processing file: {str(e)}",
                object_key=""
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