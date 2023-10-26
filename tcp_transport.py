def callTcp(data):

    with open("Server_Folder/server.txt", "a") as f:
        f.write(data)
        f.close()
    