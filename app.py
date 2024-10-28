# app.py
from flask import Flask, jsonify, make_response, request, send_file
from flask_cors import CORS
import os
import subprocess

from rich import _console

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
        # audio_path = ...
        # Monta o comando espeak
        command = f'espeak "{text}" --stdout > "outputs/generated.wav"'
        # Executa o comando
        subprocess.run(command, shell=True, check=True)
        
        
        audio_path = "outputs/generated.wav"

        
        # Enviar o áudio de volta como resposta
        response = make_response(send_file(audio_path, mimetype="audio/wav"))
        response.headers["Content-Disposition"] = "attachment; filename=output.wav"
        return response
    else:
        return jsonify({"error": "Texto não fornecido"}), 400


if __name__ == "__main__":
    app.run(port=5000)