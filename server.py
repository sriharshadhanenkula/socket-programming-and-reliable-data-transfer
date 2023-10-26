import socket
import argparse
import tcp_transport

def run_server(port, transport_protocol):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if transport_protocol == 'tcp' else socket.SOCK_DGRAM)

    # Bind the socket to the address and port
    server_socket.bind(('', port))

    server_socket.listen(5)

    print(f"Server listening on port {port} using {transport_protocol} protocol")

    client_socket, client_address = server_socket.accept()
     
    
    if transport_protocol == 'tcp':
        while True:
            # client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')
            if data == "quit":
                print("Client requested to exit.")
                break
            
            elif data.split()[0] == "get":
              
                print("get command")
                inputFile = data.split()[1]
                
                with open("Server_Folder/" + inputFile, 'r') as file:
                    fileData = file.read()
                    file.close()
                    
                client_socket.send(fileData.encode('utf-8'))    
                       
            
            elif data.split()[0] == "put":
                #print("put command")
                inputFile = data.split()[1]
                
                client_socket.send("send file".encode('utf-8')) 
                # receive file data from client which is greater than 10000 bytes
                fileData = client_socket.recv(100000).decode('utf-8')
                tcp_transport.callTcpServer(fileData, inputFile)
                
                client_socket.send("File successfully uploaded.".encode('utf-8'))
                print("File successfully uploaded.")
                
            
        
    elif transport_protocol == 'snw':
        print("snw")
        
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if data == "quit":
                print("Client requested to exit.")
                break
            
            elif data.split()[0] == "get":
                print("get command")
                print(data[1])
            
            elif data.split()[0] == "put":
                print("put command")
                # send message to client to send file
                client_socket.send("send file".encode('utf-8')) 
                while True:
                    data = client_socket.recv(1024).decode('utf-8')
                    if data == "data_start":
                        client_socket.send("data_start_ok".encode('utf-8'))
                        data = client_socket.recv(1024).decode('utf-8')
                        tcp_transport.callTcp(data)
                    elif data == "data_end":
                        break
                
                client_socket.send("File successfully uploaded.".encode('utf-8'))
                print("File successfully uploaded.")
            else:
                print("Invalid command")
   
    else:
        print("Invalid transport protocol")       
        

    # Close the sockets
    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server program")
    parser.add_argument("port", type=int, help="Server port")
    parser.add_argument("transport_protocol", choices=['tcp', 'snw'], help="Transport protocol (tcp or snw)")
    args = parser.parse_args()

    run_server(args.port, args.transport_protocol)



