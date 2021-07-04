import tkinter as tk
import pymongo
import traceback
import Pmw

from re import T
from tkinter import ttk
from tkinter.messagebox import NO, showerror
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure



DEBUG = False
 
skipvalue, row_index, total_entries = 0, 0, 0
already_counted = 0 # flag to count the total number of entries for a given query



def login_btn():
    """Function used by the login button to start the database login process"""

    db_login(username.get(), password.get())




def db_login(usr, pwd):
    """ Given a username and a password, this function attempts a login to the database. """

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

    tk.Label(window, text="Search:", background='#edf0f5', font=('Open Sans', 12)).grid(row=0, column=0, sticky='W', padx=5, pady=5)
    global query_field
    query_field = tk.Text(window, height=1, width=40, font=('Open Sans', 12))
    query_field.grid(row=0, sticky='W', padx=65, pady=5)

    tk.Button(window, text="Go!", width=8, command=start_new_query, font=('Open Sans', 11)).grid(row=0, column=0, sticky='W', padx=450, pady=5)
    tk.Button(window, text="Reset", width=8, command=reset_query_field, font=('Open Sans', 11)).grid(row=0, column=0, sticky='W', padx=540, pady=5)
    
    global radio_value 
    radio_value = tk.StringVar(value=1)       # radio_value contains the value corresponding to the selected radio button. It's needed in order to tell the selected button.
    
    tk.Label(window, text="\nSelect your query:", background='#edf0f5', font=('Open Sans', 13)).grid(row=1, column=0, sticky='W', padx=35, pady=5)
    
    global radio1, radio2, radio3, radio4, radio5, radio6

    radio1 = tk.Radiobutton(window, variable = radio_value, text = "View All", value = "1", background='#edf0f5', font=('Open Sans', 11), command=radio_reset)
    radio2 = tk.Radiobutton(window, variable = radio_value, text = "View By Country", value = "2", background='#edf0f5', font=('Open Sans', 11), command=radio_reset)
    radio3 = tk.Radiobutton(window, variable = radio_value, text = "View By Name", value = "3", background='#edf0f5', font=('Open Sans', 11), command=radio_reset)
    radio4 = tk.Radiobutton(window, variable = radio_value, text = "View By State", value = "4", background='#edf0f5', font=('Open Sans', 11), command=radio_reset)
    radio5 = tk.Radiobutton(window, variable = radio_value, text = "View By Main Category", value = "5", background='#edf0f5', font=('Open Sans', 11), command=radio_reset)
    radio6 = tk.Radiobutton(window, variable = radio_value, text = "View By Sub-Category", value = "6", background='#edf0f5', font=('Open Sans', 11), command=radio_reset)

    # Bind the tooltip for some of the radio buttons
    balloon = Pmw.Balloon(window)
    balloon.bind(radio4,"Options: failed, successful")

    radio1.grid(row=2, column=0, sticky='W', pady=2, padx=55)
    radio2.grid(row=3, column=0, sticky='W', pady=2, padx=55)
    radio3.grid(row=4, column=0, sticky='W', pady=2, padx=55)

    radio4.grid(row=2, column=0, sticky='W', pady=2, padx=305)
    radio5.grid(row=3, column=0, sticky='W', pady=2, padx=305)
    radio6.grid(row=4, column=0, sticky='W', pady=2, padx=305)

    global search_label
    search_label = tk.Label(window, text="All Database contents:", background='#edf0f5', font=('Open Sans', 13))
    search_label.grid(row=6, column=0, pady=5)


    # Add the data table

    global tree
    tree = ttk.Treeview(window, selectmode="extended", columns=('0','1', '2', '3','4','5','6','7','8','9','10','11','12'), show='headings', height=20)


    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Open Sans', 11))
    style.configure("Treeview", font=('Open Sans', 11))

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


    tree.column('0',  minwidth=60,  width=60,  stretch=NO) 
    tree.column('1',  minwidth=100, width=100, stretch=NO)
    tree.column('2',  minwidth=80,  width=125, stretch=NO)
    tree.column('3',  minwidth=80,  width=125, stretch=NO)
    tree.column('4',  minwidth=80,  width=125, stretch=NO)
    tree.column('5',  minwidth=70,  width=70,  stretch=NO)
    tree.column('6',  minwidth=70,  width=70,  stretch=NO)
    tree.column('7',  minwidth=80,  width=80,  stretch=NO)
    tree.column('8',  minwidth=90,  width=90,  stretch=NO)
    tree.column('9',  minwidth=90,  width=90,  stretch=NO)
    tree.column('10', minwidth=80,  width=80,  stretch=NO)
    tree.column('11', minwidth=70,  width=70,  stretch=NO)
    tree.column('12', minwidth=60,  width=60,  stretch=NO)
    
    tree.grid(row=7, column=0, padx=10, pady=10)
    
    # The data table will contain all entries by default in order to show the database contents
    view_all()

    # Add paging buttons and text
    tk.Button(window, text="Show Previous", command=prev_btn, font=('Open Sans', 11)).grid(row=9, column=0, padx=10, pady=10, sticky='W')
    tk.Button(window, text="Show Next", command=next_btn, font=('Open Sans', 11)).grid(row=9, column=0, padx=10, pady=10, sticky='E')
    
    
    global entries_label
    entries_label = tk.Label(window, text="Showing entries 0-20 of "+str(collection.count_documents({}))+" values", background='#edf0f5', font=('Open Sans', 11))
    entries_label.grid(row=9, column=0, pady=10)


    window.configure(background='#edf0f5')



def next_btn():
    """ Command for the next button. Shows 20 next entries"""
    global skipvalue
    skipvalue += 20
    start_query()


def prev_btn():
    """ Command for the previous button. Shows 20 previous entries"""
    global skipvalue, row_index
    
    if skipvalue >= 20:
        skipvalue -=20
        row_index -=40
        start_query()


def radio_reset():
    """ Command for all radio buttons, used to reset all indexes in order to start a new query over the selected radio button"""
    global skipvalue, row_index
    skipvalue = 0
    row_index = 0




def view_all():
    """ Wrapper of the print_to_table function, used over all the database entries"""
    print_to_table(collection.find({}, skip=skipvalue, limit=20))




def print_to_table(projects):
    """ Used to add values to the database-contents table"""
    global row_index

    #item_count = len(tree.get_children())
    
    # Clear the previous content inside the table in order to add the new entries.
    if len(tree.get_children()) > 0:
        tree.delete(*tree.get_children())

    # Add the required entries inside the table
    for project in projects:

        project=list(project.values())
        project.insert(0,row_index)
        
        if DEBUG: print(project)

        tree.insert('', tk.END, values=project)
        row_index += 1



def start_new_query():
    """ Resets all indexes and skips, an then start a query. Used as the command for the GO! Button"""
    global skipvalue, row_index, entries_label, already_counted
    already_counted = 0
    skipvalue = 0
    row_index = 0
    start_query()




def start_query():
    """ Starts a query based on the selected radio button and content of the query-text field"""
    global skipvalue, search_label, entries_label, total_entries, already_counted

    query_content = query_field.get("1.0", "end-1c") # prende dal primo al penultimo carattere, altrimenti considera anche newline
    

    if DEBUG: print(query_content)
    
    #view all
    if(radio_value.get() == "1"):
        search_label.configure(text="All Database contents:")
        if already_counted == 0:
            total_entries = collection.count_documents({})
            already_counted = 1
        view_all()

    #view by country
    if(radio_value.get() == "2"): 

        country = query_field.get("1.0", "end-1c") #prende dal primo al penultimo carattere, altrimenti considera anche newline
        projects = collection.find({"Country":country}, skip = skipvalue, limit=20)
        
        if already_counted == 0:
            total_entries = collection.count_documents({"Country":country})
            already_counted = 1
        
        search_label.configure(text="Results of [View by Country] with value ["+query_field.get("1.0", "end-1c")+"]")
        print_to_table(projects)

    #view by name
    if(radio_value.get() == "3"): 
        name = query_field.get("1.0", "end-1c") #prende dal primo al penultimo carattere, altrimenti considera anche newline
        projects = collection.find({"Name":name}, skip = skipvalue, limit = 20)
        if already_counted == 0:
            total_entries = collection.count_documents({"Name":name})
            already_counted = 1

        search_label.configure(text="Results of [View by Name] with value ["+query_field.get("1.0", "end-1c")+"]")
        print_to_table(projects)

    #view by state
    if(radio_value.get() == "4"):
        state = query_field.get("1.0", "end-1c") #prende dal primo al penultimo carattere, altrimenti considera anche newline
        projects = collection.find({"State":state}, skip = skipvalue, limit = 20)
        
        if already_counted == 0:
            total_entries = collection.count_documents({"State":state})
            already_counted = 1

        search_label.configure(text="Results of [View by State] with value ["+query_field.get("1.0", "end-1c")+"]")
        print_to_table(projects)

    #view by main category
    if(radio_value.get() == "5"):
        category = query_field.get("1.0", "end-1c") #prende dal primo al penultimo carattere, altrimenti considera anche newline
        projects = collection.find({"Main Category":category}, skip = skipvalue, limit = 20)
       
        if already_counted == 0:
            total_entries = collection.count_documents({"Main Category":category})
            already_counted = 1

        search_label.configure(text="Results of [View by Main Category] with value ["+query_field.get("1.0", "end-1c")+"]")
        print_to_table(projects)

    #view by sub-category
    if(radio_value.get() == "6"):
        category = query_field.get("1.0", "end-1c") #prende dal primo al penultimo carattere, altrimenti considera anche newline
        projects = collection.find({"Sub Category":category}, skip = skipvalue, limit = 20)
        
        if already_counted == 0:
            total_entries = collection.count_documents({"Sub Category":category})
            already_counted = 1
        
        search_label.configure(text="Results of [View by Sub-Category] with value ["+query_field.get("1.0", "end-1c")+"]")
        print_to_table(projects)
        

    #Modify the entries label under the content table
    if(row_index > 0):
        entries_text = "Showing entries "+str(int(row_index-20))+"-"+str(row_index) + " over "+str(total_entries)+" values"
        entries_label.configure(text=entries_text)
    
    #query_field.delete("1.0", "end-1c")


def reset_query_field():
    """Wrapper of the delete function, used to delete the entire query-text field"""
    
    query_field.delete("1.0", "end-1c")
    item_count = len(tree.get_children())
    
    # Clear the previous content inside the table in order to add the new entries.
    if item_count > 0:
        tree.delete(*tree.get_children())

    

    







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

usr_label = tk.Label(window, text = "Username: ", background = '#edf0f5', font=('Open Sans', 13))
usr_label.place(x = 50, y = 20)
 
username = tk.Entry(window, width = 35, font=('Open Sans', 10))
username.place(x = 150, y = 25, width = 120)
username.insert(-1, "admin")

pwd_label = tk.Label(window, text ="Password: ", background = '#edf0f5', font=('Open Sans', 13))
pwd_label.place(x = 50, y = 50)
 
password = tk.Entry(window, show = "*", width = 35, font=('Open Sans', 10))
password.place(x = 150, y = 55, width = 120)
password.insert(-1, "oNWZDGjCxDHtnp8o")
 
login_button = tk.Button(window, text = "Login", command = login_btn, font=('Open Sans', 11))
login_button.place(x = 150, y = 135, width = 55)

app = App(window)
window.configure(background='#edf0f5')
window.mainloop()