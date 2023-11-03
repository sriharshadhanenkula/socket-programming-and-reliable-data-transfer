import socket
import argparse
import snw_transport
import tcp_transport
import time


def run_client(server_ip, server_port, cache_ip, cache_port, transport_protocol):   # server_ip, server_port, cache_ip, cache_port, transport_protocol
    # Create a socket object

    if transport_protocol == "tcp":
        cache_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a socket object
        # Connect to the cache
        cache_address = (cache_ip, cache_port)  # Connect to the cache and get the client socket
        cache_socket.connect(cache_address) # Connect to the cache and get the client socket
        # Connect to the server

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        server_address = (server_ip, server_port)
        client_socket.connect(server_address)   # Connect to the server and get the client socket

        while True:
            userInput = input("Enter command: ")

            if userInput == "quit":         # If the client sends quit, close the connection
                client_socket.send(userInput.encode("utf-8"))
                print("Exiting program!")
                break

            elif userInput.split()[0] == "get":      # If the client sends get, check if the file exists in the cache_folder
                # print("get command")
                start_time = time.time()        # timer starts
                inputFile = userInput.split()[1]        
                cache_socket.send(userInput.encode("utf-8"))        # send the get command to the cache
                receivedFrom = cache_socket.recv(1024).decode("utf-8")    # receive the message from the cache

                if receivedFrom == "from_cache":
                    cache_socket.send("send_data".encode("utf-8"))      # send the message to the cache
                    fileData = cache_socket.recv(100000).decode("utf-8")    # receive the file from the cache
                    tcp_transport.saveDataInClientFolder(fileData, inputFile) # save the file in the client folder
                    print("File delivered from cache.")

                else:
                    # print("file from server")
                    client_socket.send(userInput.encode("utf-8"))   # send the get command to the server 
                    fileData = client_socket.recv(100000).decode("utf-8")   # receive the file from the server
                    tcp_transport.saveDataInClientFolder(fileData, inputFile)  # save the file in the client folder

                    cache_socket.send(fileData.encode("utf-8"))

                    print("File delivered from origin.")

                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Elapsed time: " + str(elapsed_time))

            elif userInput.split()[0] == "put":
                print("Awaiting server response.")
                inputFile = userInput.split()[1]

                client_socket.send(userInput.encode("utf-8")) # send the put command to the server
                # receive message from server to send file
                message = client_socket.recv(1024).decode("utf-8")  # receive the message from the server

                if message == "send file":      # if the message is send file
                    InputData = tcp_transport.readData(inputFile)  # read the file from the client folder

                    client_socket.send(InputData.encode("utf-8"))

                data = client_socket.recv(1024).decode("utf-8") # receive the message from the server
                print(data)

            else:
                print("Invalid command client")

        client_socket.close()
        cache_socket.close()

    elif transport_protocol == "snw":       # if the transport protocol is snw
        cache_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Create a socket object 
        cache_address = ("localhost", cache_port)       # Bind the socket to the address and port 

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create a socket object    
        server_address = ("localhost", server_port)

        print("snw")
        while True:
            userInput = input("Enter command: ")

            if userInput == "quit":
                server_socket.sendto(userInput.encode("utf-8"), server_address) # If the client sends quit, close the connection
                cache_socket.sendto(userInput.encode("utf-8"), cache_address)   # If the client sends quit, close the connection
                print("Exiting program!")
                break

            elif userInput.split()[0] == "get":
                print("get command")
                start_time = time.time()            # timer starts 
                inputFile = userInput.split()[1]
                cache_socket.sendto(userInput.encode("utf-8"), cache_address)       # send the get command to the cache

                receivedFrom, _ = cache_socket.recvfrom(1024) # receive the message from the cache
                receivedFrom = receivedFrom.decode("utf-8")   # decode the message
                length, _ = cache_socket.recvfrom(1024)     # receive the length of the file from the cache
                length = length.decode("utf-8")         # decode the length of the file
                myLength = int(length)
                receivedData = ""
                while myLength > 0:         # iterate through the chunks
                    data, _ = cache_socket.recvfrom(1024)  # receive the data from the cache
                    data = data.decode("utf-8")
                    receivedData += data
                    myLength -= len(data)       # decrement the length of the file

                    cache_socket.sendto("ACK".encode("utf-8"), cache_address)

                snw_transport.callSnwClient(receivedData, inputFile)        # save the file in the client folder

                print(receivedFrom)
                end_time = time.time()
                elapsed_time = end_time - start_time        # timer ends 
                print("Elapsed time: " + str(elapsed_time))     # timer ends 

            elif userInput.split()[0] == "put":         # if the client sends put command
                print("Awaiting server response.")
                start_time = time.time()
                inputFile = userInput.split()[1]        # split the data and get the file name
                path = "Client_Folder/" + inputFile
                server_socket.sendto(userInput.encode("utf-8"), server_address)  # send the put command to the server
                with open(path, "r") as f:
                    data = f.read()
                    data_len = len(data)
                    send_Length, _ = server_socket.recvfrom(1024)           # receive the message from the server
                    server_socket.sendto(str(data_len).encode("utf-8"), server_address)
                    received_length, _ = server_socket.recvfrom(1024)
                    chunk_size = 1000
                    chunks = [
                        data[i : i + chunk_size] for i in range(0, data_len, chunk_size)        # split the file into chunks
                    ]

                    for chunk in chunks:
                        server_socket.sendto(chunk.encode("utf-8"), server_address)     # send the chunks to the server
                        ack, _ = server_socket.recvfrom(1024)

                    # receive FIN acknowledgment from the server

                    server_socket.sendto("sentAllData".encode("utf-8"), server_address)     # send the message to the server

                    fin_ack, _ = server_socket.recvfrom(1024)       # fin acknowledgement from the server
                    FIN = fin_ack.decode("utf-8")    # decode the message
                    if FIN == "FIN":
                        print("File successfully uploaded.")    # if the file is successfully uploaded
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
    parser = argparse.ArgumentParser(description="Client program")  # Create a parser object
    parser.add_argument("server_ip", help="Server IP address")
    parser.add_argument("server_port", type=int, help="Server port")  # Add the arguments
    parser.add_argument("cache_ip", help="Cache IP address")
    parser.add_argument("cache_port", type=int, help="Cache port")      
    parser.add_argument(
        "transport_protocol",
        choices=["tcp", "snw"],
        help="Transport protocol (tcp or snw)",
    )
    args = parser.parse_args()    # Parse the arguments

    run_client(
        args.server_ip,
        args.server_port,
        args.cache_ip,
        args.cache_port,
        args.transport_protocol,
    )
