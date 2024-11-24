# app.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app_client")))  # Add the app_client directory to the system path

import itertools
import random
import grpc
from app_client import TTSServiceStub, stream_audio_to_file
from flask import Flask, jsonify, make_response, request, send_file
from flask_cors import CORS


## read the IP address of the gRPC server from the environment variable
IPADD = os.getenv("IPADD", "localhost")

request_counter = itertools.count(random.randint(1,100000000))  # Counter for audio requests (starts from 1)
app = Flask(__name__)
CORS(app)  # Permitir requisições de outros domínios

@app.route("/api/tts", methods=["POST"])
def tts():
    # Processamento TTS aqui (substitua pelo modelo que está a treinar)
    # Exemplo: Receber texto ou áudio e devolver o arquivo de áudio gerado
    
    data = request.get_json()  # Receber JSON enviado do frontend
    text = data.get("text") if data else ""  # Extrair o texto do JSON
    language = data.get("language") if data else ""  # Extrair o idioma do JSON

    if text:
        # Implementar conversão de texto para áudio e salvar o áudio
        pid = os.getpid()  # Get the process ID
        with grpc.insecure_channel(f"{IPADD}:50051") as channel:
            stub = TTSServiceStub(channel)
            request_num = next(request_counter)  # Get the next request number
            stream_audio_to_file(stub, text, pid, request_num, output_dir="app_api/outputs", filename=f"generated-{request_num}.wav")       
        audio_path = f"outputs/generated-{request_num}.wav"
        # Enviar o áudio de volta como resposta
        response = make_response(send_file(audio_path, mimetype="audio/wav"))
        response.headers["Content-Disposition"] = "attachment; filename=output.wav"
        return response
    else:
        return jsonify({"error": "Texto não fornecido"}), 400


if __name__ == "__main__":
    app.run(port=5000)