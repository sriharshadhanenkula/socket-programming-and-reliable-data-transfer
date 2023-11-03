import socket
import argparse
import os
import os.path
import snw_transport
import tcp_transport

def run_cache(cache_port, server_ip, server_port, transport_protocol):  # cache_port, server_ip, server_port, transport_protocol
    # Create a socket object
    
    
    if transport_protocol == 'tcp':
        cache_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )       # Create a socket object

        # Bind the socket to the address and port
        cache_socket.bind(('', cache_port))                       # Bind the socket to the address and port
        cache_socket.listen(5)

        print(f"Cache listening on port {cache_port} using {transport_protocol} protocol")

        # Connect to the server and get the client socket
        client_socket, client_address = cache_socket.accept()           # Connect to the server and get the client socket
        server_address = (server_ip, server_port)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Create a socket object
        server_socket.connect(server_address)                # Connect to the server
        
        
        while True:
            data = client_socket.recv(1024).decode('utf-8')     # Receive data from the client
            if data == "":
                break
            if data == "quit":                    # If the client sends quit, close the connection
                print("Client requested to exit.")      # If the client sends quit, close the connection
                break
            
            elif data.split()[0] == "get":          # if the client sends get
                print("get command")
                
                fileName = data.split()[1]          # split the data and get the file name
                path = "Cache_Folder/" + fileName
                
                #print(path)
                if os.path.exists(path):            # If the file exists in the cache_folder, send the file to the client
                    client_socket.send("from_cache".encode('utf-8'))
                    message = client_socket.recv(1024).decode('utf-8')      # send the message to the client
                    if message == "send_data":        # check if the message is send_data
                        fileData = tcp_transport.readDataFromCacheFolder(path)
                        client_socket.send(fileData.encode('utf-8'))
                    
                else:
                    print("File does not exist in cache_folder")
                    client_socket.send("from_server".encode('utf-8'))       # send the message to the client

                    fileData = client_socket.recv(100000).decode('utf-8')     
                    tcp_transport.writeDataInCacheFolder(fileData, path)   # save the file in the cache_folder     
            
            elif data.split()[0] == "put":
                print("put command")

            else:
                print("Invalid command")
                
        client_socket.close()       # Close the sockets
        server_socket.close()       

        
    elif transport_protocol == 'snw':
        
        cache_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # Create a socket object 
        cache_socket.bind(('localhost', cache_port))                # Bind the socket to the address and port
        print(f"Cache listening on port {cache_port} using {transport_protocol} protocol")      # Bind the socket to the address and port
        
        server_address = ('localhost', server_port)         # Connect to the server and get the client socket
        
        print("snw")
        
        while True:
            data, address = cache_socket.recvfrom(1024)     # Receive data from the client
            data = data.decode('utf-8')         
            if data == "":
                break
            if data == "quit":
                print("Client requested to exit.")      # If the client sends quit, close the connection
                cache_socket.close()            # If the client sends quit, close the connection
                break
            
            elif data.split()[0] == "get":
                print("get command")
                
                inputFile = data.split()[1]
                path = "Cache_Folder/" + inputFile          
                if os.path.exists(path):
                    fileData = snw_transport.callSnwReadCache(path)         #   read the file from the cache_folder
                    cache_socket.sendto("File delivered from cache.".encode('utf-8'), address)       #  send the message to the client
                    
                    length = len(fileData)
                    cache_socket.sendto(str(length).encode('utf-8'), address)    # send the file to the client
                    
                    chunk_size = 1000
                    chunks = [fileData[i:i+chunk_size] for i in range(0, len(fileData), chunk_size)]    # iterate through the chunks
                    
                    for chunk in chunks:
                        cache_socket.sendto(chunk.encode('utf-8'), address)     # send the file to the client
                        ack, _ = cache_socket.recvfrom(1024)        #  receive acknoledgement from the client
  
                else:
                    print("File does not exist in cache_folder")
                    
                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
                    server_socket.sendto(data.encode('utf-8'), server_address)      # send the data to the server
                    
                    length, _ = server_socket.recvfrom(1024)
                    length = length.decode('utf-8')
                    myLength = int(length)
                    receivedData = ""
                    while myLength > 0:         # If length is greater than 0
                        data, _ = server_socket.recvfrom(1024)      #  receive the file from the server
                        data = data.decode('utf-8')
                        receivedData += data        
                        myLength -= len(data)       #  length of the file
                        server_socket.sendto("ACK".encode('utf-8'), server_address)     #  send acknoledgement to the server
                        
                    snw_transport.callSnwCache(receivedData, inputFile)     # save the file in the cache_folder
                        
                    cache_socket.sendto("File delivered from origin.".encode('utf-8'), address)
                    cache_socket.sendto(length.encode('utf-8'), address)        # send the file to the client
                    
                    chunk_size = 1000
                    chunks = [receivedData[i:i+chunk_size] for i in range(0, len(receivedData), chunk_size)]    # iterate through the chunks 
                    
                    for chunk in chunks:        #  chunk the file 
                        cache_socket.sendto(chunk.encode('utf-8'), address)     #  send the file to the client
                        ack, _ = cache_socket.recvfrom(1024)        #  acknoledgement

            
            elif data.split()[0] == "put":
                print("put command")
   
    else:
        print("Invalid transport protocol")     

    # Close the sockets
   


   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cache program")       # cache_port, server_ip, server_port, transport_protocol
    parser.add_argument("cache_port", type=int, help="Cache port")
    parser.add_argument("server_ip", help="Server IP address")      # cache_port, server_ip, server_port, transport_protocol
    parser.add_argument("server_port", type=int, help="Server port")
    parser.add_argument("transport_protocol", choices=['tcp', 'snw'], help="Transport protocol (tcp or snw)")    # cache_port, server_ip, server_port, transport_protocol
    args = parser.parse_args()

    run_cache(args.cache_port, args.server_ip, args.server_port, args.transport_protocol)   # cache_port, server_ip, server_port, transport_protocol