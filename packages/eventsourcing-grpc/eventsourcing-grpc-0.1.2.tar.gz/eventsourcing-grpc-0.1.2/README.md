# Event Sourcing with gRPC

This is an extension for [the Python eventsourcing library](https://github.com/pyeventsourcing/eventsourcing).

This package provides a gRPC server class that runs event-sourced applications
in a gRPC server. A gRPC client class can be used to interact with the application
server. Application command and query methods can be called, and
notifications selected, remotely using an application proxy object
provided by the client.

This package also provides a system runner class, with the same interface as the Runner
classes in the core eventsourcing library. It can run a system of event-sourced
applications as a set of gRPC servers. Leader and follower connections, for prompting
and pulling event notifications, are implemented with gRPC clients.

This package provides console commands that can be used to start servers and run systems
from a command line interface.

This package also provides an example of running an event-sourced application in
gRPC server in a Docker container.

This package also provides an example of running a system of applications
in gRPC servers in Docker containers with docker-compose.

This package also provides an example of running a system of applications
in gRPC servers in Docker containers with Kubernetes, with clients and
servers authenticated with SSL/TLS PKI certificates.

## Installation

Use pip to install the [stable distribution](https://pypi.org/project/eventsourcing-grpc/)
from the Python Package Index.

    $ pip install eventsourcing_grpc

It is recommended to install Python packages into a Python virtual environment.


## gRPC clients and servers

The `GrpcApplicationServer` class can be used to run an event-sourced
application as a gRPC server, and the `GrpcApplicationClient` class can
be used to connect to a server.

Define an event-sourced application.

```python
from eventsourcing_grpc.example import Orders
```

Configure with environment variables.

```python
import os

os.environ["ORDERS_GRPC_SERVER_ADDRESS"] = "localhost:50051"
```

Application persistence can be configured in the usual way (see core library docs).

Use the `start_server()` function to create and start a gRPC application server.

```python
from eventsourcing_grpc.application_server import start_server

server = start_server(Orders)
```

Use the `connect()` function to create a gRPC client and connect to the server.

```python
from eventsourcing_grpc.application_client import connect

client = connect(Orders, max_attempts=10)
```

Use the application proxy to call command and query methods on the application server.

```python
# Create order.
order_id = client.app.create_new_order()

# Get order.
order = client.app.get_order(order_id)
assert order["id"] == order_id
assert order["is_reserved"] == False
assert order["is_paid"] == False
```

Use the application proxy to select event notifications.

```python
notifications = client.app.notification_log.select(start=1, limit=10)
assert len(notifications) == 1
assert notifications[0].id == 1
assert notifications[0].originator_id == order_id
assert notifications[0].originator_version == 1
assert notifications[0].topic == "eventsourcing_grpc.example:Order.Created"
```

Close client and stop server.

```python
client.close()
server.stop(wait=True)
```


## gRPC runner

The `GrpcRunner` class can be used to run a system of event-sourced applications
as an inter-connected set of gRPC servers.

```python
from eventsourcing_grpc.runner import GrpcRunner
```

Define a system of event-sourced applications.

```python
from eventsourcing_grpc.example import system
```

Configure with environment variables.

```python
import os

os.environ["ORDERS_GRPC_SERVER_ADDRESS"] = "localhost:50051"
os.environ["RESERVATIONS_GRPC_SERVER_ADDRESS"] = "localhost:50052"
os.environ["PAYMENTS_GRPC_SERVER_ADDRESS"] = "localhost:50053"
```

Create and start a gRPC system runner (starts servers and connects clients).

```python

runner = GrpcRunner(system)
runner.start(with_subprocesses=True)
```

Get an application proxy from the runner.

```python
app = runner.get(Orders)
```

Call command and query methods on application proxy.

```python
order1_id = app.create_new_order()

# Wait for the processing to happen.
from time import sleep

for _ in range(100):
    sleep(0.1)
    if app.is_order_paid(order1_id):
        break
    elif runner.has_errored.is_set():
        raise AssertionError("Runner error")
else:
    raise AssertionError("Timeout waiting for order to be paid")

```

Get application's event notifications.

```python
notifications = app.notification_log.select(start=1, limit=10)
assert len(notifications) == 3
assert notifications[0].id == 1
assert notifications[0].originator_id == order1_id
assert notifications[0].originator_version == 1
assert notifications[0].topic == "eventsourcing_grpc.example:Order.Created"
assert notifications[1].id == 2
assert notifications[1].originator_id == order1_id
assert notifications[1].originator_version == 2
assert notifications[1].topic == "eventsourcing_grpc.example:Order.Reserved"
assert notifications[2].id == 3
assert notifications[2].originator_id == order1_id
assert notifications[2].originator_version == 3
assert notifications[2].topic == "eventsourcing_grpc.example:Order.Paid"

```

Stop runner (closes clients and stops servers).

```python
runner.stop()
```

## Start server from command line

The console command `eventsourcing_grpc_server` can be used to start
a gRPC application server. The application topic can be given as a
command line argument.

    $ export ORDERS_GRPC_SERVER_ADDRESS=localhost:50051
    $ eventsourcing_grpc_server eventsourcing_grpc.example:Orders

A system of interconnected application servers can be started in this way,
after setting `SYSTEM_TOPIC` in the environment.

    $ export SYSTEM_TOPIC=eventsourcing_grpc.example:system
    $ export ORDERS_GRPC_SERVER_ADDRESS=localhost:50051
    $ export RESERVATIONS_GRPC_SERVER_ADDRESS=localhost:50052
    $ export PAYMENTS_GRPC_SERVER_ADDRESS=localhost:50053

    $ eventsourcing_grpc_server eventsourcing_grpc.example:Orders &
    $ eventsourcing_grpc_server eventsourcing_grpc.example:Reservations &
    $ eventsourcing_grpc_server eventsourcing_grpc.example:Payments &

In the example above, the servers are run as background processes.

## Start runner from command line

The console command `eventsourcing_grpc_runner` can be used to run a system
of event-sourced applications. Only the system topic must be configured.

The system topic can be given as a command line argument.

    $ eventsourcing_grpc_runner eventsourcing_grpc.example:system

Alternatively, the system topic can be set using the `SYSTEM_TOPIC` environment variable.

    $ export SYSTEM_TOPIC=eventsourcing_grpc.example:system
    $ eventsourcing_grpc_runner

The server addresses will be automatically configured, unless they are set as
environment variables.

## Docker container

A Docker file can be defined to run the `eventsourcing_grpc_server` command
mentioned above, after installing an event-sourced system and the `eventsourcing_grpc`
package.

```dockerfile
FROM python:3.10

WORKDIR /app

# Install package(s).
RUN pip install eventsourcing_grpc

# Run application server.
ENV PYTHONUNBUFFERED = 1
CMD ["eventsourcing_grpc_server"]
```

A container image can then be built with Docker.

    $ docker build -t eventsourcing-grpc -f Dockerfile .

## Docker Compose

A system of gRPC application servers can be run with Docker Compose.
The following Docker Compose file assumes SSL/TLS PKI certificates
have been generated in a local `./ssl` folder.

```
version: '2'

services:
  orders:
    image: "eventsourcing-grpc:v1"
    environment:
      APPLICATION_TOPIC: "eventsourcing_grpc.example:Orders"
      SYSTEM_TOPIC: "eventsourcing_grpc.example:system"
      ORDERS_GRPC_SERVER_ADDRESS: "orders:50051"
      RESERVATIONS_GRPC_SERVER_ADDRESS: "reservations:50052"
      PAYMENTS_GRPC_SERVER_ADDRESS: "payments:50053"
      MAX_PULL_INTERVAL: "10"
      GRPC_SSL_PRIVATE_KEY_PATH: /app/ssl/orders.key
      GRPC_SSL_CERTIFICATE_PATH: /app/ssl/orders.crt
      GRPC_SSL_ROOT_CERTIFICATE_PATH: /app/ssl/root.crt
    volumes:
      - ./ssl/orders:/app/ssl
    ports:
      - "50051:50051"

  reservations:
    image: "eventsourcing-grpc:v1"
    environment:
      APPLICATION_TOPIC: "eventsourcing_grpc.example:Reservations"
      SYSTEM_TOPIC: "eventsourcing_grpc.example:system"
      ORDERS_GRPC_SERVER_ADDRESS: "orders:50051"
      RESERVATIONS_GRPC_SERVER_ADDRESS: "reservations:50052"
      PAYMENTS_GRPC_SERVER_ADDRESS: "payments:50053"
      MAX_PULL_INTERVAL: "10"
      GRPC_SSL_PRIVATE_KEY_PATH: /app/ssl/reservations.key
      GRPC_SSL_CERTIFICATE_PATH: /app/ssl/reservations.crt
      GRPC_SSL_ROOT_CERTIFICATE_PATH: /app/ssl/root.crt
    volumes:
      - ./ssl/reservations:/app/ssl
    ports:
      - "50052:50052"

  payments:
    image: "eventsourcing-grpc:v1"
    environment:
      APPLICATION_TOPIC: "eventsourcing_grpc.example:Payments"
      SYSTEM_TOPIC: "eventsourcing_grpc.example:system"
      ORDERS_GRPC_SERVER_ADDRESS: "orders:50051"
      RESERVATIONS_GRPC_SERVER_ADDRESS: "reservations:50052"
      PAYMENTS_GRPC_SERVER_ADDRESS: "payments:50053"
      MAX_PULL_INTERVAL: "10"
      GRPC_SSL_PRIVATE_KEY_PATH: /app/ssl/payments.key
      GRPC_SSL_CERTIFICATE_PATH: /app/ssl/payments.crt
      GRPC_SSL_ROOT_CERTIFICATE_PATH: /app/ssl/root.crt
    volumes:
      - ./ssl/payments:/app/ssl
    ports:
      - "50053:50053"
```

The containers can then be started.

    $ docker-compose up -d

## Kubernetes

A system of gRPC application servers can be run with Kubernetes.

Create Kubernetes Secrets from the SSL/TLS PKI certificates.

	$ kubectl create secret generic root-ssl-secret \
    --from-file=root.crt=ssl/root/root.crt

	$ kubectl create secret tls orders-ssl-secret \
	--key ./ssl/orders/orders.key \
    --cert ./ssl/orders/orders.crt

	$ kubectl create secret tls reservations-ssl-secret \
	--key ./ssl/reservations/reservations.key \
    --cert ./ssl/reservations/reservations.crt

	$ kubectl create secret tls payments-ssl-secret \
	--key ./ssl/payments/payments.key \
    --cert ./ssl/payments/payments.crt


Create a Kubernetes Deployment for each application.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders
  labels:
    system: orders
spec:
  selector:
    matchLabels:
      app: orders
  replicas: 1
  template:
    metadata:
      labels:
        app: orders
    spec:
      volumes:
      - name: ssl-secret-volume
        secret:
          secretName: orders-ssl-secret
      - name: root-ssl-secret-volume
        secret:
          secretName: root-ssl-secret
      containers:
      - name: orders
        image: "eventsourcing-grpc:latest"
        imagePullPolicy: Never
        ports:
        - containerPort: 50051
        volumeMounts:
          - mountPath: /app/ssl
            name: ssl-secret-volume
          - mountPath: /app/root-ssl
            name: root-ssl-secret-volume
        env:
          - name: APPLICATION_TOPIC
            value: "eventsourcing_grpc.example:Orders"
          - name: SYSTEM_TOPIC
            value: "eventsourcing_grpc.example:system"
          - name: ORDERS_GRPC_SERVER_ADDRESS
            value: "0.0.0.0:50051"
          - name: RESERVATIONS_GRPC_SERVER_ADDRESS
            value: "reservations:50052"
          - name: PAYMENTS_GRPC_SERVER_ADDRESS
            value: "payments:50053"
          - name: GRPC_SSL_PRIVATE_KEY_PATH
            value: /app/ssl/tls.key
          - name: GRPC_SSL_CERTIFICATE_PATH
            value: /app/ssl/tls.crt
          - name: GRPC_SSL_ROOT_CERTIFICATE_PATH
            value: /app/root-ssl/root.crt
```

Create a Kubernetes Service for each Deployment.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders
  labels:
    system: orders
spec:
  selector:
    app: orders
  type: LoadBalancer
  ports:
  - port: 50051
    targetPort: 50051
    protocol: TCP
```

The above configuration will run each application on a separate Pod. Alternatively,
you can run all the applications in the same Pod, by defining a multi-container
Deployment.

Please refer to the project repo (and its GitHub actions workflow and Makefile)
to see a fully working example of running a system of applications with minikube.

## Developers

After cloning the eventsourcing-grpc repository, set up a virtual
environment and install dependencies by running the following command in the
root folder.

    $ make install

The ``make install`` command uses the build tool Poetry to create a dedicated
Python virtual environment for this project, and installs popular development
dependencies such as Black, isort and pytest.

Add tests in `./tests`. Add code in `./eventsourcing_grpc`.

Generate SSL/TLS certificates and private keys for testing.

    $ make ssl

Run tests.

    $ make test

Check the formatting of the code.

    $ make lint

Reformat the code.

    $ make fmt

Add dependencies in `pyproject.toml` and then update installed packages.

    $ make update-packages

If you edit the .proto files, regenerate the project's protos package.

    $ make grpc-stubs
