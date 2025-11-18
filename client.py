# client.py
import socket
import time

SERVER_IP = "192.168.8.122"   # استبدليها بـ IP جهاز السيرفر داخل LAN
PORT = 5000

def main():
    print("Client started.")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    print(f"Connected to server at {SERVER_IP}:{PORT}")

    try:
        while True:
            user = input("Enter base and exponent (e.g. 2 5), or 'exit' to close: ").strip()
            if not user:
                continue

            # prepare and send
            start = time.perf_counter()
            client.sendall(user.encode())

            # receive
            data = client.recv(65536)  # large buffer size for big results
            end = time.perf_counter()

            if not data:
                print("No response (server may have closed connection).")
                break

            reply = data.decode()
            rtt = end - start
            print(f"Server reply: {reply}")
            print(f"RTT: {rtt:.6f} seconds\n")

            if user.lower() == "exit":
                break

    except KeyboardInterrupt:
        print("\nClient terminated by user.")
    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
