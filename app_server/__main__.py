from concurrent import futures
import grpc
import tts_pb2
import tts_pb2_grpc
from intlex import Model
import numpy as np
import traceback
import argparse as ap

class TTSService(tts_pb2_grpc.TTSServiceServicer):
    def __init__(self):
        print("Loading TTS model...")
        self.tts = Model("config/intlex_config.json")
        self.tts.get_conditioning_latents()
        self.tts.tts = self.tts.generate_audio
        print("TTS model loaded successfully!")
        
    def SynthesizeStream(self, request_iterator, context, debug=False):
        chunk_index = 0
        block_size = 8192  # Larger block size for efficiency
        
        # Retrieve client metadata
        client_metadata = dict(context.invocation_metadata())
        session_id = client_metadata.get("session_id", "unknown")
        if debug:
            print(f"Handling request for client session: {session_id}")

        try:
            for request in request_iterator:
                if not context.is_active():
                    if debug:
                        print(f"Client {session_id} disconnected. Ending stream.")
                    break
                
                text = request.text
                if debug:
                    print(f"Client {session_id} requested synthesis for: {text}")

                audio = self.tts.tts(text)
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
            print(f"Error processing client {session_id}: {e}")
            traceback.print_exc()
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

def serve(args):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))  # High concurrency
    tts_pb2_grpc.add_TTSServiceServicer_to_server(TTSService(), server)
    server.add_insecure_port('[::]:50051')
    if args.debug:
        print("TTS server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument('-d',"--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    serve(args)
