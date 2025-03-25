import grpc
import os
from src.grpc import model_manager_pb2_grpc

GRPC_SERVER = os.getenv("GRPC_SERVER", "localhost:50051")

# Create a gRPC channel and stub
channel = grpc.insecure_channel(GRPC_SERVER)
stub = model_manager_pb2_grpc.ModelManagerStub(channel)
