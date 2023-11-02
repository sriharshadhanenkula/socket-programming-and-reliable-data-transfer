import socket
import argparse
import snw_transport
import tcp_transport
import time

def run_client(server_ip, server_port, cache_ip, cache_port, transport_protocol):
    # Create a socket object

    
    if transport_protocol == 'tcp':
        
        cache_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        # Connect to the cache
        cache_address = (cache_ip, cache_port)
        cache_socket.connect(cache_address)
        # Connect to the server
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)
        client_socket.connect(server_address)
        
        while True:
            userInput = input("Enter command: ")
            
            if userInput == "quit":
                client_socket.send(userInput.encode('utf-8'))
                print("Exiting program!")
                break
            
            elif userInput.split()[0] == "get":
                #print("get command")
                start_time = time.time()
                inputFile = userInput.split()[1]
                cache_socket.send(userInput.encode('utf-8'))
                receivedFrom = cache_socket.recv(1024).decode('utf-8')
                
                if receivedFrom == "from_cache":
                    cache_socket.send("send_data".encode('utf-8'))
                    fileData = cache_socket.recv(100000).decode('utf-8')
                    tcp_transport.saveDataInClientFolder(fileData, inputFile)
                    print("File delivered from cache.")
                    
                else:
                    #print("file from server")
                    client_socket.send(userInput.encode('utf-8'))
                    fileData = client_socket.recv(100000).decode('utf-8')
                    tcp_transport.saveDataInClientFolder(fileData, inputFile)
     
                    cache_socket.send(fileData.encode('utf-8'))
                 
                    print("File delivered from origin.")
                    
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Elapsed time: " + str(elapsed_time)) 
                           
            
            elif userInput.split()[0] == "put":
                print("Awaiting server response.")
                inputFile = userInput.split()[1]
         
                client_socket.send(userInput.encode('utf-8'))
                #receive message from server to send file
                message = client_socket.recv(1024).decode('utf-8')

                if(message == "send file"):
                    InputData = tcp_transport.readData(inputFile)
                        
                    client_socket.send(InputData.encode('utf-8'))
                            
                data = client_socket.recv(1024).decode('utf-8')
                print(data)
                
            else:
                print("Invalid command client")
                
        client_socket.close()
        cache_socket.close()
        
    elif transport_protocol == 'snw':
        
        cache_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
        cache_address = ("localhost", cache_port)
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', server_port)
        
        
        print("snw")
        while True:
            userInput = input("Enter command: ")
            
            if userInput == "quit":
                server_socket.sendto(userInput.encode('utf-8'), server_address)
                cache_socket.sendto(userInput.encode('utf-8'), cache_address)
                print("Exiting program!")
                break
            
            elif userInput.split()[0] == "get":
                print("get command")
                start_time = time.time()
                inputFile = userInput.split()[1]
                cache_socket.sendto(userInput.encode('utf-8'), cache_address)
                
                receivedFrom, _ = cache_socket.recvfrom(1024)
                receivedFrom = receivedFrom.decode('utf-8')
                length, _ = cache_socket.recvfrom(1024)
                length = length.decode('utf-8')
                myLength = int(length)
                receivedData = ""
                while myLength > 0:
                    data, _ = cache_socket.recvfrom(1024)
                    data = data.decode('utf-8')
                    receivedData += data
                    myLength -= len(data)
                    
                    cache_socket.sendto("ACK".encode('utf-8'), cache_address)
                    
                snw_transport.callSnwClient(receivedData, inputFile)
                
                print(receivedFrom)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Elapsed time: " + str(elapsed_time))
                        
            
            elif userInput.split()[0] == "put":
                print("Awaiting server response.")
                start_time = time.time()
                inputFile = userInput.split()[1]
                path = "Client_Folder/" + inputFile
                server_socket.sendto(userInput.encode('utf-8'), server_address)
                with open(path, 'r') as f:
                    data = f.read()
                    data_len = len(data)
                    server_socket.sendto(str(data_len).encode('utf-8'), server_address)

                    chunk_size = 1000
                    chunks = [data[i:i + chunk_size] for i in range(0, data_len, chunk_size)]

                    for chunk in chunks:
                        server_socket.sendto(chunk.encode('utf-8'), server_address)
                        ack, _ = server_socket.recvfrom(1024)

                    # receive FIN acknowledgment from the server
                    fin_ack, _ = server_socket.recvfrom(1024)
                    FIN = fin_ack.decode('utf-8')
                    if FIN == "FIN":
                        print("File successfully uploaded.")
                    else:
                        print("File upload failed.")
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Elapsed time: " + str(elapsed_time))   
                    
                
            else:
                print("Invalid command")
        
    else:
        print("Invalid transport protocol")

      

    # Close the socket
    
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client program")
    parser.add_argument("server_ip", help="Server IP address")
    parser.add_argument("server_port", type=int, help="Server port")
    parser.add_argument("cache_ip", help="Cache IP address")
    parser.add_argument("cache_port", type=int, help="Cache port")
    parser.add_argument("transport_protocol", choices=['tcp', 'snw'], help="Transport protocol (tcp or snw)")
    args = parser.parse_args()

    run_client(args.server_ip, args.server_port, args.cache_ip, args.cache_port, args.transport_protocol)
