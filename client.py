import socket
import argparse

def run_client(server_ip, server_port, cache_ip, cache_port, transport_protocol):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if transport_protocol == 'tcp' else socket.SOCK_DGRAM)

    # Connect to the server
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)
    
    inputFile = "file1.txt"
    with open(inputFile, 'r') as file:
        InputData = file.read().replace('\n', '')

    while True:
        # data = input("Enter command: ")
        # client_socket.send(data.encode('utf-8'))

        # if data == "exit":
        #     print("Exiting client.")
        #     break
           
        for i in range(0, len(InputData), 1000):
            data = InputData[i:i+1000]
            client_socket.send(data.encode('utf-8'))
            print(f"Sent to server: {data}")
            
        myInput = input("Enter your message: ")
        if myInput == "exit":
            client_socket.send(myInput.encode('utf-8'))
            print("Exiting...")
            break

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client program")
    parser.add_argument("server_ip", help="Server IP address")
    parser.add_argument("server_port", type=int, help="Server port")
    parser.add_argument("cache_ip", help="Cache IP address")
    parser.add_argument("cache_port", type=int, help="Cache port")
    parser.add_argument("transport_protocol", choices=['tcp', 'snw'], help="Transport protocol (tcp or snw)")
    args = parser.parse_args()

    run_client(args.server_ip, args.server_port, args.cache_ip, args.cache_port, args.transport_protocol)


























# import socket

# # Server configuration
# host = "127.0.0.1"
# port = 12345

# inputFile = "file1.txt"
# with open(inputFile, 'r') as file:
#     InputData = file.read().replace('\n', '')

# # Create a socket object
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect to the server
# client_socket.connect((host, port))

# while True:
    
#     # the sender splits the InputData into equal chunks of 1000 bytes each, and proceeds to send the data one chunk at a time to the receiver.
    
#     for i in range(0, len(InputData), 1000):
#         data = InputData[i:i+1000]
#         client_socket.send(data.encode('utf-8'))
#         print(f"Sent to server: {data}")
        
#     myInput = input("Enter your message: ")
#     if myInput == "exit":
#         client_socket.send(myInput.encode('utf-8'))
#         print("Exiting...")
#         break


# client_socket.close()
