import socket
import threading

# Simple peer-to-peer chat: one user runs as server, the other as client
# Usage: Run on both computers. One chooses 'server', the other 'client'.

HOST = input("Enter your friend's IP (or leave blank to host): ").strip()
PORT = 4000

if HOST == '':
    # Act as server
    print(f"[SERVER] Waiting for connection on port {PORT}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", PORT))
    s.listen(1)
    conn, addr = s.accept()
    print(f"[SERVER] Connected by {addr}")
    sock = conn
else:
    # Act as client
    print(f"[CLIENT] Connecting to {HOST}:{PORT}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"[CLIENT] Connected!")

def receive():
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[INFO] Connection closed.")
                break
            print(f"\nFriend: {data.decode()}\nYou: ", end="", flush=True)
        except:
            break

def send():
    while True:
        try:
            msg = input("You: ")
            sock.sendall(msg.encode())
        except:
            break

recv_thread = threading.Thread(target=receive, daemon=True)
send_thread = threading.Thread(target=send, daemon=True)
recv_thread.start()
send_thread.start()
recv_thread.join()
send_thread.join()
sock.close()
