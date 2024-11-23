#!/bin/bash

python3.10 -m grpc_tools.protoc -I=proto --python_out=server --grpc_python_out=server proto/tts.proto
python3.10 -m grpc_tools.protoc -I=proto --python_out=client --grpc_python_out=client proto/tts.proto
