# Import modules
from tkinter import *
from tkinter import filedialog

# Set varibles
root = Tk()
root.eval('tk::PlaceWindow . center')
root.title("General Purpose Substitution Cipher 2.0")
root.iconbitmap('Icon.ico')
cipher1 = '''
 .&T?zpYJ[h_"C4ufQwWI('M@^q9FdnOlN>8B=`SAx71/*btv}gj{|,6y%\<:k-X3$2~Ra5cr+LU#Z)iPHsV!eDmG]Ko;E0
'''

# Clear the text box
def clear():
    my_box.delete(1.0, END)
    info_bar.config(text=("Cleared text box").center(34))

# Open file
def open_file():
    info_bar.config(text=("Open file").center(34))
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("text files", "*.txt"),("all files", "*.*")))
    if root.filename == '':
        info_bar.config(text=("Canceled open file").center(34))
    else:
        file = open(root.filename, "r")
        newtext = file.read()
        file.close()
        clear()
        my_box.insert(END, newtext)

# Ciper operation
def cipher(mode):
    newtext = ""
    text = my_box.get(1.0, END)[:-1]
    for x in text:
        cn = ord(x)
        if 32 <= cn <= 126:
            if mode == "decrypt":
                newtext += chr(cipher1.index(x) + 31)
            else:
                newtext += cipher1[cn - 31]
            
        elif cn == 10:
            # Preserve New Lines
            newtext += "\n"
        else:
            # Perserve Spaces
            newtext += " "
    
    clear()
    my_box.insert(END, newtext)
    info_bar.config(text=(mode + "ed message").center(34))

def encrypt():
    cipher("encrypt")

def decrypt():
    cipher("decrypt")

# ===== Dialog Wigets ===== #
color1 = '#ffffff'
color2 = '#000000'
# Backround
root.config(bg=color2, padx=10, pady=10)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
# Info bar
info_bar = Label(root, bg=color1, fg=color2, text="Only printable characters allowed!")
info_bar.grid(row=2, column=0, columnspan=2, sticky=(N,E,S,W))
# Top buttons
btn_encrypt = Button(root, text="Encrypt", command=encrypt).grid(row=0, column=0, sticky=(N,E,S,W))
btn_decrypt = Button(root, text="Decrypt", command=decrypt).grid(row=0, column=1, sticky=(N,E,S,W))
# Text box
my_box = Text(root, width=60, height=20, padx=4, pady=4, font=("Lucida Console", 10), selectbackground=color2, undo=True, )
my_box.grid(row=1, column=0, columnspan=2, pady=10, sticky=(N,E,S,W))
my_box.insert(1.0, 'Type in your secret message or\nclick the "Chose file" button to open a extenal file.')

# Main loop
root.mainloop()
