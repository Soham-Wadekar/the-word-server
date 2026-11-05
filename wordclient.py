import sys
import socket

packet_buffer = bytearray()
RECV_SIZE = 5


def get_next_word_packet(s):
    while True:
        if len(packet_buffer) >= 2:
            word_length = int.from_bytes(packet_buffer[:2], "big")
            packet_length = 2 + word_length

            if len(packet_buffer) >= packet_length:
                packet = bytes(packet_buffer[:packet_length])
                del packet_buffer[:packet_length]
                return packet

        data = s.recv(RECV_SIZE)

        if not data:
            if packet_buffer:
                raise ConnectionError("Incomplete package received")
            return None

        packet_buffer.extend(data)


def extract_word(packet):
    return packet[2:].decode()


def client(domain="localhost", port=12345):
    with socket.socket() as s:
        s.connect((domain, int(port)))

        print("Received the following words from the server:")
        while True:
            packet = get_next_word_packet(s)

            if packet is None:
                break

            word = extract_word(packet)
            print(word, end="\t")


if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else 12345
    client(domain, port)
