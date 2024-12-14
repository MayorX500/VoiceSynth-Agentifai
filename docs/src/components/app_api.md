## API

The API is a RESTful service that provides access to the system's functionality. It is built using [Flask](https://flask.palletsprojects.com/en/stable/installation/#python-version), a Python microframework for web development. The API is responsible for handling requests from the client, processing them by sending them to the proxy, and returning the appropriate response.

### Endpoints

The API has the following endpoint:
- `/api/tts`: This endpoint is used to syntesize text to speech. It accepts a POST request with a JSON payload containing the text to be synthesized and the language to use. The API sends the text to the proxy, which then sends it to the TTS engine. The TTS engine synthesizes the text and returns the audio file, which is then returned to the client.

#### POST `/api/tts`
##### Request
```json
{
    "text": "Hello, how are you?",
    "language": "en"
}
```
##### Response
```json
UklGRvYAAABXQVZFZm10...IBAAAAABAAEAQB8AAEAfAAAA==
```

### Requirements

The API requires the following:
- ENV: The environment variables must be defined in the `.env` file or as environment variables. The following variables must be defined:
    - `PORT`: The port on which the API server will run.
    - `PROXY_SERVER_PORT`: The port on which the proxy server is running.
    - `PROXY_SERVER_ADDRESS`: The address of the proxy server.

- Dependencies: The API requires the following dependencies:
    - [Python requirements](../../../enviroments/api_requirements.txt)


### Usage

To use the API, you need to start the Flask server by doing the following:

1. Define the proxy address and port in the `.env` file or as an environment variable. The serve port can also be defined, just remember to update the frontend `REACT_APP_API_PORT` to the correct one. For example:
    ```bash
    export PORT=5000
    export PROXY_SERVER_PORT=50051
    export PROXY_SERVER_ADDRESS={proxy_address}
    ```
2. Install the required dependencies by running:
    ```bash
    pip install -r enviroments/api_requirements.txt
    ```

3. Start the Flask server by running:
    ```bash
    python app_api
    ```

The API will start running on the specified port, and you can now send requests to it.