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

@app.route("/api/tts", methods=["POST"])
def tts():
    print("Request received")
    # Processamento TTS aqui (substitua pelo modelo que está a treinar)
    # Exemplo: Receber texto ou áudio e devolver o arquivo de áudio gerado
    
    data = request.get_json()  # Receber JSON enviado do frontend
    text = data.get("text") if "text" in data.keys() else ""  # Extrair o texto do JSON
    language = data.get("language") if "language" in data.keys() else ""  # Extrair o idioma do JSON
    user_token = data.get("user_token") if "user_token" in data.keys() else "1"  # Extrair o token do usuário do JSON

    if text:
        # Implementar conversão de texto para áudio e salvar o áudio
        with grpc.insecure_channel(f"{PROXY_ADD}:{PROXY_PORT}") as channel:
            stub = TTSServiceStub(channel)
            request_num = next(request_counter)  # Get the next request number
            synthesize_text(stub, user_token, text=text, output_dir="app_api/outputs", filename=f"generated-{request_num}.wav", debug=True)       
        audio_path = f"outputs/generated-{request_num}.wav"
        # Enviar o áudio de volta como resposta
        response = make_response(send_file(audio_path, mimetype="audio/wav"))
        response.headers["Content-Disposition"] = "attachment; filename=output.wav"
        print("Response sent")
        return response
    else:
        return jsonify({"error": "Texto não fornecido"}), 400
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)  # Iniciar o servidor Flask