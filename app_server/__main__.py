import sys
import os

from concurrent import futures
import grpc
import tts_pb2
import tts_pb2_grpc
from intlex import Model
import numpy as np
import traceback
import argparse as ap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../db")))  # Add the app_client directory to the system path

from db import models

# Initialize SQLAlchemy engine and sessionmaker
engine = create_engine('sqlite:///tts_system.db')
Session = sessionmaker(bind=engine)

class TTSService(tts_pb2_grpc.TTSServiceServicer):
    def __init__(self,config_file="config/intlex_config.json"):
        self.db_session = Session()  # Initialize the session here
        print("Loading TTS model...")
        self.tts = Model(config_file) 
        print("TTS model initialized successfully!")
        
    def get_voice(self, user_token):
        # Fetch the voice configuration from the database based on the user_token
        user = self.db_session.query(models.User).filter_by(user_token=user_token).first()
        if user and user.voices:
            voice_config = user.voices[0]  # Assuming the user has an associated voice
            return voice_config
        raise ValueError("Voice configuration not found for user_token")

    def SynthesizeStream(self, request_iterator, context, debug=False):
        chunk_index = 0
        block_size = 8192  # Size of the block for streaming audio
        
        # Retrieve metadata from the client
        client_metadata = dict(context.invocation_metadata())
        user_token = client_metadata.get("user_token", None)
        
        if not user_token:
            context.set_details("User token not provided")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return
        
        # Get voice configuration based on user_token
        try:
            voice_config = self.get_voice(user_token)
            print(f"Loaded voice configuration for user_token {user_token}: {voice_config}")
            print(f"Voice configuration: {voice_config.file_path}")

            for request in request_iterator:
                if not context.is_active():
                    break

                text = request.text
                if debug:
                    print(f"Client {user_token} requested synthesis for: {text}")

                audio = self.tts.generate_audio(text, voice_path=voice_config.file_path) # lang default is "pt"
                audio = np.clip(audio, -1.0, 1.0)
                audio = np.int16(audio * 32767)
                
                for i in range(0, len(audio), block_size):
                    audio_chunk = audio[i:i + block_size]
                    yield tts_pb2.SynthesisResponse(
                        audio_chunk=audio_chunk.tobytes(),
                        chunk_index=chunk_index
                    )
                    chunk_index += 1

        except Exception as e:
            print(f"Error processing user_token {user_token}: {e}")
            traceback.print_exc()
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

def serve(args):
    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    tts_pb2_grpc.add_TTSServiceServicer_to_server(TTSService(args.configuration_file), server)
    server.add_insecure_port('[::]:50051')
    if args.debug:
        print("TTS server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument('configuration_file', nargs='?' , type=str, default="config/intlex_config.json", help="Path to the configuration file for the TTS model")
    parser.add_argument('-d',"--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    serve(args)
