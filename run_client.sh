#!/bin/bash

source .env_client/bin/activate

export CONN_PORT=50051
export PROXY_ADD=sparrow

python app_client sparrow $1
