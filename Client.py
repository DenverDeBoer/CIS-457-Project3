import tkinter
import socket
import select
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectServer():
    servIP = serverHostText.get()
    port = portText.get()

    if len(servIP) > 0 and len(port):
        serverAddress = (str(servIP), int(port))
        sock.connect(serverAddress)
        messagebox.showinfo("Connection", "Connected to central server")
        disButton["state"] = tkinter.NORMAL
        connButton["state"] = tkinter.DISABLED
        
    else:
        messagebox.showerror("Invalid Input", "Please fill in hostname and port number")
        
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
        
def getData():
    try:
        option = getOps.get()
        
        if rangeOps == "RANGE":
            start = startDate.get()
            end = endDate.get()
        elif rangeOps == "SINGLE DAY":
            start = startDate.get()
        
        msg = "GET " + option
        
        if option == "MAX":
            msg = msg + " " + start
        elif option == "AVG":
            msg = msg + " " + start
        elif option == "MIN":
            msg = msg + " " + start
            
    except:
        messagebox.showerror("ERROR", "Failure to retrieve data")
        
gui = tkinter.Tk()
gui.title("NANO Temp Client")
gui.geometry("500x500")

##################### CONNECTION #####################
cLabel = tkinter.Label(gui, text="Connection", font=("-weighted bold", 13))
cLabel.grid(column=0, row=0, padx=10, sticky='W',columnspan=6)

ipLabel = tkinter.Label(gui, text="Server IP Address: ")
ipLabel.grid(column=0, row=1)
ipEntry = tkinter.Entry(gui, width=20)
ipEntry.grid(column=1, row=1, sticky='W')

portLabel = tkinter.Label(gui, text="Server Port: ")
portLabel.grid(column=0, row=2)
portEntry = tkinter.Entry(gui, width=10)
portEntry.grid(column=1, row=2, sticky='W')

connButton = tkinter.Button(gui, text='Connect', width=10, command=connectServer)
connButton.grid(column=2, row=1, pady=10, padx=5)
disButton = tkinter.Button(gui, text='Disconnect', width=10, command=disconnectServer)
disButton['state'] = tkinter.DISABLED
disButton.grid(column=3, row=1, pady=10, padx=5)

gLabel = tkinter.Label(gui, text="Get", font=("-weighted bold", 13))
gLabel.grid(column=0, row=3, pady=15, padx=10, sticky='W', columnspan=6)

dateLabel = tkinter.Label(gui, text="Timeframe: ")
dateLabel.grid(column=0, row=4)
dateOps = ttk.Combobox(gui, width=10)
dateOps['values'] = ("Latest", "Single Day", "Range")
dateOps.current(0)
dateOps.grid(column=1, row=4)

tempTypeLabel = tkinter.Label(gui, text="Temp Type: ")
tempTypeLabel.grid(column=2, row=4, padx=10)
tempOps = ttk.Combobox(gui, width=10)
tempOps['values'] = ("Celsius", "Fahrenheit")
tempOps.current(0)
tempOps.grid(column=3, row=4)

choicesLabel = tkinter.Label(gui, "Choose what to Display: ")
choicesLabel.grid(column=0, row=5)

gui.mainloop()