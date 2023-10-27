def callSnwServer(data, inputFile):
    with open("Server_Folder/" + inputFile, 'a') as file:
        file.write(data)
        file.close()