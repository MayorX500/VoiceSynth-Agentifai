import os
import sys
import threading
import grpc
import argparse as ap
import json
from concurrent import futures

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file

## Load the proxy port from the environment variables
PROXY_SERVER_PORT = os.getenv("PROXY_SERVER_PORT")
if PROXY_SERVER_PORT is None:
    PROXY_SERVER_PORT = 50052 # Default port if not specified as an environment variable

PROXY_SERVER_CONFIG = os.getenv("PROXY_SERVER_CONFIG")
if PROXY_SERVER_CONFIG is None:
    PROXY_SERVER_CONFIG = "config/proxy_config.json" # Default configuration file if not specified as an environment variable

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpcs'))) # Add the grpcs directory to the system path
from grpcs import tts_pb2, tts_pb2_grpc

# Start the health check loop
import time, traceback
def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            traceback.print_exc()
        # in production code you might want to have this instead of course:
        # logger.exception("Problem while executing repetitive task.")
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay

class TTSProxy(tts_pb2_grpc.TTSServiceServicer):
    def __init__(self, args):
        # Load the configuration file
        self.config = self.load_config(args.config_file)
        # The address of the backend TTS servers
        self.peers = self.get_backend()
        self.debug = args.debug
        self.timeout = self.config["heartbeatTimeout"]
        self.healthcheck_interval = self.config["heartbeatInterval"]
        self.server_address = self.get_server()
        # Start the heartbeat check in a separate thread
        self.start_healthcheck_thread()

    def load_config(self, config_file):
        """Load the configuration file."""
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading configuration file: {e}")
            sys.exit(1)
        return config
    
    def get_backend(self):
        """Get the addresses of the backend TTS servers."""

        def check(host,port,timeout=2):
            import socket
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
            sock.settimeout(timeout)
            try:
                sock.connect((host,port))
            except:
                return False
            else:
                sock.close()
                return True
        self.check = check # for pinging the servers every X seconds (configurable)
        peers = {}
        for server in self.config["servers"]:
            server_name = server["name"]
            server_priority = server["priority"]
            server_address = server["address"]
            server_port = server["port"]
            peers[server_name] = {"up":check(server['address'],int(server['port'])), "priority":server_priority, "address":server_address, "port":server_port}
        return peers
    
    def get_server(self):
        """Get the address of the backend TTS server with the highest priority if 'up'."""
        servers = [server for server in self.peers if self.peers[server]["up"]]
        if not servers:
            return None
        server = min(servers, key=lambda x: self.peers[x]["priority"]) # Get the server with the highest priority inverse (lower is better)
        return f'{self.peers[server]["address"]}:{self.peers[server]["port"]}'
    
    def heartbeat(self):
        """Check the health of the backend TTS servers."""
        for server in self.peers:
            self.peers[server]["up"] = self.check(self.peers[server]['address'],int(self.peers[server]['port']))
        self.server_address = self.get_server()
        if self.debug:
            self.print_status()

    def print_status(self):
        """ Print the status of the proxy server and the backend TTS servers."""
        print(f"Server address: {self.server_address}")
        for server in self.peers:
            print(f"{server}: {'UP' if self.peers[server]['up'] else 'DOWN'}")

    def start_healthcheck_thread(self):
        """Start a thread to periodically call the heartbeat function."""
        healthcheck_thread = threading.Thread(target=every, args=(self.healthcheck_interval, self.heartbeat), daemon=True)
        healthcheck_thread.start()


    def SynthesizeStream(self, request_iterator, context):
        # Create a channel to the backend TTS server
        with grpc.insecure_channel(self.server_address) as channel:
            stub = tts_pb2_grpc.TTSServiceStub(channel)

            # Get the client metadata
            client_metadata = dict(context.invocation_metadata())
            user_token = client_metadata.get("user_token", None)
            if not user_token:
                context.set_details("User token not provided")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return

            # Forward the request to the TTS server with the same metadata
            try:
                if self.debug:
                    print(f"Forwarding request to {self.server_address}")
                response_iterator = stub.SynthesizeStream(request_iterator, metadata=context.invocation_metadata())
                for response in response_iterator:
                    yield response

            except grpc.RpcError as e:
                print(f"gRPC error: {e.code()} - {e.details()}")
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INTERNAL)
                return
            
    def AddUser(self, request, context):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = tts_pb2_grpc.TTSServiceStub(channel)
            try:
                if self.debug:
                    print(f"Forwarding AddUser request to {self.server_address}")
                response = stub.AddUser(request, metadata=context.invocation_metadata())
                return response
            except grpc.RpcError as e:
                print(f"gRPC error: {e.code()} - {e.details()}")
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INTERNAL)
                return

    def RemoveUser(self, request, context):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = tts_pb2_grpc.TTSServiceStub(channel)
            try:
                if self.debug:
                    print(f"Forwarding RemoveUser request to {self.server_address}")
                response = stub.RemoveUser(request, metadata=context.invocation_metadata())
                return response
            except grpc.RpcError as e:
                print(f"gRPC error: {e.code()} - {e.details()}")
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INTERNAL)
                return

    def AddVoice(self, request, context):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = tts_pb2_grpc.TTSServiceStub(channel)
            try:
                if self.debug:
                    print(f"Forwarding AddVoice request to {self.server_address}")
                response = stub.AddVoice(request, metadata=context.invocation_metadata())
                return response
            except grpc.RpcError as e:
                print(f"gRPC error: {e.code()} - {e.details()}")
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INTERNAL)
                return

    def RemoveVoice(self, request, context):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = tts_pb2_grpc.TTSServiceStub(channel)
            try:
                if self.debug:
                    print(f"Forwarding RemoveVoice request to {self.server_address}")
                response = stub.RemoveVoice(request, metadata=context.invocation_metadata())
                return response
            except grpc.RpcError as e:
                print(f"gRPC error: {e.code()} - {e.details()}")
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INTERNAL)
                return

    def AssociateUserVoice(self, request, context):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = tts_pb2_grpc.TTSServiceStub(channel)
            try:
                if self.debug:
                    print(f"Forwarding AssociateUserVoice request to {self.server_address}")
                response = stub.AssociateUserVoice(request, metadata=context.invocation_metadata())
                return response
            except grpc.RpcError as e:
                print(f"gRPC error: {e.code()} - {e.details()}")
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INTERNAL)
                return

    def RemoveUserVoiceAssociation(self, request, context):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = tts_pb2_grpc.TTSServiceStub(channel)
            try:
                if self.debug:
                    print(f"Forwarding RemoveUserVoiceAssociation request to {self.server_address}")
                response = stub.RemoveUserVoiceAssociation(request, metadata=context.invocation_metadata())
                return response
            except grpc.RpcError as e:
                print(f"gRPC error: {e.code()} - {e.details()}")
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INTERNAL)
                return

def serve(args):
    if args.config_file is None:
        args.config_file = PROXY_SERVER_CONFIG
    # The address where this proxy server will listen
    proxy_address = f'[::]:{PROXY_SERVER_PORT}'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    tts_pb2_grpc.add_TTSServiceServicer_to_server(TTSProxy(args), server)
    server.add_insecure_port(proxy_address)
    print(f"Proxy server running on port {PROXY_SERVER_PORT}...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("config_file", type=str, help="Path to the configuration file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode", default=False)
    args = parser.parse_args()
    serve(args)
