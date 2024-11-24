# This file is used to import the necessary functions and classes from the app_client module
from client import stream_audio_to_file
from tts_pb2_grpc import TTSServiceStub

__all__ = ["stream_audio_to_file", "TTSServiceStub"]

