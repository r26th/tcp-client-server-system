# TCP Client-Server System

A Python implementation of a multithreaded TCP client-server system for concurrent communication over a local network. Clients send a base and exponent, the server calculates the result, and the response is returned over the same persistent connection with client-side Round-Trip Time (RTT) measurement.

## Features

- IPv4 TCP communication using Python’s `socket` module.
- Multithreaded server architecture for handling concurrent clients.
- A dedicated server thread for each connected client.
- Persistent connections supporting multiple requests per client.
- Remote exponent calculation using `pow(base, exponent)`.
- Validation for missing, malformed, and non-numeric input.
- Handling of large calculations that raise an `OverflowError`.
- Graceful client disconnection using the `exit` command.
- Client-side RTT measurement using `time.perf_counter()`.

## Project Files

- `server.py` and `client.py` — primary TCP server-client implementation.
- `server3.py` and `client3.py` — an additional LAN-tested configuration with revised connection handling.

Both server-client pairs communicate through TCP port `5000`. The configured IP addresses are local-network addresses and should be updated to match the server device’s current IPv4 address when running the system on another network.

## Requirements

- Python 3
- Two or more devices connected to the same LAN for multi-device testing, or one device for local testing
- No external Python packages are required.

## Configuration

1. Determine the server device’s current IPv4 address.
2. Set `HOST` in the selected server file to that address.
3. Set `SERVER_IP` in the matching client file to the same address.
4. Keep the same `PORT` value in both files.

For same-device testing, both address values can be set to:

```text
127.0.0.1
```

## How to Run

Start the server:

```bash
python server3.py
```

Open separate terminals or use additional devices on the same LAN, then start one or more clients:

```bash
python client3.py
```

Enter calculation requests using the following format:

```text
<base> <exponent>
```

Example:

```text
2 10
```

The client displays the server response and the measured RTT. Enter `exit` to close the connection gracefully.

## Testing

The system was tested over a LAN with the server and clients running on separate machines. The documented test cases cover:

- Integer and floating-point inputs
- Negative values
- Zero and fractional exponents
- Large-number calculations
- Invalid and non-numeric input
- Concurrent client connections
- Server and client execution on the same device

The tests verify request processing, error handling, concurrent communication, connection persistence, and RTT measurement across different input conditions.
