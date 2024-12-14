#!/bin/bash

activate_env() {
	if [ ! -d ".env_api" ]; then
		python3 -m venv .env_client
	fi
	source .env_client/bin/activate
	pip install -r enviromets/client_requirements.txt
}

export CONN_PORT=50051
export PROXY_ADD=sparrow

activate_env

python app_client sparrow $1
