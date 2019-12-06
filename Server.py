# This is the server that will interact with the client and the nano.
#
# Authors:  Denver DeBoer
#           Nicholas English
#           Kevin Smith
# Date:     12-4-2019


import socket
import _thread
# from __future__ import division
from datetime import date
from datetime import datetime
from statistics import mean

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Local server
serverAddress = (socket.gethostbyname(socket.gethostname()), 10000)
print("Starting on %s port %s" % serverAddress)
print(serverAddress)
sock.bind(serverAddress)
sock.listen(1)


# Thread for the Nano device.
def nanoThread(connection):
    # Tells the user the connection is successful.
    try:
        print("Connection with ", clientAddress)
        # print("User: ", user[0])

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


# Thread for the client.
def clientThread(connection):
    # Tells the user the connection is successful.
    try:
        print("Connection with ", clientAddress)

        # Listens for the selected input from the client.
        while True:
            data = connection.recv(1024).decode()
            command = data.split(" ")
            print("\nReceived: %s" % data)

            if data:

                # Read in the data file.
                with open("data.txt", "r") as myfile:
                    stringData = str(myfile.readlines()[0])

                dataList = stringData.split(" ")
                # print(dataList)

                # Store all of the dates, times, and temps in their own lists (does this every request).
                dateList = []
                tempList = []
                timeList = []
                x = 0
                while x < (len(dataList)-1):
                    dateList.append(dataList[x])
                    timeList.append(dataList[x+1])
                    tempList.append(dataList[x+2])
                    x += 3

                # Gets the data stored.
                if command[0] == "GET":

                    # Returns the latest temperature.
                    if command[1] == "LATEST":
                        print(dataList[len(dataList) - 2])
                        connection.sendall(("LATEST: " + dataList[len(dataList) - 2]).encode())

                    # Returns values based on requested day.
                    elif command[1] == "SINGLE_DAY":

                        # Find items on the requested day.
                        singleDay = []
                        x = 0
                        for day in dataList:
                            if day == command[2]:
                                singleDay.append(float(dataList[x+2]))
                            x += 1

                        if command[3] == "ALL":
                            connection.sendall(("MAX: " + str(max(singleDay)) + ";AVG: " + str(format((sum(singleDay) / len(singleDay)), '.2f')) + ";MIN: " + str(min(singleDay))).encode())

                        elif command[3] == "MAX":
                            connection.sendall(("MAX: " + str(max(singleDay))).encode())

                        elif command[3] == "AVG":
                            connection.sendall(( "AVG: " + format((sum(singleDay) / len(singleDay)), '.2f') ).encode())

                        else: # command[3] == "MIN"
                            connection.sendall(("MIN: " + str(min(singleDay))).encode())


                    else: # command[1] == "RANGE"

                        # Find items on the requested day.
                        singleDay = []
                        x = 0
                        for day in dataList:
                            if command[2] <= day <= command[3]:
                                singleDay.append(float(dataList[x+2]))
                            x += 1

                        if command[4] == "ALL":
                            connection.sendall(("MAX: " + format(max(singleDay), '.2f') + ";AVG: " + str(format((sum(singleDay) / len(singleDay)), '.2f')) + ";MIN: " + format(min(singleDay), '.2f')).encode())

                        elif command[4] == "MAX":
                            connection.sendall(("MAX: " + format(max(singleDay), '.2f')).encode())

                        elif command[4] == "AVG":
                            connection.sendall(( "AVG: " + str(format((sum(singleDay) / len(singleDay)), '.2f')) ).encode())

                        else: # command[4] == "MIN"
                            connection.sendall(("MIN: " + format(min(singleDay), '.2f')).encode())

            else:
                break
    finally:
        print("Connection terminated!")


# Starts the connection process with the client.
while True:
    print("Waiting for a connection...\n")
    connection, clientAddress = sock.accept()

    typeUser = connection.recv(1024).decode()
    typeUser = typeUser.split(" ")

    if typeUser[0] == "NANO":
        # print("A NANO!")
        _thread.start_new_thread(nanoThread, (connection,))

    if typeUser[0] == "CLIENT":
        # print("A CLIENT!")
        _thread.start_new_thread(clientThread, (connection,))

sock.close()

