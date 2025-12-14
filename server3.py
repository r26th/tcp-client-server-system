import socket
import threading

# server host and port
HOST = "192.168.100.168"  
PORT = 5000                    

# handles communication with the client and args here: 
# conn is client socket 
# addr is tuple for client address as (IP, port)
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")  
    with conn:  # close connection if block ends
        while True:
            try:
                # Receive data from client
                data = conn.recv(4096)
                
                # If no data received (as client disconnect without send exit)
                if not data:
                    print(f"[DISCONNECTED] {addr} closed the socket")
                    break
                
                # decode received data and strip white spaces
                message = data.decode().strip()

                # If message is exit: close connection
                if message.lower() == "exit":
                    conn.sendall("Closing connection".encode())  
                    print(f"[CLOSE REQUEST] from {addr}")
                    break

                # Split to base and exponent 
                parts = message.split()

                # If it is not two parts: send error msg
                if len(parts) != 2:
                    conn.sendall("ERROR: Send exactly two Numbers: <base> <exponent>".encode())
                    continue

                try:
                    base = float(parts[0])
                    exponent = float(parts[1])
                except ValueError:
                    # If not numbers: send error msg
                    conn.sendall("ERROR: base and exponent must be numbers".encode())
                    continue

                try:
                    # Calc base^exponent 
                    result = pow(base, exponent) 
                except OverflowError:
                    # If result large to calc: send error msg
                    conn.sendall("ERROR: result large to calc".encode())
                    continue

                # Send result to the client
                reply = str(result)
                conn.sendall(reply.encode())
                
                print(f"[REQUEST] {addr} -> {base}^{exponent} = (sent result, {len(reply)} bytes)")
    
            except Exception as e:
                print(f"[ERROR] {addr} : {e}")
                break

    print(f"[END] connection with {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create server TCP socket for IPv4 client connections
    server.bind((HOST, PORT)) # bind the server socket to the host and port
    server.listen() # listen for connections
    print(f"[LISTENING] Server listening on {HOST}:{PORT}")
    
    # timeout to see if Ctrl+C interrupt
    server.settimeout(1) 

    try:
        # continuously accept client connections
        while True:
            try:
               # accept new client connection 
                conn, addr = server.accept()
                
                # create thread for client 
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}") # number of connections: (total threads - 1 for main thread)

            except socket.timeout:
            # If timeout: continue to see if Ctrl+C interrupt 
                continue 
                        
    except Exception as e:
        print(f"\n[ERROR] error occurred: {e}")
        server.close()
        print("[CLOSE SERVER] Server socket closed")


if __name__ == "__main__":
    start_server()



