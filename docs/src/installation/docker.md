## Docker

For ease of use, we have provided a Dockerfile that contains all the necessary dependencies to run the application. This is the recommended way to run the application.

### Prerequisites

- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ddu72/PI
   ```

2. Change to the project directory:

   ```bash
   cd PI
   ```

3. Build the Docker image:

   ```bash
   docker-compose build
   ```

4. Start the target services:

   ```bash
   docker-compose up [proxy, server, api, normalizer] -d
   ```

   **!Note**: The `-d` flag is optional and runs the services in detached mode.

   **!Note**: The each service will start its dependencies automatically, for example, the `proxy` service will start all the `server` services and the `server` service will start the `normalizer` service.

The services are now running and ready to be used. See [How to Use](../usage/docker.md) for more information.

### Stopping the Services

To stop the services, run the following command:

```bash
docker-compose down
```

### Removing the Docker Image

To remove the Docker image, run the following command:

```bash
docker-compose down --rmi all
```

