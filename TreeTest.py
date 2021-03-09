from tkinter import *
from tkinter import ttk
from time import sleep
import configparser

# Build window
keywin = Tk()
keywin.title("Ciphers")
keywin.iconbitmap('Icon.ico')
keywin.minsize(210, 250)
keywin.grid_rowconfigure(1, weight=1)
keywin.grid_columnconfigure(0, weight=1)
keywin.grid_columnconfigure(1, weight=1)

# Read Settings
ini_path = "settings.ini"
settings = configparser.ConfigParser()
settings.read(ini_path)
keys = settings.items(section='keys')

selectall = True
def getItem():
    global selectall
    if selectall:
        lb1.selection_set(0, END)
        selBTN.config(text="Sellect None")
        selectall = False
    else:
        lb1.selection_clear(0, END)
        selBTN.config(text="Sellect All")
        selectall = True

importBTN = Button(keywin, text="Import", command=getItem)
importBTN.grid(row=0, column=0, sticky=(N,S,E,W))

exportBTN = Button(keywin, text="Export", command=getItem)
exportBTN.grid(row=0, column=1, sticky=(N,S,E,W))

# Create Frame
boxframe = Frame(keywin)
boxframe.grid(row=1, column=0, columnspan=2, sticky=(N,S,E,W))
boxframe.grid_columnconfigure(0, weight=1)
boxframe.grid_rowconfigure(0, weight=1)
# Create listbox
lb1 = Listbox(boxframe, activestyle='none', selectmode=MULTIPLE)
for i in keys:
    lb1.insert(1, i[0].upper())
lb1.grid(row=0, column=0, sticky=(N,S,E,W))
# Create scrollbar
scrollbar = Scrollbar(boxframe)
scrollbar.grid(row=0, column=1, sticky=(N,S,E,W))
# Config
lb1.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = lb1.yview)

selBTN = Button(keywin, text="Sellect All", command=getItem)
selBTN.grid(row=2, column=0, columnspan=2, sticky=(N,S,E,W))

deleteBTN = Button(keywin, text="Delete", command=getItem)
deleteBTN.grid(row=3, column=0, sticky=(N,S,E,W))

genBTN = Button(keywin, text="Generate", command=getItem)
genBTN.grid(row=3, column=1, sticky=(N,S,E,W))

keywin.mainloop()
