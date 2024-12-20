## Docker

To run the application (Client-side) using Docker, follow the steps below.

### Prerequisites

- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Docker images built (see [How to Install](../installation/docker.md))

### Usage

1. Verify that the Docker images have been built and the "main" services are running:

   ```bash
   docker compose ps
   ```

   **!Note**: The output should be similar to the following:

   ```bash
   PI> docker compose ps
   NAME                   IMAGE                      COMMAND                  SERVICE      CREATED          STATUS          PORTS
   normalizer_container   tts-agentifai:normalizer   "python app_normaliz…"   normalizer   13 seconds ago   Up 12 seconds   50051/tcp
   proxy_container        tts-agentifai:proxy        "python app_proxy -d"    proxy        13 seconds ago   Up 11 seconds   0.0.0.0:50051->50051/tcp, :::50051->50051/tcp
   server_container1      tts-agentifai:server       "python app_server"      server_1     13 seconds ago   Up 12 seconds   50051/tcp
   server_container2      tts-agentifai:server       "python app_server"      server_2     13 seconds ago   Up 12 seconds   50051/tcp
   server_container3      tts-agentifai:server       "python app_server"      server_3     13 seconds ago   Up 12 seconds   50051/tcp
   ```

   **!Note**: The `normalizer_container`, `proxy_container`, and `server_containerX` services should be running.

2. Run endpoints:

   1. Client:

      ```bash
      docker compose run -e PROXY_SERVER_PORT={PROXY_SERVER_PORT} -e PROXY_SERVER_ADDRESS={PROXY_SERVER_ADDRESS} client
      ```

      **!Note**: The `PROXY_SERVER_PORT` and `PROXY_SERVER_ADDRESS` are optional and default to `50051` and `proxy_container`, respectively.

      **!Note**: The client will be available in the opened terminal.

   2. Frontend and API:

      ```bash
      docker compose run frontend
      ```

      **!Note**: The frontend will be available at `http://localhost:3000` and the API will be available at `http://localhost:5000`.

3. The output will be displayed in the terminal.
