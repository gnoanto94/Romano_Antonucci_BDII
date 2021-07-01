import tkinter as tk
import pymongo
import traceback

from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from pymongo.message import _query_compressed
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

    # Add the data table

    global tree
    tree = ttk.Treeview(window, columns=('1', '2', '3','4','5'), show='headings')

    
    tree.heading('1', text='Attack')
    tree.heading('2', text='Year')
    tree.heading('3', text='Organization Type')
    tree.heading('4', text='Country')
    tree.heading('5', text='Attack Vector')

    tree.grid(row=0, column=0, sticky='NSEW')
    
    # Inizializziamo in maniera tale da vedere tutti gli elementi già da subito.
    view_all()

    
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='NS')

    

    # Add query buttons

    b1 = tk.Button(window, text="View all", height=2, width=15, command=view_all) #creating buttons for the various operations. Giving it a name and assigning a particular command to it. 
    b2 = tk.Button(window, text="Search entry", height=2, width=15) #, command=search_command)
    b3 = tk.Button(window, text="Add entry", height=2, width=15) #, command=add_command)
    b4 = tk.Button(window, text="Update selected", height=2,width=15) #, command=update_command)
    b5 = tk.Button(window, text="Delete selected", height=2, width=15) #, command=delete_command)
    b6 = tk.Button(window, text="SearchByCountry", height=2,width=15, command=attack_by_exact_country)

    b1.grid(sticky='W')
    b2.grid(sticky='W')
    b3.grid(sticky='W')
    b4.grid(sticky='W')
    b5.grid(sticky='W')
    b6.grid(sticky='W')


    # Add text field for the queries
    global field

    field = tk.Text(window, height=5, width=40)
    field.grid(sticky='W')

    window.geometry("1200x800")
    #window.mainloop()




def view_all():

    stampa(collection.find())



def stampa(attacks):

    item_count = len(tree.get_children())
    
    #se non faccio questo controllo e non c'è nulla nella treeview, si ha exception
    if item_count > 0:
        tree.delete(*tree.get_children())

    for attack in attacks:

        attack = list(attack.values())[1:len(attack)]
        tree.insert('', tk.END, values=attack)



def attack_by_exact_country():
    country = field.get("1.0", "end-1c") #prende dal primo al penultimo carattere, altrimenti considera anche newline
    attacks = collection.find({"Country":country})
    stampa(attacks)




    






class App:

    def __init__(self, master):
        master.report_callback_exception = self.login_error
        self.frame = tk.Frame(master)
        self.frame.pack()

    def login_error(self, *args):
        traceback.format_exception(*args)
        showerror('Errore', 'Le credenziali inserite non sono valide. Riprovare.', parent = window)

        
global window 

window = tk.Tk(className="login")
window.geometry("300x300")
window.eval('tk::PlaceWindow . center')

usr_label = tk.Label(window, text = "Username: ")
usr_label.place(x = 50, y = 20)
 
username = tk.Entry(window, width = 35)
username.place(x = 150, y = 20, width = 100)
username.insert(-1, "admin")

pwd_label = tk.Label(window, text ="Password: ")
pwd_label.place(x = 50, y = 50)
 
password = tk.Entry(window, show = "*", width = 35)
password.place(x = 150, y = 50, width = 100)
password.insert(-1, "oNWZDGjCxDHtnp8o")
 
login_button = tk.Button(window, text = "Login", command = login_btn)
login_button.place(x = 150, y = 135, width = 55)

app = App(window)
window.mainloop()