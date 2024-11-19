import grpc
import wave
import tts_pb2
import tts_pb2_grpc

def save_audio_to_file(audio_data, filename="output.wav", sample_rate=22050):
    """Save audio data as a valid WAV file."""
    try:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # Mono audio
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(sample_rate)  # Sample rate
            wf.writeframes(audio_data)
        print(f"Audio saved to '{filename}'")
    except Exception as e:
        print(f"Error saving audio: {e}")

def stream_audio_to_file(stub, text, output_file="output.wav"):
    """Receives streamed audio from the gRPC server and saves it to a file."""
    request = tts_pb2.SynthesisRequest(text=text)
    request_stream = iter([request])  # Convert the single request into an iterator

    print("Streaming audio and saving to file...")
    audio_data = bytearray()

    try:
        for response in stub.SynthesizeStream(request_stream):
            audio_data.extend(response.audio_chunk)  # Collect chunks of audio data
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")
        return

    # Save the received audio data to a file
    save_audio_to_file(audio_data, filename=output_file)

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = tts_pb2_grpc.TTSServiceStub(channel)
        while True:
            text = input("Enter text to synthesize (or type 'exit' to quit): ")
            if text.lower() == "exit":
                break
            output_file = "output.wav"  # Default output filename
            stream_audio_to_file(stub, text, output_file=output_file)

if __name__ == "__main__":
    main()
