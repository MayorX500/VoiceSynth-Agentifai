# app.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','app_client')))  # Add the app_client directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpcs'))) # Add the grpcs directory to the system path
from grpcs.tts_pb2_grpc import TTSServiceStub


import itertools
import random
import grpc
from app_client import synthesize_text
from flask import Flask, jsonify, make_response, request, send_file
from flask_cors import CORS


from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

## Connection port
PROXY_PORT = os.getenv("PROXY_PORT")
if not PROXY_PORT:
    PROXY_PORT = 50051 # Default proxy port if not specified in the environment variables

## IP address
PROXY_ADD = os.getenv("PROXY_ADD")
if not PROXY_ADD:
    PROXY_ADD = "localhost" # Default IP address if not specified in the environment variables

PORT = os.getenv("PORT")
if not PORT:
    PORT = 5000  # Default port if not specified in the environment variables

request_counter = itertools.count(random.randint(1,100000000))  # Counter for audio requests (starts from 1)
app = Flask(__name__)
CORS(app)  # Permitir requisições de outros domínios

@app.route("/api/tts", methods=["POST", "OPTIONS"])
def tts():
    if request.method == "OPTIONS":
        # Return an empty response to indicate that the preflight request is OK
        response = make_response('', 204)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response

    # Your existing POST request handling logic
    print("Request received")
    data = request.get_json()
    text = data.get("text", "")
    language = data.get("language", "")
    user_token = data.get("user_token", "1")

    if text:
        with grpc.insecure_channel(f"{PROXY_ADD}:{PROXY_PORT}") as channel:
            stub = TTSServiceStub(channel)
            request_num = next(request_counter)
            synthesize_text(stub, user_token, text=text, output_dir="app_api/outputs", filename=f"generated-{request_num}.wav", debug=True)       
        audio_path = f"outputs/generated-{request_num}.wav"
        response = make_response(send_file(audio_path, mimetype="audio/wav"))
        response.headers["Content-Disposition"] = "attachment; filename=output.wav"
        response.headers.add("Access-Control-Allow-Origin", "*")
        print("Response sent")
        return response
    else:
        return jsonify({"error": "Texto não fornecido"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)  # Iniciar o servidor Flask