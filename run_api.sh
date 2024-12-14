#!/bin/bash

run_frontend() {
	export REACT_APP_API_PORT=5000
	cd app
	npm install
	npm start
}

activate_env() {
	if [ ! -d ".env_api" ]; then
		python3 -m venv .env_api
	fi
	source .env_api/bin/activate &&
	pip install -r enviroments/api_requirements.txt
}

export PROXY_SERVER_PORT=50051
export PROXY_SERVER_ADDRESS=sparrow

activate_env
python app_api &
run_frontend
