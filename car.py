import socket
import threading

HEADER = 64
PORT = 5050  # Port for server to run on
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

# Uses DNS Query to get current IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("192.168.86.29", 80))
SERVER = s.getsockname()[0]
s.close()

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f'[{addr}] {msg}')
    conn.close()


def start():
    print(f'[LISTENING] Server is listening on {SERVER}')
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


print("[STARTING] Server is starting...")
start()