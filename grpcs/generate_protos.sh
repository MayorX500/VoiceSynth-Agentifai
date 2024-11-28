#!/bin/bash

python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/tts.proto
python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/normalizer.proto