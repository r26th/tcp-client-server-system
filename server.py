# server.py
import socket
import threading

HOST = "192.168.8.122"   
PORT = 5000        

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    print(f"[DISCONNECTED] {addr} closed the socket.")
                    break
                message = data.decode().strip()
                if message.lower() == "exit":
                    conn.sendall("Closing connection. Bye!".encode())
                    print(f"[CLOSE REQUEST] from {addr}")
                    break

                
                parts = message.split()
                if len(parts) != 2:
                    conn.sendall("ERROR: Send exactly two Numbers: <base> <exponent>".encode())
                    continue

                try:
                    base = float(parts[0])
                    exponent = float(parts[1])
                except ValueError:
                    conn.sendall("ERROR: base and exponent must be Numbers.".encode())
                    continue

                
                try:
                    result = pow(base, exponent)  # efficient built-in (big ints supported)
                except OverflowError:
                    conn.sendall("ERROR: result too large to compute.".encode())
                    continue

                reply = str(result)
                conn.sendall(reply.encode())
                print(f"[REQUEST] {addr} -> {base}^{exponent} = (sent result, {len(reply)} bytes)")
            except ConnectionResetError:
                print(f"[CONNECTION RESET] {addr}")
                break
            except Exception as e:
                print(f"[ERROR] {addr} : {e}")
                break

    print(f"[END] connection with {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

if __name__ == "__main__":
    start_server()
