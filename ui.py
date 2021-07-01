import tkinter as tk
import pymongo
import traceback

from tkinter import ttk
from tkinter.messagebox import NO, showerror
from tkinter.constants import END
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure





def login_btn():
    """Function used by the login button to start the database login process"""

    db_login(username.get(), password.get())




def db_login(usr, pwd):
    """ Given a username and a password, this function attempts a login to the database."""

    client = MongoClient()
    client = pymongo.MongoClient("mongodb+srv://"+usr+":"+pwd+"@cluster0.bkvuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    success = 0

    try:
        # The ismaster command is cheap and does not require authentication, so we can use it to verify whether the user has successfully completed the login process
        client.admin.command('ismaster')
        success = 1

    except ConnectionFailure:
        pass
    
    if success!=1:
        showerror('Login Error', 'Cose a caso per dire che il login non è andato a buon fine', parent = window)

    global db, collection

    db = client.ksprojects
    collection = db.data

    window.destroy()
    create_db_window()





def create_db_window():
    """This function creates the database-interaction window"""

    window = tk.Tk(className="database")

    # Add text field and buttons for the queries


    tk.Label(window, text="Search:").grid(row=0, column=0, sticky='W', padx=5, pady=5)
    global query_field
    query_field = tk.Text(window, height=2, width=40)
    query_field.grid(row=0, sticky='W', padx=65, pady=5)

    query_button = tk.Button(window, text="Go!", width=4, command=start_query).grid(row=0, column=0, sticky='W', padx=400, pady=5)
    query_reset_button = tk.Button(window, text="Reset", command=reset_query_field).grid(row=0, column=0, sticky='W', padx=450, pady=5)
    
    global var1 
    var1 = tk.StringVar(value=1)       # var1 è per il gruppo dei radio button -> seleziona univoca
    

    tk.Label(window, text="\nSelezionare il tipo di ricerca:").grid(row=1, column=0, sticky='W', padx=50)

    global radio1, radio2, radio3, radio4

    radio1 = tk.Radiobutton(window, variable = var1, text = "View All", value = "1")
    radio2 = tk.Radiobutton(window, variable = var1, text = "View By Country", value = "2")
    radio3 = tk.Radiobutton(window, variable = var1, text = "View By Name", value = "3")
    radio4 = tk.Radiobutton(window, variable = var1, text = "...", value = "4")


    radio1.grid(row=2, column=0, sticky='W', padx=55)
    radio2.grid(row=3, column=0, sticky='W', padx=55)
    radio3.grid(row=4, column=0, sticky='W', padx=55)    
    radio4.grid(row=5, column=0, sticky='W', padx=55)

    global search_label
    search_label = tk.Label(window, text="Contenuti del database:")
    search_label.grid(row=6, column=0)


    # Add the data table

    global tree
    tree = ttk.Treeview(window, selectmode="extended", columns=('0','1', '2', '3','4','5','6','7','8','9','10','11','12'), show='headings')

    tree.heading('0',  text = '#')
    tree.heading('1',  text = 'ID')
    tree.heading('2',  text = 'Name')
    tree.heading('3',  text = 'Main Category')
    tree.heading('4',  text = 'Category')
    tree.heading('5',  text = 'Currency')
    tree.heading('6',  text = 'Deadline')
    tree.heading('7',  text = 'Goal')
    tree.heading('8',  text = 'Launched')
    tree.heading('9',  text = 'Pledged')
    tree.heading('10', text = 'State')
    tree.heading('11', text = 'Backers')
    tree.heading('12', text = 'Country')


    tree.column('0',  minwidth=80, width=100, stretch=NO) 
    tree.column('1',  minwidth=80, width=100, stretch=NO)
    tree.column('2',  minwidth=80, width=100, stretch=NO)
    tree.column('3',  minwidth=80, width=100, stretch=NO)
    tree.column('4',  minwidth=80, width=100, stretch=NO)
    tree.column('5',  minwidth=80, width=100, stretch=NO)
    tree.column('6',  minwidth=80, width=100, stretch=NO)
    tree.column('7',  minwidth=80, width=100, stretch=NO)
    tree.column('8',  minwidth=80, width=100, stretch=NO)
    tree.column('9',  minwidth=80, width=100, stretch=NO)
    tree.column('10', minwidth=80, width=100, stretch=NO)
    tree.column('11', minwidth=80, width=100, stretch=NO)
    tree.column('12', minwidth=80, width=100, stretch=NO)
    
    tree.grid(row=7, column=0, padx=5, pady=10)
    
    # The data table will contain all entries by default in order to show the database contents
    # view_all()

    
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=7, column=1)

    # Add data-update buttons

    b1 = tk.Button(window, text="Add Entry").grid(row=8, column=0, padx=30, pady=10, sticky='W')   #, height=2, width=15 , command=view_all)
    b2 = tk.Button(window, text="Edit Entry").grid(row=8, column=0, padx=100, pady=10, sticky='W')   # , command=view_all)
    b3 = tk.Button(window, text="Delete Entry").grid(row=8, column=0, padx=170, pady=10, sticky='W')   # , command=view_all)




def view_all():
    """ Wrapper of the print_to_table function, used over all the database entries"""

    print_to_table(collection.find())


def print_to_table(projects):
    """ Used to add values to the database-contents table"""

    item_count = len(tree.get_children())
    
    # Clear the previous content inside the table in order to add the new entries.
    if item_count > 0:
        tree.delete(*tree.get_children())

    # Add the required entries inside the table
    global row_index
    row_index = 1 #indice di riga
    
    
    for project in projects:

        #attack = list(attack.values())[1:len(attack)]
        project=list(project.values())
        
        project.insert(0,row_index)
        print(project)
        tree.insert('', tk.END, values=project)
        row_index += 1



def start_query():
    """ Starts a query based on the selected radio button and content of the query-text field"""
    
    query_content = query_field.get("1.0", "end-1c") # prende dal primo al penultimo carattere, altrimenti considera anche newline
    print(query_content)



    if(var1.get() == "1"): #view all

        search_label.configure(text="Contenuti del database:")
        view_all()

    if(var1.get() == "2"): #view by country

        country = query_field.get("1.0", "end-1c") #prende dal primo al penultimo carattere, altrimenti considera anche newline
        projects = collection.find({"Country":country})

        search_label.configure(text="Risultati della ricerca utilizzando View by Country con parametro "+query_field.get("1.0", "end-1c"))

        print_to_table(projects)

    
    if(var1.get() == "3"): #view by name

        name = query_field.get("1.0", "end-1c") #prende dal primo al penultimo carattere, altrimenti considera anche newline
        projects = collection.find({"Name":name})

        search_label.configure(text="Risultati della ricerca utilizzando View by Name con parametro "+query_field.get("1.0", "end-1c"))
        print_to_table(projects)


    
    if(var1.get() == "4"):
        print("... è selezionato")


    reset_query_field()


def reset_query_field():
    """Wrapper of the delete function, used to delete the entire query-text field"""

    query_field.delete("1.0", "end-1c")
    




class App:

    def __init__(self, master):
        master.report_callback_exception = self.login_error
        self.frame = tk.Frame(master)
        self.frame.pack()

    def login_error(self, *args):
        traceback.format_exception(*args)
        showerror('Errore', 'Le credenziali inserite non sono valide. Riprovare.', parent = window)

        

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