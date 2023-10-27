import socket
import argparse
import os
import os.path

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
                
                print(path)
                if os.path.exists(path):
                    client_socket.send("from_cache".encode('utf-8'))
                    message = client_socket.recv(1024).decode('utf-8')
                    if message == "send_data":
                        with open(path, 'r') as file:
                            fileData = file.read()
                            file.close()
                        client_socket.send(fileData.encode('utf-8'))
    
                    
                else:
                    print("File does not exist in cache_folder")
                    client_socket.send("from_server".encode('utf-8'))

                    fileData = client_socket.recv(100000).decode('utf-8')
                    with open(path, 'w') as file:
                        file.write(fileData)
                        file.close()
                    
            
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
        #         client_socket.send("send file".encode('utf-8'))
                
        #         fileName = client_socket.recv(1024).decode('utf-8')
        #         print(fileName)
                
        #         # check if fileName exists in cache_folder 
        #         if os.path.isfile("Cache_Folder/" + fileName):
        #             print("File exists in cache_folder")
        #             client_socket.send("from_cache".encode('utf-8'))
        #             with open("Cache_Folder/" + fileName, 'r') as file:
        #                 fileData = file.read()
        #                 file.close()
        #             for i in range(0, len(fileData), 1000):
        #                 data = fileData[i:i+1000]
        #                 if data:
        #                     client_socket.send("data_start".encode('utf-8'))
        #                     if client_socket.recv(1024).decode('utf-8') == "data_start_ok":
        #                         client_socket.send(data.encode('utf-8'))
                    
        #             client_socket.send("data_end".encode('utf-8'))
                
                
                # else:
                #     print("File does not exist in cache_folder")
        #             client_socket.send("from_server".encode('utf-8'))
                
        #             # # file does not exist in cache_folder
        #             # # send message to server to get file
        #             # server_socket.send(data.encode('utf-8'))
        #             # data = server_socket.recv(1024).decode('utf-8')
        #             # client_socket.send(data.encode('utf-8'))
        #             # # receive file from server
        #             # data = server_socket.recv(1024).decode('utf-8')
        #             # # save file to cache_folder
        #             # with open("Cache_Folder/" + fileName, 'w') as file:
        #             #     file.write(data)
        #             #     file.close()
        #             # # send file to client
        #             # client_socket.send(data.encode('utf-8'))
                
            
        #         print(data)
                
        #         # server_socket.send(data.encode('utf-8'))
        #         # data = server_socket.recv(1024).decode('utf-8')
        #         # client_socket.send(data.encode('utf-8'))
            
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