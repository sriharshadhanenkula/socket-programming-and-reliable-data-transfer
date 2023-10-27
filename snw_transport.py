def callSnwServer(data, inputFile):
    with open("Server_Folder/" + inputFile, 'a') as file:
        file.write(data)
        file.close()
        
def callSnwClient(data,inputFile):
    with open("Client_Folder/" + inputFile, 'a') as file:
        file.write(data)
        file.close()
        
def callSnwCache(data,inputFile):
    with open("Cache_Folder/" + inputFile, 'a') as file:
        file.write(data)
        file.close()