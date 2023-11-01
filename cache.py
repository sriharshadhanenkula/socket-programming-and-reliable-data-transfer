import socket
import argparse
import os
import os.path
import snw_transport
import tcp_transport

def run_cache(cache_port, server_ip, server_port, transport_protocol):
    # Create a socket object
    cache_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )

    # Bind the socket to the address and port
    cache_socket.bind(('', cache_port))
    cache_socket.listen(5)

    print(f"Cache listening on port {cache_port} using {transport_protocol} protocol")

    # Connect to the server and get the client socket
    client_socket, client_address = cache_socket.accept()
    server_address = (server_ip, server_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(server_address)
    
    if transport_protocol == 'tcp':
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if data == "":
                break
            if data == "quit":
                print("Client requested to exit.")
                break
            
            elif data.split()[0] == "get":
                print("get command")
                
                fileName = data.split()[1]
                # check if fileName exists in cache_folder
                path = "Cache_Folder/" + fileName
                
                #print(path)
                if os.path.exists(path):
                    client_socket.send("from_cache".encode('utf-8'))
                    message = client_socket.recv(1024).decode('utf-8')
                    if message == "send_data":
                        fileData = tcp_transport.readDataFromCacheFolder(path)
                        client_socket.send(fileData.encode('utf-8'))
                    
                else:
                    print("File does not exist in cache_folder")
                    client_socket.send("from_server".encode('utf-8'))

                    fileData = client_socket.recv(100000).decode('utf-8')
                    tcp_transport.writeDataInCacheFolder(fileData, path)
                    
            
            elif data.split()[0] == "put":
                print("put command")

            else:
                print("Invalid command")
                

        
    elif transport_protocol == 'snw':
        print("snw")
    
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if data == "":
                break
            if data == "quit":
                print("Client requested to exit.")
                break
            
            elif data.split()[0] == "get":
                print("get command")
                fileName = data.split()[1]
                path = "Cache_Folder/" + fileName
                if os.path.exists(path):
                    client_socket.send("from_cache".encode('utf-8'))
                    acknowledgement = client_socket.recv(1024).decode('utf-8')
                    if acknowledgement == "ACK":
                        with open("Cache_Folder/" + fileName, 'r') as file:
                            fileData = file.read()
                            file.close()
                        for i in range(0, len(fileData), 1000):
                            data = fileData[i:i+1000]
                            if data:
                                client_socket.send("data_start".encode('utf-8'))
                                if client_socket.recv(1024).decode('utf-8') == "ACK2":
                                    client_socket.send(data.encode('utf-8'))
                            else:
                                break
                            
                            
                        client_socket.send("FIN".encode('utf-8'))
                        
                    data = client_socket.recv(1024).decode('utf-8')
                    print(data)
                                
                        
                    
                    
                else:
                    print("File does not exist in cache_folder")
                    client_socket.send("from_server".encode('utf-8'))
                    
                    message = client_socket.recv(1024).decode('utf-8')
                    client_socket.send("ACK".encode('utf-8'))
                    while True:
                        message = client_socket.recv(1024).decode('utf-8')
                       
                        if message == "data_start":
                            client_socket.send("ACK2".encode('utf-8'))
                            data = client_socket.recv(1024).decode('utf-8')
                            snw_transport.callSnwCache(data, fileName)
                                    
                        elif message == "FIN":
                            break
                        
                    client_socket.send("File delivered from origin.".encode('utf-8'))               

            
            elif data.split()[0] == "put":
                print("put command")
        #         # server_socket.send(data.encode('utf-8'))
        #         # data = server_socket.recv(1024).decode('utf-8')
        #         # client_socket.send(data.encode('utf-8'))
        #     else:
        #         print("Invalid command")
   
    else:
        print("Invalid transport protocol")     

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