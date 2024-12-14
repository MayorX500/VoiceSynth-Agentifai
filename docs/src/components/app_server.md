## Server

The Server is responsible for processing the requests from the Proxy and returning the responses. The Server is a GRPC server that listens for requests from the Proxy and processes them. The Server is also responsible for communicating with the Normalizer to process the requests.

### Implementation

The Server is implemented as a GRPC server in Python. It listens for requests from the Proxy, processes them, and returns the responses. The Server uses the `grpc` library to communicate with the Proxy using GRPC. It also communicates with the Normalizer to process the requests.

The Server also uses a database to store user data and other information. It uses the `sqlite3` library to interact with the database and store the data.
