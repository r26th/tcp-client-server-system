# client.py
import socket
import time

# Define server IP and port to connect to
SERVER_IP = "192.168.8.122"  # IP address of the server
PORT = 5000                 # Port number to connect to

# Main function to run the client
def main():
    print("Client started.")  # Print when the client starts
    # Create a new socket object for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server using the provided IP and port
    client.connect((SERVER_IP, PORT))
    print(f"Connected to server at {SERVER_IP}:{PORT}")  # Print connection details

    try:
        # Continuously ask the user for input
        while True:
            # Get user input for base and exponent or exit command
            user = input("Enter base and exponent numbers in this order: <base> <exponent>, or 'exit' to close: ").strip()
            if not user:  # Skip if input is empty
                continue

            # Send the user input to the server
            start = time.perf_counter()  # Start measuring round-trip time (RTT)
            client.sendall(user.encode())

            # Receive data (the result) from the server
            data = client.recv(65536)  # Use large buffer size to handle large results
            end = time.perf_counter()  # End measuring round-trip time (RTT)

            if not data:  # If no data is received, print a message and break
                print("No response (server may have closed connection).")
                break

            # Decode and print the server's reply
            reply = data.decode()
            rtt = end - start  # Calculate the round-trip time (RTT)
            print(f"Server reply: {reply}")  # Print the server's response
            print(f"RTT: {rtt:.6f} seconds\n")  # Print the round-trip time in seconds

            # Exit the loop if the user types "exit"
            if user.lower() == "exit":
                break

    except KeyboardInterrupt:
        # Handle keyboard interruption (Ctrl+C)
        print("\nClient terminated by user.")
    finally:
        # Close the client connection and print a closing message
        client.close()
        print("Connection closed.")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
