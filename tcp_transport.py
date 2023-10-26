def callTcpServer(fileData, inputFile):
    path = "Server_Folder/" + inputFile
    with open(path, "w") as f:
        f.write(fileData)
        f.close()