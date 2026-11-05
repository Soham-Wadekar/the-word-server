# The Word Server

A Python-based TCP client-server project that demonstrates how to implement application-level message framing over a TCP byte stream.

The server generates a random collection of words and transmits them as binary packets. The client reconstructs individual packets from the incoming byte stream, even when packets arrive fragmented across multiple socket reads or multiple packets arrive in a single read.

This project explores fundamental networking concepts such as TCP stream communication, binary encoding, byte buffering, and packet parsing.

## Features

- **TCP Communication:** Establishes a connection between a Python TCP server and client using sockets.
- **Binary Packet Encoding:** Encodes words into binary packets using a 2-byte big-endian length header.
- **Variable-Length Messages:** Supports words of different lengths, including words up to 65,535 bytes.
- **Stream Reassembly:** Accumulates incoming data in a buffer to reconstruct complete packets.
- **Packet Extraction:** Identifies and extracts individual packets from a continuous TCP byte stream.
- **UTF-8 Decoding:** Converts received binary payloads back into readable strings.
- **Configurable Receive Size:** Handles different socket receive sizes without relying on TCP message boundaries.

## Packet Format

Each word is transmitted as an individual packet with the following structure:

| Field | Size | Description |
|---|---:|---|
| Length Header | 2 bytes | Word length in bytes (big-endian) |
| Payload | N bytes | UTF-8 encoded word |

For example, the word `hello` is represented as:

```text
00 05 68 65 6c 6c 6f
```

Where:

- `00 05` represents the length of the word (5 bytes).
- `68 65 6c 6c 6f` represents the UTF-8 encoded word (`hello`).

Multiple word packets are concatenated into a continuous byte stream:

```text
[Length][Word][Length][Word][Length][Word]...
```

No additional delimiters are required because each packet contains its own length header.

## Project Structure

```text
the-word-server/
│
├── wordserver.py    # TCP server and binary packet generation
├── wordclient.py    # TCP client and packet parsing
├── wordlist.py      # Collection of words used by the server
└── README.md
```

## Getting Started

### Requirements

- Python 3.8+
- No third-party dependencies

### Running the Server

Open a terminal and execute:

```bash
python wordserver.py
```

The server starts listening on port `12345` by default.

```text
Listening on port 12345...
```

### Running the Client

Open another terminal and execute:

```bash
python wordclient.py
```

To specify a different server address or port:

```bash
python wordclient.py localhost 12345
```

The client connects to the server and prints the received words.

Example output:

```text
Received the following words from the server:
network, protocol, socket, python, packet
```

The actual words and their count are randomly generated for each connection.

## How It Works

### 1. Server: Packet Generation

The server selects between 1 and 10 unique random words from the word list.

Each word is:
1. Encoded into UTF-8 bytes.
2. Prefixed with its length, represented as a 2-byte big-endian integer.
3. Appended to the outgoing byte stream.

The resulting stream is transmitted using `socket.sendall()`.

### 2. Client: Packet Buffering

TCP provides a continuous, ordered stream of bytes rather than individual application-level messages.

Consequently, a single `recv()` call is not guaranteed to return an entire packet.

The client maintains a byte buffer and accumulates incoming data until a complete packet is available.

### 3. Client: Packet Extraction

The `get_next_word_packet()` function:

1. Checks whether the buffer contains the 2-byte length header.
2. Decodes the header to determine the payload length.
3. Calculates the total packet size.
4. Checks whether the complete packet is available.
5. Extracts the packet and removes its bytes from the buffer.
6. Preserves any remaining bytes for subsequent packets.

If the buffer does not contain a complete packet, the client receives more data.

### 4. Client: Payload Decoding

The `extract_word()` function removes the 2-byte header and decodes the remaining payload using UTF-8.

## Learning Objectives

This project explores several fundamental networking concepts:

- TCP sockets and connection management.
- Difference between TCP streams and application-level messages.
- Binary data representation and byte encoding.
- Big-endian integer representation.
- Variable-length packet formats.
- Buffer management and stream reassembly.
- Handling partial reads and multiple packets in a single read.
- UTF-8 encoding and decoding.

## Testing

The client uses a configurable `RECV_SIZE` variable to control the number of bytes requested per socket read.

Experiment with different values:

```python
RECV_SIZE = 1
RECV_SIZE = 2
RECV_SIZE = 5
RECV_SIZE = 4096
```

The client should correctly reconstruct all packets regardless of the receive size.

Additional testing can be performed using words of varying lengths, including the maximum supported length of 65,535 bytes.

## Acknowledgements

This project was developed as a hands-on networking exercise inspired by the socket programming concepts covered in [Beej's Guide to Network Concepts](https://beej.us/guide/bgnet0/).

---

**Built with Python and TCP sockets.**