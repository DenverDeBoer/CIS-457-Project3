# This is the server that will interact with the client and the nano.
#
# Authors:  Denver DeBoer
#           Nicholas English
#           Kevin Smith
# Date:     12-4-2019


import socket
import _thread

from datetime import date
from datetime import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Local server
serverAddress = (socket.gethostbyname(socket.gethostname()), 10000)
print("Starting on %s port %s" % serverAddress)
print(serverAddress)
sock.bind(serverAddress)
sock.listen(1)


def clientThread(connection):
    # Tells the user the connection is successful.
    try:

        # Gets the user that connected and add to user table
        user = connection.recv(1024).decode()
        user = user.split(" ")

        print("Connection with ", clientAddress)
        print("User: ", user[0])

        # Listens for the selected input from the client.
        while True:
            data = connection.recv(1024).decode()
            command = data.split(" ")
            print("\nReceived: %s" % data)
            if data:

                # Check if a Nano device sent the data.
                if command[0] == "NANO":

                    # Store to a file.
                    with open("data.txt", "a") as myfile:
                        data2write = str(date.today()) + " " + str(datetime.now().time()) + " " + command[1] + " "
                        myfile.write(data2write)

                else:
                    print("INVALID COMMAND")
            else:
                break
    finally:
        print("Connection terminated!")


# Starts the connection process with the client.
while True:
    print("Waiting for a connection...\n")
    connection, clientAddress = sock.accept()
    _thread.start_new_thread(clientThread, (connection,))

sock.close()



