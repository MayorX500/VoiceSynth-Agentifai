import grpc
import wave
import tts_pb2
import tts_pb2_grpc
import os
import os.path
import itertools

def save_audio_to_file(audio_data, output_dir, filename, sample_rate=22050):
    """Save audio data as a valid WAV file."""
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    filepath = os.path.join(output_dir, filename)
    try:
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(1)  # Mono audio
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(sample_rate)  # Sample rate
            wf.writeframes(audio_data)
        print(f"Audio saved to '{filepath}'")
    except Exception as e:
        print(f"Error saving audio: {e}")

def stream_audio_to_file(stub, text, pid, request_counter, sample_rate=22050):
    """Receives streamed audio from the gRPC server and saves it to a file."""
    request = tts_pb2.SynthesisRequest(text=text)
    request_stream = iter([request])  # Convert the single request into an iterator

    output_dir = str(pid)  # Directory named after the PID
    filename = f"{pid}-{request_counter}.wav"  # Audio file named as 'pid-N.wav'

    print(f"Streaming audio for text '{text}' and saving to '{output_dir}/{filename}'...")
    audio_data = bytearray()

    try:
        metadata = [("session_id", str(pid))]  # Send PID as session metadata
        response_stream = stub.SynthesizeStream(request_stream, metadata=metadata)

        for response in response_stream:
            audio_data.extend(response.audio_chunk)  # Collect chunks of audio data
            print(f"Received chunk {response.chunk_index}")

    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")
        return

    # Save the received audio data to the appropriate directory and file
    save_audio_to_file(audio_data, output_dir=output_dir, filename=filename, sample_rate=sample_rate)

def main():
    pid = os.getpid()  # Get the process ID
    request_counter = itertools.count(1)  # Counter for audio requests (starts from 1)

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = tts_pb2_grpc.TTSServiceStub(channel)
        while True:
            text = input("Enter text to synthesize (or type 'exit' to quit): ")
            if text.lower() == "exit":
                break
            request_num = next(request_counter)  # Get the next request number
            stream_audio_to_file(stub, text, pid, request_num)

if __name__ == "__main__":
    main()
