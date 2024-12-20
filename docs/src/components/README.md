# System Components

In this section, we will discuss the system components, how they function, and how they interact with each other.

## Components

- [Intlex Module](./app_standalone.md)
- [Frontend](./app.md)
- [API](./app_api.md)
- [Client](./app_client.md)
- [Proxy](./app_proxy.md)
- [Server](./app_server.md)
- [Normalizer](./app_normalizer.md)

## Communication

The components communicate with each other in the following ways:

- With the use of GRPC's:
  - `API` <---> `Proxy`
  - `Client` <---> `Proxy`
  - `Proxy` <---> `Server`
  - `Server` <---> `Normalizer`
- With the use of HTTP Requests and Responses:
  - `Frontend` <---> `API`
