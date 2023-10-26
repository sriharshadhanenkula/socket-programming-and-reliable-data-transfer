import socket
import argparse

def run_cache(cache_port, server_ip, server_port, transport_protocol):
    # Create a socket object
    cache_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if transport_protocol == 'tcp' else socket.SOCK_DGRAM)

    # Bind the socket to the address and port
    cache_socket.bind(('', cache_port))
    cache_socket.listen(5)

    print(f"Cache listening on port {cache_port} using {transport_protocol} protocol")

    # Connect to the server and get the client socket
    client_socket, client_address = cache_socket.accept()
    server_address = (server_ip, server_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if transport_protocol == 'tcp' else socket.SOCK_DGRAM)
    server_socket.connect(server_address)
    
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if data == "quit":
            print("Client requested to exit.")
            break
        
        elif data.split()[0] == "get":
            print("get command")
            # server_socket.send(data.encode('utf-8'))
            # data = server_socket.recv(1024).decode('utf-8')
            # client_socket.send(data.encode('utf-8'))
        
        elif data.split()[0] == "put":
            print("put command")
            # server_socket.send(data.encode('utf-8'))
            # data = server_socket.recv(1024).decode('utf-8')
            # client_socket.send(data.encode('utf-8'))
        else:
            print("Invalid command")
            

    # Close the sockets
    client_socket.close()
    server_socket.close()
    


   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cache program")
    parser.add_argument("cache_port", type=int, help="Cache port")
    parser.add_argument("server_ip", help="Server IP address")
    parser.add_argument("server_port", type=int, help="Server port")
    parser.add_argument("transport_protocol", choices=['tcp', 'snw'], help="Transport protocol (tcp or snw)")
    args = parser.parse_args()

    run_cache(args.cache_port, args.server_ip, args.server_port, args.transport_protocol)
