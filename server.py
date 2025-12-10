# server.py
import socket
import threading

# Define server host and port
HOST = "172.20.10.4"  # IP address of the server
PORT = 5000             # Port number to listen on        

# This function handles communication with the client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")  # Print a message when a new connection is made
    with conn:  # Automatically closes the connection when the block ends
        while True:
            try:
                # Receive data from the client, maximum of 4096 bytes
                data = conn.recv(4096)
                
                # If no data is received (i.e., client disconnected), break the loop
                if not data:
                    print(f"[DISCONNECTED] {addr} closed the socket.")
                    break
                
                # Decode the received data and strip any extra spaces
                message = data.decode().strip()

                # If the client sends the message "exit", close the connection
                if message.lower() == "exit":
                    conn.sendall("Closing connection. Bye!".encode())  # Send confirmation message
                    print(f"[CLOSE REQUEST] from {addr}")
                    break

                # Split the received message into base and exponent parts
                parts = message.split()

                # If there are not exactly two parts, send an error message and continue
                if len(parts) != 2:
                    conn.sendall("ERROR: Send exactly two Numbers: <base> <exponent>".encode())
                    continue

                try:
                    # Convert base and exponent to float
                    base = float(parts[0])
                    exponent = float(parts[1])
                except ValueError:
                    # If conversion fails, send an error message and continue
                    conn.sendall("ERROR: base and exponent must be Numbers.".encode())
                    continue

                try:
                    # Calculate base raised to the power of exponent
                    result = pow(base, exponent)  # Efficient built-in function, supports large numbers (big ints)
                except OverflowError:
                    # If the result is too large to compute, send an error message
                    conn.sendall("ERROR: result too large to compute.".encode())
                    continue

                # Send the result as a string back to the client
                reply = str(result)
                conn.sendall(reply.encode())
                
                # Print the request and result for logging
                print(f"[REQUEST] {addr} -> {base}^{exponent} = (sent result, {len(reply)} bytes)")
            except ConnectionResetError:
                # If the connection is reset by the client, log the error
                print(f"[CONNECTION RESET] {addr}")
                break
            except Exception as e:
                # Catch any other exceptions and log them
                print(f"[ERROR] {addr} : {e}")
                break

    # Print when the connection with the client is ended
    print(f"[END] connection with {addr}")

# This function starts the server and listens for incoming client connections
def start_server():
    # Create a new socket object for the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the server socket to the specified host and port
    server.bind((HOST, PORT))
    
    # Start listening for incoming connections (maximum backlog of 5 connections)
    server.listen()
    print(f"[LISTENING] Server listening on {HOST}:{PORT}")
    
    # Continuously accept incoming client connections
    while True:
        conn, addr = server.accept()  # Accept the new client connection
        # Create a new thread to handle the client connection
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()  # Start the thread
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")  # Print number of active connections

# Main entry point to start the server
if __name__ == "__main__":
    start_server()
