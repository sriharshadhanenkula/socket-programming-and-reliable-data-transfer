import socket
import argparse

def run_server(port, transport_protocol):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if transport_protocol == 'tcp' else socket.SOCK_DGRAM)

    # Bind the socket to the address and port
    server_socket.bind(('0.0.0.0', port))

    server_socket.listen(1)

    print(f"Server listening on port {port} using {transport_protocol} protocol")

    client_socket, client_address = server_socket.accept()

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        print(data)
        print("------------------")
        if data == "quit":
            print("Client requested to exit.")
            break
        
        elif data.split()[0] == "get":
            print("get command")
        
        elif data.split()[0] == "put":
            print("put command")
            print(data[1])
            # with open("Server_Folder/server.txt", "a") as f:
            #     f.write(data)
            #     f.close()
            # print("Data stored in file.")
        
        elif len(data.split()) == 1:
            print("filename")
            
        
        
        
        #print(f"Received from client: {data}")
        
        # store data in file
        # with open("Server_Folder/server.txt", "a") as f:
        #     f.write(data)
        #     f.close()
        # print("Data stored in file.")

    # Close the sockets
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server program")
    parser.add_argument("port", type=int, help="Server port")
    parser.add_argument("transport_protocol", choices=['tcp', 'snw'], help="Transport protocol (tcp or snw)")
    args = parser.parse_args()

    run_server(args.port, args.transport_protocol)



