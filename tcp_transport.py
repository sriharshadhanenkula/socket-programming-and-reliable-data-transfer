def callTcpServer(fileData, inputFile):
    path = "Server_Folder/" + inputFile
    with open(path, "a") as f:
        f.write(fileData)
        f.close()