def callTcpServer(fileData, inputFile):
    path = "Server_Folder/" + inputFile
    with open(path, "w") as f:
        f.write(fileData)
        f.close()
        
def readData(inputFile):
    path = "Client_Folder/" + inputFile
    with open(path, "r") as f:
        fileData = f.read()
        f.close()
    return fileData

def saveDataInClientFolder(fileData, inputFile):
    with open("Client_Folder/" + inputFile, "w") as f:
        f.write(fileData)
        f.close()
        
def readDataFromCacheFolder(path):
    with open(path, 'r') as file:
        fileData = file.read()
        file.close()
        
    return fileData

def writeDataInCacheFolder(fileData, path):
    with open(path, 'w') as file:
        file.write(fileData)
        file.close()
        
def readDataServerFolder(inputFile):
    with open("Server_Folder/" + inputFile, 'r') as file:
        fileData = file.read()
        file.close()
        
    return fileData