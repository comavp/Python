To generate 'greeting_service_pb2.py' and 'greeting_service_pb2_grpc.py' use this command:

python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. greeting_service.proto
