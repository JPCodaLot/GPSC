# Import modules
from tkinter import *
from tkinter import filedialog, ttk, messagebox, colorchooser
from string import printable
from random import shuffle
import configparser
import json

# Create appinfo dict
appinfo = {
    "name":"GPSC",
    "version":{
        "major":2,
        "minor":0,
        "patch":0
    }
}

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
        cipher_menu.entryconfig(3, label="Encrypt")
        mesEnc = False

# Open file
def open_file(e=False):

    # Get Globals
    global filesave
    global mesEnc
    
    # Save Changes
    result = messagebox.askyesnocancel("Save Changes", "Do you want to save your changes?")
    if result == None:
        return False
    elif result == True:
        save()
   
    # Read File
    info_bar.config(text=("Open file").center(34))
    filename = filedialog.askopenfilename(initialdir="documents", title="Open", filetypes=(("Messages", "*.gscm"),))
    if not filename:
        info_bar.config(text=("Canceled open file").center(34))
        return False
    file = open(filename, "r")
    gscm = json.loads(file.read())
    file.close()
    
    # Test For vailidity
    try:
        if gscm["app"]["name"] != appinfo["name"]:
            messagebox.showerror("Import Error", "Incorect File Type! ID#1")
        elif gscm["datatype"] != "General Susitution Cipher Message":
            messagebox.showerror("Import Error", "Incorect File Type! ID#2")
        elif gscm["app"]["version"]["major"] > appinfo["version"]["major"]:
            ver = gscm["app"]["version"]
            messagebox.showerror("Import Error", f'You need version {ver["major"]}.{ver["minor"]}.{ver["patch"]} to open this message!')
        elif gscm["app"]["version"]["major"] < appinfo["version"]["major"]:
            messagebox.showerror("Import Error", "This message was made in a earlier version and can not be opened!")
        else:
            
            # Look for key
            cipher_drop.config(state='readonly')
            if gscm["state"] == "encrypted":
                if settings.has_option("keys", gscm["key"]):
                    current_key.set(gscm["key"].upper())
                    cipher_drop.config(state='disabled')
                else:
                    result = messagebox.askyesnocancel("Message Key", "You do not have the key that this message was encrypted in. Would you like to open it anyways?")
                    if result != True:
                        info_bar.config(text=("Canceled open file").center(34))
                        return False

            # Insert File
            text_box.delete(1.0, END)
            text_box.insert(END, gscm["data"])
            filesave = filename
            if gscm["state"] == "encrypted":
                button.configure(text="Decrypt")
                cipher_menu.entryconfig(3, label="Decrypt")
                mesEnc = True
            else:
                button.configure(text="Encrypt")
                cipher_menu.entryconfig(3, label="Encrypt")
                mesEnc = False
            info_bar.config(text=("Opened file").center(34))
    except KeyError:
        messagebox.showerror("Import Error", "Incorect File Type! ID#3")

# Save as file
def save_as_file(e=False):
    global filesave
    filename = filedialog.asksaveasfilename(defaultextension=".gscm", initialdir="documents", title="Save As", filetypes=(("Encrypted Messages", "*.gscm"),))
    if filename:
        filesave = filename
        save()
    else:
        info_bar.config(text=("Canceled save file").center(34))

# Save file
def save(e=False):
    global filesave
    global mesEnc
    if filesave:
        file = open(filesave, "w")
        pydict = {
            "app":appinfo,
            "datatype":"General Susitution Cipher Message",
            "key":current_key.get(),
            "state":"encrypted" if mesEnc else "normal",
            "data":text_box.get(1.0, END)[:-1]
        }
        sckj = json.dumps(pydict, indent=2) + "\n"
        file.write(sckj)
        file.close()
        info_bar.config(text=("Saved file").center(34))
    else:
        save_as_file()

# Undo box
def undo(e=False):
    try:
        text_box.edit_undo()
    except TclError:
        edit_menu.entryconfig(0, state=DISABLED)
    else:
        edit_menu.entryconfig(1, state=NORMAL)

# Redo box
def redo(e=False):
    try:
        text_box.edit_redo()
    except TclError:
        edit_menu.entryconfig(1, state=DISABLED)
    else:
       edit_menu.entryconfig(0, state=NORMAL)

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
            cipher_drop.config(state='readonly')
            mesEnc = False
        else:
            info_bar.config(text=("Encrypted message").center(34))
            button.configure(text="Decrypt")
            cipher_menu.entryconfig(2, label="Decrypt")
            cipher_drop.config(state='disabled')
            mesEnc = True

def ptype(event):
    type = cipher_drop.get()
    info_bar.config(text=f'Set cipher key to {type}'.center(34))

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

def buildCipherBox(e=False):

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

    def importKeys():
        global appinfo
        filename = filedialog.askopenfilename(initialdir="documents", title="Import Cipher Keys", filetypes=(("Cipher Keys", "*.gsck"),))
        if filename:
            file = open(filename, "r")
            sckj = json.loads(file.read())
            file.close()
            if sckj["app"]["name"] != appinfo["name"]:
                messagebox.showerror("Import Error", "Incorect File Type!")
            elif sckj["datatype"] != "Susitution Cipher Keys":
                messagebox.showerror("Import Error", "Incorect File Type!")
            elif sckj["app"]["version"]["major"] > appinfo["version"]["major"]:
                ver = sckj["app"]["version"]
                messagebox.showerror("Import Error", f'You need version {ver["major"]}.{ver["minor"]}.{ver["patch"]} to open these keys!')
            elif sckj["app"]["version"]["major"] < appinfo["version"]["major"]:
                messagebox.showerror("Import Error", "These keys were made in a earlier version and can not be opened!")
            else:
                listend = lb1.size()
                for k, v in sckj["data"].items():
                    settings.set('keys', k, v)
                refresh()
                lb1.selection_clear(0, END)
                lb1.see(listend)
                lb1.selection_set(listend, END)
                messagebox.showinfo("Import", "The keys were successfully imported.")

    def exportKeys():
        filename = filedialog.asksaveasfilename(defaultextension=".gsck", initialdir="documents", title="Save As", filetypes=(("Cipher Keys File", "*.gsck"),))
        if filename:
            file = open(filename, "w")
            pydict = {
                "app":appinfo,
                "datatype":"Susitution Cipher Keys",
                "data":dict(settings.items("keys"))
            }
            sckj = json.dumps(pydict, indent=2) + "\n"
            file.write(sckj)
            file.close()

    def refresh():
        update_ini()
        lb1.delete(0, END)
        key_names = settings.options('keys')
        key_names = [k.upper() for k in key_names]
        lb1.insert(END, *key_names)
        cipher_drop.config(value=key_names)
        current_key.set(key_names[0])

    def delete():
        cersel = lb1.curselection()
        sellen = len(cersel)
        if sellen > 0:
            result = messagebox.askyesnocancel("Delete Comfiration", f"Are you sure you want to delete {f'these {sellen} keys' if sellen > 1 else 'this key'}?")
            if result == True:
                for i in cersel:
                    key_name = lb1.get(0,END)[i]
                    if mesEnc and key_name == current_key.get():
                        apply_cipher()
                    settings.remove_option("keys", key_name)
                if sellen == lb1.size():
                    default = settings.items("default-keys")[0]
                    settings.set("keys", default[0], default[1])
                refresh()

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
        refresh()
        lb1.selection_clear(0, END)
        lb1.see(END)
        lb1.selection_set(END)

    # Import Button
    importBTN = Button(keywin, text="Import", command=importKeys)
    importBTN.grid(row=0, column=0, sticky=(N,S,E,W), padx=5, pady=5)

    # Export Button
    exportBTN = Button(keywin, text="Export", command=exportKeys)
    exportBTN.grid(row=0, column=1, sticky=(N,S,E,W), padx=5, pady=5)

    # Create Frame
    boxframe = Frame(keywin, borderwidth=2, relief="sunken")
    boxframe.grid(row=1, column=0, columnspan=2, sticky=(N,S,E,W), padx=5, pady=5)
    boxframe.grid_columnconfigure(0, weight=1)
    boxframe.grid_rowconfigure(0, weight=1)

    # Create listbox
    lb1 = Listbox(boxframe, activestyle='none', selectmode=MULTIPLE, borderwidth=0)
    lb1.grid(row=0, column=0, sticky=(N,S,E,W))
    refresh()

    # Create scrollbar
    scrollbar = Scrollbar(boxframe)
    scrollbar.grid(row=0, column=1, sticky=(N,S,E,W))

    # Config scrollbar
    lb1.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = lb1.yview)

    # Delete Button
    deleteBTN = Button(keywin, text="Delete", command=delete)
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
file_menu.add_command(label="Exit", command=root.quit, accelerator="Alt+F4")

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
color_submenu.add_command(label="Foreground", command=sel_colorFG)
setting_menu.add_cascade(label="Color", menu=color_submenu)

# ==== Dialog Styling ==== #

# Resizable configs
root.config(bg=colorBG, padx=10, pady=10)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# ===== Dialog Wigets ===== #

# Info bar
info_bar = Label(root, bg=colorFG, fg=colorBG, text="Only printable characters allowed!")
info_bar.grid(row=0, column=0, sticky=(N,E,S,W))

# Cipher dropdown
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
