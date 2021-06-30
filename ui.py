import tkinter as tk
import pymongo
import traceback

from tkinter.messagebox import showerror, showinfo
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure





def login_btn():
    """Function used by the login button to start the database login process"""

    db_login(username.get(), password.get())


def db_login(usr, pwd):
    """ Given a username and a password, this function attempts a login to the database."""

    client = MongoClient()
    client = pymongo.MongoClient("mongodb+srv://"+usr+":"+pwd+"@cluster0.bkvuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    try:
        # The ismaster command is cheap and does not require authentication, so we can use it to verify whether the user has successfully completed the login process
        client.admin.command('ismaster')

    except ConnectionFailure:
        pass
    
    showinfo('Login successful', 'Cose a caso per dire che il login è andato a buon fine', parent = window)

    global db, collection

    db = client.attacks
    collection = db.data

    window.destroy()
    create_db_window()
   


def create_db_window():
    """This function creates the database-interaction window"""

    window = tk.Tk(className="database")
    window.geometry("1200x800")


    l1 = tk.Label(window, text="QUERY") #creating input labels in the window
    l1.grid(row=0, column=0) #determining size of the input grid for these labels

    title_text = tk.StringVar()
    e1 = tk.Entry(window, textvariable=title_text) #taking input from the user in the grid and storing it in a string variable
    e1.grid(row=0, column=1)

    list1 = tk.Listbox(window, height=25, width=65) #creating the list space to display all the rows of the table
    list1.grid(row=2, column=0, rowspan=6, columnspan=2) #determining the size

    sb1 = tk.Scrollbar(window) #creating a scrollbar for the window to scroll through the list entries
    sb1.grid(row=2, column=2, rowspan=6)

    list1.configure(yscrollcommand=sb1.set) #configuring the scroll function for the scrollbar object sb1
    sb1.configure(command=list1.yview)

    b1 = tk.Button(window, text="View all", width=12) #, command=view_command) #creating buttons for the various operations. Giving it a name and assigning a particular command to it. 
    b1.grid(row=2, column=3) #size of the button

    b2 = tk.Button(window, text="Search entry", width=12) #, command=search_command)
    b2.grid(row=3, column=3)

    b3 = tk.Button(window, text="Add entry", width=12) #, command=add_command)
    b3.grid(row=4, column=3)

    b4 = tk.Button(window, text="Update selected", width=12) #, command=update_command)
    b4.grid(row=5, column=3)

    b5 = tk.Button(window, text="Delete selected", width=12) #, command=delete_command)
    b5.grid(row=6, column=3)

    b6 = tk.Button(window, text="Close", width=12) #, command=window.destroy)
    b6.grid(row=7, column=3)





    






class App:

    def __init__(self, master):
        master.report_callback_exception = self.login_error
        self.frame = tk.Frame(master)
        self.frame.pack()

    def login_error(self, *args):
        err = traceback.format_exception(*args)
        showerror('Errore', 'Le credenziali inserite non sono valide. Riprovare.', parent = window)

        
global window 

window = tk.Tk(className="login")
window.geometry("300x300")
window.eval('tk::PlaceWindow . center')

usr_label = tk.Label(window, text = "Username -")
usr_label.place(x = 50, y = 20)
 
username = tk.Entry(window, width = 35)
username.place(x = 150, y = 20, width = 100)
username.insert(-1, "admin")

pwd_label = tk.Label(window, text ="Password -")
pwd_label.place(x = 50, y = 50)
 
password = tk.Entry(window, show = "*", width = 35)
password.place(x = 150, y = 50, width = 100)
password.insert(-1, "oNWZDGjCxDHtnp8o")
 
login_button = tk.Button(window, text = "Login", command = login_btn)
login_button.place(x = 150, y = 135, width = 55)

app = App(window)
window.mainloop()