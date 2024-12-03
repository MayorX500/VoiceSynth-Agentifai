#!/bin/bash

run_frontend() {
	cd app
	npm start
}

source .env_api/bin/activate

export PROXY_PORT=50051
export PORT=5001
export PROXY_ADD=sparrow

python app_api &
run_frontend
