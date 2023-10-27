import socket
import argparse

def run_client(server_ip, server_port, cache_ip, cache_port, transport_protocol):
    # Create a socket object
    
    cache_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
    # Connect to the cache
    cache_address = (cache_ip, cache_port)
    cache_socket.connect(cache_address)
    # Connect to the server
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)
    
    if transport_protocol == 'tcp':
        while True:
            userInput = input("Enter command: ")
            
            if userInput == "quit":
                client_socket.send(userInput.encode('utf-8'))
                print("Exiting program!")
                break
            
            elif userInput.split()[0] == "get":
                print("get command")
                inputFile = userInput.split()[1]
                cache_socket.send(userInput.encode('utf-8'))
                receivedFrom = cache_socket.recv(1024).decode('utf-8')
                
                if receivedFrom == "from_cache":
                    cache_socket.send("send_data".encode('utf-8'))
                    fileData = cache_socket.recv(100000).decode('utf-8')

                    with open("Client_Folder/" + inputFile, "a") as f:
                        f.write(fileData)
                        f.close()
                    print("File delivered from cache.")
                    
                else:
                    print("file from server")
                    client_socket.send(userInput.encode('utf-8'))
                    fileData = client_socket.recv(100000).decode('utf-8')
                    with open("Client_Folder/" + inputFile, "w") as f:
                        f.write(fileData)
                        f.close()
                            
                    cache_socket.send(fileData.encode('utf-8'))
                 
                    print("File delivered from origin.")
                
               
            
            elif userInput.split()[0] == "put":
                print("Awaiting server response.")
                inputFile = userInput.split()[1]
         
                client_socket.send(userInput.encode('utf-8'))
                #receive message from server to send file
                message = client_socket.recv(1024).decode('utf-8')

                if(message == "send file"):
                    with open(inputFile, 'r') as file:
                        InputData = file.read()        
                        
                    client_socket.send(InputData.encode('utf-8'))
                            
                data = client_socket.recv(1024).decode('utf-8')
                print(data)
                
            else:
                print("Invalid command client")
        
    elif transport_protocol == 'snw':
        print("snw")
        while True:
            userInput = input("Enter command: ")
            
            if userInput == "quit":
                client_socket.send(userInput.encode('utf-8'))
                print("Exiting program!")
                break
            
            elif userInput.split()[0] == "get":
                print("get command")
        #         inputFile = userInput.split()[1]
        #         cache_socket.send(userInput.split()[0].encode('utf-8'))
        #         message = cache_socket.recv(1024).decode('utf-8')
        #         if message == "send file":
        #             cache_socket.send(inputFile.encode('utf-8'))
        #             receivedFrom = cache_socket.recv(1024).decode('utf-8')
        #             if receivedFrom == "from_cache":
        #                 while True:
        #                     message = cache_socket.recv(1024).decode('utf-8')
        #                     if message == "data_start":
        #                         cache_socket.send("data_start_ok".encode('utf-8'))
        #                         path = "Client_Folder/" + inputFile
        #                         with open(path, "a") as f:
        #                             f.write(data)
        #                             f.close()
                                    
        #                     elif message == "data_end":
        #                         break
        #                 print("File delivered from cache.")
        #             else:
        #                 print("file from server")
                        
                        
                    
            
            elif userInput.split()[0] == "put":
                print("Awaiting server response.")
                inputFile = userInput.split()[1]
                #print(inputFile)
                client_socket.send(userInput.encode('utf-8'))
                # receive message from server to send file
                message = client_socket.recv(1024).decode('utf-8')
                #print(message)
                if(message == "send length"):
                    
                    with open(inputFile, 'r') as file:
                        InputData = file.read()
                    myLength = "LEN:"+str(len(InputData))
                    client_socket.send(myLength .encode('utf-8'))
                    
                    message = client_socket.recv(1024).decode('utf-8')
                    if(message == "ACK"):
                        
                        for i in range(0, len(InputData), 1000):
                            data = InputData[i:i+1000]
                            if data:
                                client_socket.send("data_start".encode('utf-8'))
                                if client_socket.recv(1024).decode('utf-8') == "ACK2":
                                    client_socket.send(data.encode('utf-8'))
                        
                        client_socket.send("FIN".encode('utf-8'))
                                
                    data = client_socket.recv(1024).decode('utf-8')
                    print(data)
                        
                #print("File successfully uploaded.")
        
                
            else:
                print("Invalid command")
        
        
    else:
        print("Invalid transport protocol")
       
        
      

    # Close the socket
    client_socket.close()
    cache_socket.close()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client program")
    parser.add_argument("server_ip", help="Server IP address")
    parser.add_argument("server_port", type=int, help="Server port")
    parser.add_argument("cache_ip", help="Cache IP address")
    parser.add_argument("cache_port", type=int, help="Cache port")
    parser.add_argument("transport_protocol", choices=['tcp', 'snw'], help="Transport protocol (tcp or snw)")
    args = parser.parse_args()

    run_client(args.server_ip, args.server_port, args.cache_ip, args.cache_port, args.transport_protocol)
