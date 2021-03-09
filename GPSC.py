# Import modules
from tkinter import *
from tkinter import filedialog, ttk, messagebox, colorchooser
from string import printable
from random import shuffle
import configparser
import os

# Create Window 
root = Tk()
root.eval('tk::PlaceWindow . center')
root.minsize(500, 250)
root.title("General Purpose Substitution Cipher 3.0")
root.iconbitmap('Icon.ico')

# Read Settings
ini_path = "settings.ini"
settings = configparser.ConfigParser()
settings.read(ini_path)
colorBG = settings['prefences']['colorBackground']
colorFG = settings['prefences']['colorForground']
key_names = settings.options('keys')
key_names = [k.upper() for k in key_names]

# Set Inital Varibles
filesave = ""
mesEnc = False
current_key = StringVar()
current_key.set(key_names[0])
lastUsed = key_names[0]

def update_ini():
    file = open(ini_path, "w")
    settings.write(file)
    file.close()

# New file 
def new(e=False):
    global filesave
    result = messagebox.askyesnocancel("Save Changes", "Do you want to save your changes?")
    if result != None:
        if result == True:
            save()
        text_box.delete(1.0, END)
        info_bar.config(text=("New message").center(34))
        filesave = ""
        button.configure(text="Encrypt")
        edit_menu.entryconfig(3, label="Encrypt")
        mesEnc = False

# Open file
def open_file(e=False):
    global filesave
    global mesEnc
    info_bar.config(text=("Open file").center(34))
    result = messagebox.askyesnocancel("Save Changes", "Do you want to save your changes?")
    if result != None:
        if result == True:
            save()
        info_bar.config(text=("Open file").center(34))
        filename = filedialog.askopenfilename(initialdir="C:/Users/Harbaughs/Documents/", title="Open", filetypes=(("Encrypted Messages", "*.scme"),("Text Documents", "*.txt"),("All Files", "*.*")))
        if filename:
            file = open(filename, "r")
            newtext = file.read()
            file.close()
            text_box.delete(1.0, END)
            text_box.insert(END, newtext)
            filesave = filename
            if os.path.splitext(filename)[1] == ".scme":
                button.configure(text="Decrypt")
                edit_menu.entryconfig(3, label="Decrypt")
                cipher_menu.config(state='disabled')
                mesEnc = True
            else:
                button.configure(text="Encrypt")
                edit_menu.entryconfig(3, label="Encrypt")
                cipher_menu.config(state='normal')
                mesEnc = False
        else:
            info_bar.config(text=("Canceled open file").center(34))

# Save as file      
def save_as_file(e=False):
    global filesave
    if mesEnc:
        filename = filedialog.asksaveasfilename(defaultextension=".scme", initialdir="C:/Users/Harbaughs/Documents/", title="Save As", filetypes=(("Encrypted Messages", "*.scme"),("All Files", "*.*")))
    else:
        filename = filedialog.asksaveasfilename(defaultextension=".txt", initialdir="C:/Users/Harbaughs/Documents/", title="Save As", filetypes=(("Text Documents", "*.txt"),("All Files", "*.*")))
    if filename:
        file = open(filename, "w")
        file.write(text_box.get(1.0, END)[:-1])
        file.close()
        info_bar.config(text=("Saved file").center(34))
        filesave = filename
    else:
        info_bar.config(text=("Canceled save file").center(34))

# Save file
def save(e=False):
    global filesave
    global mesEnc
    if filesave:
        if mesEnc:
            filename = os.path.splitext(filesave)[0] + ".scme"
        else:
            filename = os.path.splitext(filesave)[0] + ".txt"
        os.rename(filesave, filename)
        filesave = filename
        file = open(filesave, "w")
        file.write(text_box.get(1.0, END)[:-1])
        file.close()
        info_bar.config(text=("Saved file").center(34))
    else:
        save_as_file()

# Undo box
def undo(e=False):
    text_box.edit_undo()

# Redo box
def redo(e=False):
    text_box.edit_redo()

def cut(e=False):
    if text_box.tag_ranges(SEL):
        root.clipboard_clear()
        root.clipboard_append(text_box.selection_get())
        text_box.delete("sel.first", "sel.last")
    
def copy(e=False):
    if text_box.tag_ranges(SEL):
        root.clipboard_clear()
        root.clipboard_append(text_box.selection_get())
    
def paste(e=False):
    if not e: # Check if its a keyboard event
        if text_box.tag_ranges(SEL):
            text_box.delete("sel.first", "sel.last")
        text_box.insert(text_box.index(INSERT), root.clipboard_get())
   
def select_all(e=False):
    text_box.focus_set()
    text_box.tag_add(SEL, 1.0, END)

def cipher(encipher, text, keyname):
    key = bytes.fromhex(settings.get("keys", keyname)).decode("utf-8")
    newtext = ""
    invaidChars = ""
    for x in text:
        cn = ord(x)
        if 32 < cn < 127:
            if encipher:
                newtext += chr(key.index(x) + 31)
            else:
                newtext += key[cn - 31]
        elif cn == 10:
            # Preserve New Lines
            newtext += "\n"
        elif cn == 32:
            # Perserve Spaces
            newtext += " "
        else:
            invaidChars += x
    if invaidChars:
        messagebox.showerror("Encipherment Error", f"The text contains the folowing unsuported characters:\n{invaidChars}.\n Please remove them before trying again.")
        return false
    else:
        return newtext  

# Ciper operation
def apply_cipher(e=False):
    global mesEnc
    newtext = cipher(mesEnc, text_box.get(1.0, END)[:-1], current_key.get())
    if newtext:
        text_box.delete(1.0, END)
        text_box.insert(1.0, newtext)
        # Update texts
        if mesEnc:
            info_bar.config(text=("Decrypted message").center(34))
            button.configure(text="Encrypt")
            cipher_menu.entryconfig(2, label="Encrypt")
            cipher_drop.config(state='normal')
            mesEnc = False
        else:
            info_bar.config(text=("Encrypted message").center(34))
            button.configure(text="Decrypt")
            cipher_menu.entryconfig(2, label="Decrypt")
            cipher_drop.config(state='disabled')
            mesEnc = True

def ptype(event):
    print(event)
    type = cipher_menu.get()
    info_bar.config(text=type.center(34))
    messagebox.showinfo("Python Cipher", f"Set cipher to {type}")
    
def sel_colorBG():
    global colorBG
    colorBG = colorchooser.askcolor(title ="Choose Background Color")[1]
    settings['prefences']['colorBackground'] = colorBG
    root.config(bg=colorBG)
    info_bar.config(fg=colorBG)
    text_box.config(fg=colorBG, selectbackground=colorBG)
    update_ini()
    
def sel_colorFG():
    global colorFG
    colorFG = colorchooser.askcolor(title ="Choose Forground Color")[1]
    settings['prefences']['colorForground'] = colorFG
    info_bar.config(bg=colorFG)
    text_box.config(bg=colorFG, selectforeground=colorFG)
    update_ini()
    
def switch_key(keyname):
    global mesEnc
    key_names = settings.options('keys')
    key_names = [k.upper() for k in key_names]
    cipher_menu.config(value=key_names)
    if mesEnc:
        text = text_box.get(1.0, END)[:-1]
        newtext = cipher(False, text, lastUsed)
    current_key.set(keyname)


# ===== Cipher Toplevel ===== #

def buildCipherBox():

    # Create ciphers toplevel
    keywin = Toplevel()
    keywin.grab_set()
    keywin.focus_force()
    keywin.geometry(f'+{root.winfo_x()+20}+{root.winfo_y()+20}')
    keywin.title("Ciphers")
    keywin.iconbitmap('Icon.ico')
    keywin.minsize(210, 250)
    keywin.resizable(False, False)
    keywin.grid_rowconfigure(1, weight=1)
    keywin.grid_columnconfigure(0, weight=1)
    keywin.grid_columnconfigure(1, weight=1)
    
    def generate():
        char_list = sorted(list(printable))[6:]
        shuffle(char_list)
        cipher = ''.join(char_list)
        cipher = ' ' + cipher # Add space at begining
        name = ''
        name_len = 5
        for c in cipher:
            if name_len > 2:
                if c.isalpha():
                    name += c.upper()
                    name_len -= 1
            elif name_len == 2:
                if c.isalpha():
                    name += c.upper()
                    name += "-"
                    name_len -= 1
            elif name_len == 1:
                if c.isnumeric():
                    name += c
                    name_len -= 1
            elif name_len == 0:
                if c.isnumeric():
                    name += c
                    break
        settings.set('keys', name, cipher.encode('utf-8').hex())
        update_ini()
        lb1.insert(END, name)
        lb1.selection_clear(0, END)
        lb1.selection_set(END)
        lb1.see(END)
        key_names = settings.options('keys')
        key_names = [k.upper() for k in key_names]
        cipher_drop.config(value=key_names)

    # Import Button
    importBTN = Button(keywin, text="Import")
    importBTN.grid(row=0, column=0, sticky=(N,S,E,W), padx=5, pady=5)
    
    # Export Button
    exportBTN = Button(keywin, text="Export")
    exportBTN.grid(row=0, column=1, sticky=(N,S,E,W), padx=5, pady=5)
    
    # Create Frame
    boxframe = Frame(keywin, borderwidth=2, relief="sunken")
    boxframe.grid(row=1, column=0, columnspan=2, sticky=(N,S,E,W), padx=5, pady=5)
    boxframe.grid_columnconfigure(0, weight=1)
    boxframe.grid_rowconfigure(0, weight=1)
    
    # Create listbox
    lb1 = Listbox(boxframe, activestyle='none', selectmode=MULTIPLE, borderwidth=0)
    lb1.grid(row=0, column=0, sticky=(N,S,E,W))
    for i in key_names:
        lb1.insert(1, i)
    
    # Create scrollbar
    scrollbar = Scrollbar(boxframe)
    scrollbar.grid(row=0, column=1, sticky=(N,S,E,W))
    
    # Config scrollbar
    lb1.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = lb1.yview)
    
    # Delete Button
    deleteBTN = Button(keywin, text="Delete")
    deleteBTN.grid(row=3, column=0, sticky=(N,S,E,W), padx=5, pady=5)
    
    # Generate Button
    genBTN = Button(keywin, text="Generate", command=generate)
    genBTN.grid(row=3, column=1, sticky=(N,S,E,W), padx=5, pady=5) 


# ==== Menu Bar ==== #

# Menu Bar
menubar = Menu(root)
root.config(menu=menubar)

# File menu
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new, accelerator="Ctrl+N")
root.bind('<Control-n>', new)
file_menu.add_command(label="Open...", command=open_file, accelerator="Ctrl+O")
root.bind('<Control-o>', open_file)
file_menu.add_command(label="Save", command=save, accelerator="Ctrl+S")
root.bind('<Control-s>', save)
file_menu.add_command(label="Save As...", command=save_as_file, accelerator="Ctrl+Shift+S")
root.bind('<Control-S>', save_as_file)
file_menu.add_separator()
cipher_submenu = Menu(file_menu, tearoff=0)
file_menu.add_cascade(label="Cipher Key", menu=cipher_submenu)
cipher_submenu.add_command(label="Import", command=apply_cipher)
cipher_submenu.add_command(label="Export Current", command=apply_cipher)
cipher_submenu.add_command(label="Export All", command=apply_cipher)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Edit menu
edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
root.bind('<Control-z>', undo)
edit_menu.add_command(label="Redo", command=redo, accelerator="Ctrl+Y")
root.bind('<Control-y>', redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
root.bind('<Control-x>', cut)
edit_menu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
root.bind('<Control-c>', copy)
edit_menu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
root.bind('<Control-v>', paste)
edit_menu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
root.bind('<Control-a>', select_all)

# Cipher menu
cipher_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Cipher", menu=cipher_menu)
cipher_menu.add_command(label="Edit Keys", command=buildCipherBox, accelerator="Ctrl+K")
root.bind('<Control-k>', buildCipherBox)
cipher_menu.add_separator()
cipher_menu.add_command(label="Encrypt", command=apply_cipher, accelerator="Ctrl+E")
root.bind('<Control-e>', apply_cipher)

# Preferences menu
setting_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Preferences", menu=setting_menu)
color_submenu = Menu(setting_menu, tearoff=0)
color_submenu.add_command(label="Background", command=sel_colorBG)
color_submenu.add_command(label="Forground", command=sel_colorFG)
setting_menu.add_cascade(label="Color", menu=color_submenu)
def printfo():
    print(root.winfo_x(), root.winfo_y())
setting_menu.add_command(label="More...", command=printfo)

# ==== Dialog Styling ==== #

# Resizable configs
root.config(bg=colorBG, padx=10, pady=10)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# ===== Dialog Wigets ===== #

# Info bar
info_bar = Label(root, bg=colorFG, fg=colorBG, text="Only printable characters allowed!")
info_bar.grid(row=0, column=0, sticky=(N,E,S,W))

# Cipher menu
cipher_drop = ttk.Combobox(root, state="readonly", textvariable=current_key, value=key_names, width=10)
cipher_drop.bind("<<ComboboxSelected>>", ptype)
cipher_drop.grid(row=0, column=1, sticky=(N,S), padx=10)

# Cipher button
button = Button(root, text="Encrypt", padx=15, command=apply_cipher)
button.grid(row=0, column=2, sticky=(N,S))

# Text box
text_box = Text(root, width=60, height=20, padx=4, pady=4, font=("Lucida Console", 10), fg=colorBG, bg=colorFG, selectforeground=colorFG, selectbackground=colorBG, undo=True)
text_box.grid(row=1, column=0, columnspan=3, pady=(10,0), sticky=(N,E,S,W))
text_box.insert(1.0, 'Type in your secret message or\nclick the "Chose file" button to open a extenal file.')


# Main loop
root.mainloop()
