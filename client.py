import socket
import argparse

def run_client(server_ip, server_port, cache_ip, cache_port, transport_protocol):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if transport_protocol == 'tcp' else socket.SOCK_DGRAM)

    # Connect to the server
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)
    
    while True:
        userInput = input("Enter command: ")
        
        if userInput == "quit":
            client_socket.send(userInput.encode('utf-8'))
            print("Exiting program!")
            break
        
        elif userInput.split()[0] == "get":
            print("get command")
            client_socket.send(userInput.split()[0].encode('utf-8'))
        
        elif userInput.split()[0] == "put":
            inputFile = userInput.split()[1]
            print(inputFile)
            # client_socket.send(userInput.split()[0].encode('utf-8'))
            # client_socket.send(inputFile.encode('utf-8'))
            
            # send both userInput and inputFile to server only once socket request 
            client_socket.send(userInput.encode('utf-8') + inputFile.encode('utf-8')) 
            
            # with open(inputFile, 'r') as file:
            #     InputData = file.read().replace('\n', '')
            
            # for i in range(0, len(InputData), 1000):
            #     data = InputData[i:i+1000]
            #     client_socket.send(data.encode('utf-8'))
               # print(f"Sent to server: {data}")
                
            print("Awaiting server response.")
            
        else:
            print("Invalid command")
        
      

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client program")
    parser.add_argument("server_ip", help="Server IP address")
    parser.add_argument("server_port", type=int, help="Server port")
    parser.add_argument("cache_ip", help="Cache IP address")
    parser.add_argument("cache_port", type=int, help="Cache port")
    parser.add_argument("transport_protocol", choices=['tcp', 'snw'], help="Transport protocol (tcp or snw)")
    args = parser.parse_args()

    run_client(args.server_ip, args.server_port, args.cache_ip, args.cache_port, args.transport_protocol)


