import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpcs'))) # Add the grpcs directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db')))  # Add the db directory to the system path


import json
from concurrent import futures
import grpc
from grpcs import tts_pb2, tts_pb2_grpc, normalizer_pb2, normalizer_pb2_grpc
from intlex import Model
import numpy as np
import traceback
import argparse as ap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

## Load the proxy port from the environment variables
SERVER_PORT = os.getenv("SERVER_PORT")
if SERVER_PORT is None:
    SERVER_PORT = 50051 # Default port if not specified as an environment variable

NORMALIZER_IPADDRESS = os.getenv("NORMALIZER_IPADDRESS")
if NORMALIZER_IPADDRESS is None:
    NORMALIZER_IPADDRESS = "localhost" # Default port if not specified as an environment variable

NORMALIZER_PORT = os.getenv("NORMALIZER_PORT")
if NORMALIZER_PORT is None:
    NORMALIZER_PORT = 50053 # Default port if not specified as an environment variable

from db import models

# Initialize SQLAlchemy engine and sessionmaker
engine = create_engine('sqlite:///tts_system.db')
Session = sessionmaker(bind=engine)

class TTSService(tts_pb2_grpc.TTSServiceServicer):
    def __init__(self,args):
        self.debug = args.debug
        self.db_session = Session()  # Initialize the session here
        with open(args.configuration_file, 'r') as f:
            self.config = json.load(f)
        self.storage_dir = self.config.get("storage_directory", "inputs/voices")
        os.makedirs(self.storage_dir, exist_ok=True)  # Ensure storage directory exists
        if self.debug:
            print("Loading TTS model...")
        self.tts = Model(args.configuration_file)
        if self.debug:
            print("TTS model initialized successfully!")
        self.pre_compute = args.pre_compute
        if self.pre_compute:
            if self.debug:
                print("Creating pre-computed voice configurations...")
            self.create_voice_configs()
        print("TTS service is ready!")
        
    def get_voice(self, user_token):
        # Fetch the voice configuration from the database based on the user_token
        user = self.db_session.query(models.User).filter_by(user_token=user_token).first()
        if user and user.voices:
            voice_config = user.voices[0]  # Assuming the user has an associated voice
            return voice_config
        raise ValueError("Voice configuration not found for user_token")
    
    def create_voice_configs(self):
        self.voices = {}
        for user in self.db_session.query(models.User).all():
            if user.voices:
                voice_config = user.voices[0]
                self.voices[f"{user.user_token}"] = {}
                self.voices[f"{user.user_token}"]["file_path"] = voice_config.file_path
                self.voices[f"{user.user_token}"]["gpt_cond_latent"], self.voices[f"{user.user_token}"]["speaker_embedding"] = self.tts.get_conditioning_latents(voice_config.file_path)
        if self.debug:
            print("Pre-computed voice configurations created successfully!")

    def SynthesizeStream(self, request_iterator, context):
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
            if self.debug:
                print(f"Loaded voice configuration for user_token {user_token}: {voice_config}")
            
            # Establish a connection to the normalizer service
            with grpc.insecure_channel(f'{NORMALIZER_IPADDRESS}:{NORMALIZER_PORT}') as channel:
                normalizer_stub = normalizer_pb2_grpc.NormalizerServiceStub(channel)

                # Normalize each text segment
                for request in request_iterator:
                    if not context.is_active():
                        break

                    # Send text to the normalizer
                    normalize_request = normalizer_pb2.NormalizeRequest(text=request.text)
                    normalize_response = normalizer_stub.Normalize(normalize_request)
                    normalized_text = normalize_response.normalized_text

                text = normalized_text
                if self.debug:
                    print(f"Client {user_token} requested synthesis for: {text}")

                if self.pre_compute:
                    audio = self.tts.generate_audio(text, voice_path=voice_config.file_path, gpt_cond_latent=self.voices[f"{user_token}"]["gpt_cond_latent"], speaker_embedding=self.voices[f"{user_token}"]["speaker_embedding"])
                else:
                    audio = self.tts.generate_audio(text, voice_path=voice_config.file_path)
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

    def AddUser(self, request, context):
        try:
            new_user = models.User(user_token=request.user_token, username=request.username)
            self.db_session.add(new_user)
            self.db_session.commit()
            return tts_pb2.AddUserResponse(status="User added successfully")
        except Exception as e:
            self.db_session.rollback()
            context.set_details(f"Error adding user: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return tts_pb2.AddUserResponse(status="Error adding user")
    
    def RemoveUser(self, request, context):
        try:
            user = self.db_session.query(models.User).filter_by(user_token=request.user_token).first()
            if not user:
                return tts_pb2.RemoveUserResponse(status="User not found")
            
            self.db_session.delete(user)
            self.db_session.commit()
            return tts_pb2.RemoveUserResponse(status="User removed successfully")
        except Exception as e:
            self.db_session.rollback()
            return tts_pb2.RemoveUserResponse(status=f"Error removing user: {e}")
    
    def AddVoice(self, request_iterator, context):
        try:
            voice_name = None  # Name provided by the client
            audio_data = bytearray()  # Buffer to store the audio sent by the client
    
            # Process the stream to collect the name and audio data
            for request in request_iterator:
                if not voice_name:
                    # The voice name is expected in the first request
                    voice_name = request.voice_name.strip().decode('utf-8')  # Decode bytes back to string
                    if not voice_name:
                        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                        context.set_details("Invalid or missing voice name.")
                        return tts_pb2.AddVoiceResponse(status="Failure")
                
                audio_data.extend(request.audio_chunk)  # Collect audio chunks
            
            # Ensure audio data was received
            if not audio_data:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("No audio data received.")
                return tts_pb2.AddVoiceResponse(status="Failure")
            
            # Sanitize the voice name to avoid filesystem issues
            sanitized_name = "".join(c for c in voice_name if c.isalnum() or c in " _-").strip()
            if not sanitized_name:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Voice name contains only invalid characters.")
                return tts_pb2.AddVoiceResponse(status="Failure")
            
            # Generate the full path to save the file
            file_name = f"{sanitized_name}.wav"
            file_path = os.path.join(self.storage_dir, file_name)
    
            # Save the audio file
            with open(file_path, 'wb') as f:
                f.write(audio_data)
    
            # Save to the database
            new_voice = models.Voice(voice_name=sanitized_name, file_path=file_path)
            self.db_session.add(new_voice)
            self.db_session.commit()
    
            if self.debug:
                print(f"Voice added successfully: {sanitized_name} at {file_path}")
    
            return tts_pb2.AddVoiceResponse(status="Success")
        
        except Exception as e:
            self.db_session.rollback()
            print(f"Error adding voice: {e}")
            traceback.print_exc()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return tts_pb2.AddVoiceResponse(status="Failure")
    

    def RemoveVoice(self, request, context):
        try:
            voice = self.db_session.query(models.Voice).filter_by(id=request.voice_id).first()
            if not voice:
                return tts_pb2.RemoveVoiceResponse(status="Voice not found")
            
            self.db_session.delete(voice)
            self.db_session.commit()
            return tts_pb2.RemoveVoiceResponse(status="Voice removed successfully")
        except Exception as e:
            self.db_session.rollback()
            return tts_pb2.RemoveVoiceResponse(status=f"Error removing voice: {e}")
    
    def AssociateUserVoice(self, request, context):
        try:
            user = self.db_session.query(models.User).filter_by(user_token=request.user_token).first()
            voice = self.db_session.query(models.Voice).filter_by(id=request.voice_id).first()
            
            if not user or not voice:
                return tts_pb2.AssociateUserVoiceResponse(status="User or Voice not found")
            
            user.voices.append(voice)
            self.db_session.commit()
            return tts_pb2.AssociateUserVoiceResponse(status="Association created successfully")
        except Exception as e:
            self.db_session.rollback()
            return tts_pb2.AssociateUserVoiceResponse(status=f"Error associating user and voice: {e}")
    
    def RemoveUserVoiceAssociation(self, request, context):
        try:
            user = self.db_session.query(models.User).filter_by(user_token=request.user_token).first()
            voice = self.db_session.query(models.Voice).filter_by(id=request.voice_id).first()
            
            if not user or not voice or voice not in user.voices:
                return tts_pb2.RemoveUserVoiceAssociationResponse(status="Association not found")
            
            user.voices.remove(voice)
            self.db_session.commit()
            return tts_pb2.RemoveUserVoiceAssociationResponse(status="Association removed successfully")
        except Exception as e:
            self.db_session.rollback()
            return tts_pb2.RemoveUserVoiceAssociationResponse(status=f"Error removing association: {e}")


def serve(args):
    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    tts_pb2_grpc.add_TTSServiceServicer_to_server(TTSService(args), server)
    server.add_insecure_port('[::]:{}'.format(SERVER_PORT))
    print("TTS server running on port {}...".format(SERVER_PORT))
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument('configuration_file', nargs='?' , type=str, default="config/intlex_config.json", help="Path to the configuration file for the TTS model")
    parser.add_argument('-p', '--pre_compute', action='store_true', help="Pre-compute voice configurations")
    parser.add_argument('-d',"--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    serve(args)
