import sys
import random
import socket

from wordlist import WORDS


def build_word_packets():
    word_packets = bytearray()
    words = random.sample(WORDS, random.randint(1, 10))
    for word in words:
        word_bytes = word.encode()
        word_len = len(word_bytes).to_bytes(2, "big")

        word_packets += word_len + word_bytes

    return word_packets, words


def server(port=12345):
    with socket.socket() as s:
        s.bind(("", port))
        s.listen()

        print(f"Listening on port {port}...")

        while True:
            word_packets, word_list = build_word_packets()
            new_s, addr = s.accept()
            with new_s:
                print(f"Received a connection from {addr}")
                new_s.sendall(word_packets)
                print(f"Sent {len(word_list)} word{'s' if len(word_list) > 1 else ''}: {word_list}")


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 12345
    server(port)
