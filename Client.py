#Client GUI
import tkinter
import socket
import select
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    result.insert(tkinter.INSERT, "-> GET\n")
    
def clearData():
    result.delete(1.0, tkinter.END)
        
gui = tkinter.Tk()
gui.title("NANO Temp Client")
gui.geometry("550x450")

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
gLabel.grid(column=0, row=3, pady=10, padx=10, sticky='W', columnspan=6)

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

optionLabel = tkinter.Label(gui, text="Data Options: ")
optionLabel.grid(column=0, row=5)
allV = tkinter.Variable()
allOp = tkinter.Checkbutton(gui, text='All', variable=allV, height=2)
allOp.grid(column=1, row=5)
maxV = tkinter.Variable()
maxOp = tkinter.Checkbutton(gui, text='MAX', variable=maxV, height=2)
maxOp.grid(column=2, row=5)
avgV = tkinter.Variable()
avgOp = tkinter.Checkbutton(gui, text='AVG', variable=avgV, height=2)
avgOp.grid(column=3, row=5)
minV = tkinter.Variable()
minOp = tkinter.Checkbutton(gui, text='MIN', variable=minV, height=2)
minOp.grid(column=4, row=5)

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

rLabel = tkinter.Label(gui, text="Results", font=('-weighted bold', 13))
rLabel.grid(column=0, row=7, pady=10, padx=10, sticky='W')

result = scrolledtext.ScrolledText(gui, width=55, height=8)
result.grid(column=0, row=8, padx=30, columnspan=5, rowspan=4)

clearButton = tkinter.Button(gui, text="Clear", width=10, command=clearData)
clearButton.grid(column=1, row=12, pady=5, padx=10)
searchButton = tkinter.Button(gui, text="Search", width=10, command=getData)
searchButton.grid(column=2, row=12, pady=5, padx=10)

gui.mainloop()