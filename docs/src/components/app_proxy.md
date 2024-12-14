## Proxy

The Proxy is the intermediary between the clients and the Server. It receives requests from the clients, forwards them to the available server, and returns the responses to the respective client.

The proxy also handles the load balancing and availability of the servers. It keeps track of the available servers and distributes the requests among them based on their load.

### Functionality

The Proxy provides the following functionality:

- **Request forwarding**: The Proxy receives requests from the clients and forwards them to the available servers.

- **Response routing**: The Proxy receives responses from the servers and routes them back to the respective clients.

- **Server Availability**: The Proxy keeps track of the available servers and distributes the requests among them based on their load.

### Implementation

The Proxy is implemented as a gRPC server in Python. It listens for requests from the clients, forwards them to the available servers, and returns the responses to the clients.

The Proxy uses the `grpc` library to communicate with the clients and servers using gRPC. It maintains a list of available servers and their load status to distribute the requests efficiently.

The Proxy is a standalone component that can be run on any machine with Python installed. It requires only the `grpc` module/folder to be present in the same directory.

### Requirements

The Proxy requires the following dependencies:

- Python 3.12 or higher
- [Python packages](../../../enviroments/proxy_requirements.txt)

### Usage

To run the Proxy, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/ddu72/PI
   ```

2. Define the environment variables:
   ```bash
   export PROXY_SERVER_PORT={proxy_port}
   export PROXY_SERVER_CONFIG={proxy_config}
   ```

3. Install the required packages:
   ```bash
    pip install -r environments/proxy_requirements.txt
    ```
4. Run the Proxy:
    ```bash
     python app_proxy
     ```

5. The Proxy will start listening for requests from the clients and forwarding them to the available servers.

### Arguments

The Proxy accepts the following arguments, some can only be passed as environment variables:

- `PROXY_SERVER_PORT`: The port on which the Proxy server will listen for requests. (Environment Variable)

- `PROXY_SERVER_CONFIG`: The configuration file for the Proxy server. (Environment Variable)

- `-d`, `--debug`: Enable debug mode for the Proxy server. (Optional)

### Configuration

The Proxy server configuration file should be in the following format:

```json
{
    "heartbeatInterval": 10,
    "heartbeatTimeout": 5,
    "servers": [
        {
            "priority": 0,
            "name": "tts@container1",
            "address": "server_container1",
            "port": 50051,
            "load": 0.5
        },
        {
            "priority": 1,
            "name": "tts@container2",
            "address": "server_container2",
            "port": 50051,
            "load": 0.3
        },
        {
            "priority": 2,
            "name": "tts@container3",
            "address": "server_container3",
            "port": 50051,
            "load": 0.2
        }
    ]
}
```
#### Proxy Server Configuration
##### Heartbeat Interval

The `heartbeatInterval` is the time interval in seconds at which the Proxy server will send heartbeat messages to the servers to check their availability.

##### Heartbeat Timeout

The `heartbeatTimeout` is the time in seconds after which the Proxy server will consider a server unavailable if it does not receive a heartbeat message.

##### Servers

The `servers` array contains the list of available servers with the following attributes:
- `priority`: The priority of the server. The Proxy will distribute the requests based on the server's priority.
- `name`: The name of the server.
- `address`: The IP address or hostname of the server.
- `port`: The port on which the server is listening for requests.
- `load`: The current load of the server. The Proxy will distribute the requests based on the server's load.

#### Note

The load balancing is not implemented in the current version of the Proxy. The servers are selected based on their priority only.