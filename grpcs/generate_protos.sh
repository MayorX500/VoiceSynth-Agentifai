#!/bin/bash

python3.10 -m grpc_tools.protoc -I=proto --python_out=app_server --grpc_python_out=app_server proto/tts.proto
python3.10 -m grpc_tools.protoc -I=proto --python_out=app_client --grpc_python_out=app_client proto/tts.proto
