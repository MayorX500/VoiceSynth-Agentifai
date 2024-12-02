import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpcs'))) # Add the grpcs directory to the system path

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

## Connection port
CONN_PORT = os.getenv("CONN_PORT")
if not CONN_PORT:
    CONN_PORT = 50051 # Default proxy port if not specified in the environment variables

## IP address
PROXY_ADD = os.getenv("PROXY_ADD")
if not PROXY_ADD:
    PROXY_ADD = "localhost" # Default IP address if not specified in the environment variables

import time
import grpc
import wave
from grpcs import tts_pb2
from grpcs import tts_pb2_grpc
import os
import os.path
import itertools
import argparse as ap
import random

def save_audio_to_file(audio_data, output_dir, filename, sample_rate=22050, debug=False):
    """Save audio data as a valid WAV file."""
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    filepath = os.path.join(output_dir, filename)
    try:
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(1)  # Mono audio
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(sample_rate)  # Sample rate
            wf.writeframes(audio_data)
        if debug:
            print(f"Audio saved to '{filepath}'")
    except Exception as e:
        print(f"Error saving audio: {e}")

def stream_audio_to_file(stub, text, pid, request_counter, user_token, sample_rate=22050,output_dir=None, filename=None, debug=False):
    """Receives streamed audio from the gRPC server and saves it to a file."""
    request = tts_pb2.SynthesisRequest(text=text)
    request_stream = iter([request])  # Convert the single request into an iterator

    if output_dir is None:
        output_dir = str(pid)  # Directory named after the PID
    if filename is None:
        filename = f"{pid}-{request_counter}.wav"  # Audio file named as 'pid-N.wav'

    if debug:
        print(f"Streaming audio for text '{text}' and saving to '{output_dir}/{filename}'...")
    audio_data = bytearray()

    try:
        metadata = [("session_id", str(pid)), ("user_token", user_token)]  # Send user_token as session metadata
        response_stream = stub.SynthesizeStream(request_stream, metadata=metadata)

        for response in response_stream:
            audio_data.extend(response.audio_chunk)  # Collect chunks of audio data
            if debug:
                print(f"Received chunk {response.chunk_index}")

    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")
        return

    # Save the received audio data to the appropriate directory and file
    save_audio_to_file(audio_data, output_dir=output_dir, filename=filename, sample_rate=sample_rate, debug=debug)

def create_user(stub):
    """Create a new user."""
    user_token = input("Enter user token: ")
    username = input("Enter username: ")
    request = tts_pb2.AddUserRequest(user_token=user_token, username=username)
    response = stub.AddUser(request)
    print(response.status)
    
def remove_user(stub):
    """Remove an existing user."""
    user_token = input("Enter user token: ")
    request = tts_pb2.RemoveUserRequest(user_token=user_token)
    response = stub.RemoveUser(request)
    print(response.status)

def add_audio(stub):
    file_path = input("Enter the path of the audio file: ")
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return
    
    voice_name = input("Enter the voice name: ").strip()
    if not voice_name:
        print("Error: Voice name cannot be empty.")
        return

    # Read the entire audio file into memory
    with open(file_path, "rb") as audio_file:
        audio_data = audio_file.read()
        
    try:
        # Send the entire file in a single message
        request = tts_pb2.AddVoiceRequest(voice_name=voice_name, audio_chunk=audio_data)
        response = stub.AddVoice(request)  # Non-streaming gRPC call
        print(f"Resposta do servidor: {response.status}")
    except grpc.RpcError as e:
        print(f"Erro no gRPC: {e.code()} - {e.details()}")



def remove_audio(stub):
    """Remove an audio from the server."""
    voice_id = int(input("Enter the voice ID to remove: "))
    request = tts_pb2.RemoveVoiceRequest(voice_id=voice_id)
    response = stub.RemoveVoice(request)
    print(response.status)

def associate_audio(stub):
    """Associate an audio with a user."""
    user_token = input("Enter user token: ")
    voice_id = int(input("Enter voice ID to associate: "))
    request = tts_pb2.AssociateUserVoiceRequest(user_token=user_token, voice_id=voice_id)
    response = stub.AssociateUserVoice(request)
    print(response.status)

def disassociate_audio(stub):
    """Disassociate an audio from a user."""
    user_token = input("Enter user token: ")
    voice_id = int(input("Enter voice ID to disassociate: "))
    request = tts_pb2.RemoveUserVoiceAssociationRequest(user_token=user_token, voice_id=voice_id)
    response = stub.RemoveUserVoiceAssociation(request)
    print(response.status)

def synthesize_text(stub, user_token, debug=False, output_dir=None, filename=None, text=None):
    """Generate audio from text."""
    if text is None:
        text = input("Enter text to synthesize: ")
    pid = os.getpid()  # Get the process ID
    request_counter = itertools.count(random.randint(1, 100000000))  # Counter for audio requests
    request_num = next(request_counter)
    stream_audio_to_file(stub, text, pid, request_num, user_token, debug=debug, output_dir=output_dir, filename=filename)   

def main(args):
    """
    Client entry point

    This function is the entry point for the client. It receives the IP address of the server and the user token as
    arguments and starts the client.
    """
    user_token = args.user_token
    if args.proxy_add is None:
        args.proxy_add = PROXY_ADD
    running = True
    while running:
        if user_token == "0":
            # Menu para user_token == 0
            print("\nOptions:")
            print("1. Create User")
            print("2. Remove User")
            print("3. Add Audio")
            print("4. Remove Audio")
            print("5. Associate Audio with User")
            print("6. Disassociate Audio from User")
            print("7. Exit")
            choice = input("Select an option (1-5): ")
            with grpc.insecure_channel(f"{args.proxy_add}:{CONN_PORT}") as channel:
                stub = tts_pb2_grpc.TTSServiceStub(channel)
                if choice == "1":
                    create_user(stub)
                elif choice == "2":
                    remove_user(stub)
                elif choice == "3":
                    add_audio(stub)
                elif choice == "4":
                    remove_audio(stub)
                elif choice == "5":
                    associate_audio(stub)
                elif choice == "6":
                    disassociate_audio(stub)
                elif choice == "7":
                    print("Exiting...")
                    running = False
                else:
                    print("Invalid option. Please try again.")
        else:
            # Menu para user_token != 0
            print("\nOptions:")
            print("1. Synthesize Audio")
            print("2. Exit")
            choice = input("Select an option (1-2): ")
            with grpc.insecure_channel(f"{args.proxy_add}:{CONN_PORT}") as channel:
                stub = tts_pb2_grpc.TTSServiceStub(channel)
                if choice == "1":
                    synthesize_text(stub, user_token, debug=args.debug)
                elif choice == "2":
                    print("Exiting...")
                    running = False
                else:
                    print("Invalid option. Please try again.")


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("proxy_add", nargs='?', type=str, help="IP address of the server", default=PROXY_ADD)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode", default=False)
    args = parser.parse_args()
    main(args)
