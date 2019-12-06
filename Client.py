#Client GUI
import tkinter
import socket
import select
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to the remote server
def connectServer():
    servIP = ipEntry.get()
    port = portEntry.get()

    if len(servIP) > 0 and len(port):
        serverAddress = (str(servIP), int(port))
        sock.connect(serverAddress)
        messagebox.showinfo("Connection", "Connected to central server")
        disButton["state"] = tkinter.NORMAL
        connButton["state"] = tkinter.DISABLED
        
    else:
        messagebox.showerror("Invalid Input", "Please fill in hostname and port number")
        
#Disconnect from the server
def disconnectServer():
    try:
        msg = "QUIT"
        sock.sendall(msg.encode())
        sock.close()
        messagebox.showinfo("Disconnection", "Disconnected from central server")
        connButton["state"] = tkinter.NORMAL
        disButton["state"] = tkinter.DISABLED
    except:
        messagebox.showerror("ERROR", "Failure to disconnect from central server")
        
#Verify that dates are somewhat valid
def verifyDate(date):
    date = date.split("/")
    try:
        if len(date) == 3:
            if int(date[0]) in range(1, 13) and int(date[1]) in range(1, 32)\
            and int(date[2]) in range(2000, 3000):
                return True
        return False
    except:
        return False

#Sent relavant information to the server
#Display the data returned
def getData():
    #Add appropriate dates depending on date range
    try:
        if dateOps.get().upper() == "SINGLE_DAY" and verifyDate(startEntry.get()):
            msg = "GET " + dateOps.get().upper() + " " + startEntry.get()
        elif dateOps.get().upper() == "RANGE" and verifyDate(startEntry.get())\
        and verifyDate(endEntry.get()):
            msg = "GET " + dateOps.get().upper() + " " + startEntry.get() + " " + endEntry.get()
        elif dateOps.get().upper() == "LATEST":
            msg = "GET " + dateOps.get().upper()
        else:
            raise ValueError

        msg = msg + " " + dataOps.get()
        
        #sock.sendall(msg.encode())
        result.insert(tkinter.INSERT, "-> " + msg + "\n")
        
        
        #Receiving data from server
        totalData = []
        while True:
            ready = select.select([sock], [], [], 2)
            if (ready[0]):
                data = sock.recv(1024).decode()
            else:
                break
            totalData.append(data)
        
        #Split the collected data
        dataArray = totalData[0].split(";")
        if dataArray[len(dataArray) - 1] == '':
            dataArray.pop(len(dataArray) - 1)
            
        #Display data on GUI
        for info in dataArray:
            result.insert(tkinter.INSERT, info + "\n")

    except ValueError:
        messagebox.showerror("REQUEST ERROR", """Ensure that:
            Connection is established
            IP address and port number is correct
            Timeframe and data options are correct
            Dates are valid for the program""")

#Clear the output scroll box
def clearData():
    result.delete(1.0, tkinter.END)

#Generates the GUI window        
gui = tkinter.Tk()
gui.title("NANO Temp Client")
gui.geometry("550x450")

##################### CONNECTION #####################
cLabel = tkinter.Label(gui, text="Connection", font=("-weighted bold", 13))
cLabel.grid(column=0, row=0, padx=10, sticky='W',columnspan=6)

#Gets IP adddress of server
ipLabel = tkinter.Label(gui, text="Server IP Address: ")
ipLabel.grid(column=0, row=1)
ipEntry = tkinter.Entry(gui, width=20)
ipEntry.grid(column=1, row=1, sticky='W')

#Gets port number for server connection
portLabel = tkinter.Label(gui, text="Server Port: ")
portLabel.grid(column=0, row=2)
portEntry = tkinter.Entry(gui, width=10)
portEntry.grid(column=1, row=2, sticky='W')

#Connect / Disconnect buttons
connButton = tkinter.Button(gui, text='Connect', width=10, command=connectServer)
connButton.grid(column=2, row=1, pady=10, padx=5)
disButton = tkinter.Button(gui, text='Disconnect', width=10, command=disconnectServer)
disButton['state'] = tkinter.DISABLED
disButton.grid(column=3, row=1, pady=10, padx=5)

##################### GET #####################

gLabel = tkinter.Label(gui, text="Get", font=("-weighted bold", 13))
gLabel.grid(column=0, row=3, pady=10, padx=10, sticky='W', columnspan=6)

#Allows the user to select the timeframe for which to search
dateLabel = tkinter.Label(gui, text="Timeframe: ")
dateLabel.grid(column=0, row=4)
dateOps = ttk.Combobox(gui, width=10)
dateOps['values'] = ("Latest", "Single_Day", "Range")
dateOps.current(0)
dateOps.grid(column=1, row=4)

#Allows the user to choose between temperature units
tempTypeLabel = tkinter.Label(gui, text="Temp Type: ")
tempTypeLabel.grid(column=2, row=4, padx=10)
tempOps = ttk.Combobox(gui, width=10)
tempOps['values'] = ("Celsius", "Fahrenheit")
tempOps.current(0)
tempOps.grid(column=3, row=4)

#Allows the user to select the calculated data to be displayed
optionLabel = tkinter.Label(gui, text="Data Options: ")
optionLabel.grid(column=0, row=5)
dataOps = ttk.Combobox(gui, width=10)
dataOps['values'] = ("All", "AVG", "MAX", "MIN")
dataOps.current(0)
dataOps.grid(column=1, row=5, pady=10)

#The starting and ending dates to be searched for data
startLabel = tkinter.Label(gui, text="Start Date: ")
startLabel.grid(column=0, row=6)
startEntry = tkinter.Entry(gui, width=15)
startEntry.insert(0, "MM/DD/YYYY")
startEntry.grid(column=1, row=6)
endLabel = tkinter.Label(gui, text="End Date: ")
endLabel.grid(column=2, row=6)
endEntry = tkinter.Entry(gui, width=15)
endEntry.insert(0, "MM/DD/YYYY")
endEntry.grid(column=3, row=6)

##################### Results #####################

rLabel = tkinter.Label(gui, text="Results", font=('-weighted bold', 13))
rLabel.grid(column=0, row=7, pady=10, padx=10, sticky='W')

#Area to display the information retrieved from the server
result = scrolledtext.ScrolledText(gui, width=55, height=8)
result.grid(column=0, row=8, padx=30, columnspan=5, rowspan=4)

#Clears the field of previously collected data
clearButton = tkinter.Button(gui, text="Clear", width=10, command=clearData)
clearButton.grid(column=1, row=12, pady=5, padx=10)

#Calls the function to send the selections to the server to retrieve data
searchButton = tkinter.Button(gui, text="Search", width=10, command=getData)
searchButton.grid(column=2, row=12, pady=5, padx=10)

gui.mainloop()