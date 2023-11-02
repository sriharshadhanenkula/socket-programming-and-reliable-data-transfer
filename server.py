import socket
import argparse
import tcp_transport
import snw_transport
import time

def run_server(port, transport_protocol):
    
    
    if transport_protocol == 'tcp':
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_socket.bind(('', port))

        server_socket.listen(5)

        print(f"Server listening on port {port} using {transport_protocol} protocol")

        client_socket, client_address = server_socket.accept()
        
        while True:
            # client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')
            if data == "":
                break
            if data == "quit":
                print("Client requested to exit.")
                break
            
            elif data.split()[0] == "get":
                print("get command")
                inputFile = data.split()[1]
                fileData = tcp_transport.readDataServerFolder(inputFile) 
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
                
        client_socket.close()
        
    elif transport_protocol == 'snw':
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('localhost', port))
        print(f"Server listening on port {port} using {transport_protocol} protocol")

        
        print("snw")
        
        while True:
            data, client_address = server_socket.recvfrom(1024)
            data = data.decode('utf-8')
            if data == "quit":
                print("Client requested to exit.")
                break
            
            elif data.split()[0] == "get":
                print("get command")
                inputFile = data.split()[1]
                
                fileData = snw_transport.callSnwReadServer(inputFile)
                length = len(fileData)
                server_socket.sendto(str(length).encode('utf-8'), client_address)
                
                chunk_size = 1000
                chunks = [fileData[i:i+chunk_size] for i in range(0, len(fileData), chunk_size)]
                
                for chunk in chunks:
                    server_socket.sendto(chunk.encode('utf-8'), client_address)
                    ack, _ = server_socket.recvfrom(1024)
                     
            
            elif data.split()[0] == "put":
                print("put command")
                
                inputFile = data.split()[1]
                data_len, _ = server_socket.recvfrom(1024)
                data_len = data_len.decode('utf-8')
                #data_len = int(data_len)
                length = int(data_len)

                received_data = ""
                while length > 0:
                    data, _ = server_socket.recvfrom(1024)
                    data = data.decode('utf-8')
                    received_data += data
                    length -= len(data)

                    # Send acknowledgment
                    server_socket.sendto("ACK".encode('utf-8'), client_address)
            
                # store the received data into a file
                snw_transport.callSnwServer(received_data, inputFile)

                # # Send FIN acknowledgment to the client
                server_socket.sendto("FIN".encode('utf-8'), client_address)
                
    
            else:
                print("Invalid command")
   
    else:
        print("Invalid transport protocol")       
        

    # Close the sockets
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server program")
    parser.add_argument("port", type=int, help="Server port")
    parser.add_argument("transport_protocol", choices=['tcp', 'snw'], help="Transport protocol (tcp or snw)")
    args = parser.parse_args()

    run_server(args.port, args.transport_protocol)