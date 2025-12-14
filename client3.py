import socket
import time

# server IP and port to connect 
SERVER_IP = "192.168.100.168"
PORT = 5000

def main():
    print("Client started.")
    # create TCP socket for IPv4 connection to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((SERVER_IP, PORT))
        print(f"Connected to server at {SERVER_IP}:{PORT}")

        # continuously ask the user for input (keep alive)
        while True:
            # user input:base and exponent or exit 
            user = input("Enter base and exponent numbers in this order: <base> <exponent>, or 'exit' to close: ").strip()
            if not user:
                continue

            try:
                start = time.perf_counter()  # Start calc RTT
                client.sendall(user.encode()) # send input to server

                # Receive result from server
                data = client.recv(65536)
                end = time.perf_counter()  # End calc RTT

            except ConnectionResetError:
                print("\n[ERROR] server close the connection")
                break

            if not data:
                print("No response (server may close connection)")
                break

            reply = data.decode()
            RTT = end - start  # Calc RTT
            print(f"Server reply: {reply}")
            print(f"RTT: {RTT:.6f} seconds\n")

            if user.lower() == "exit":
                break

    except Exception as e:
        print(f"\n[ERROR] error occurred: {e}")
        client.close()
        print("Connection closed")

      
if __name__ == "__main__":
    main()
    