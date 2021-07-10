import tkinter as tk
import pymongo
import traceback

from re import T
from tkinter import ttk
from tkinter.messagebox import NO, showerror
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure



DEBUG = False
 
skipvalue, row_index, total_entries = 0, 1, 0
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

    window = tk.Tk(className=" ProjectFinder Database")

    # Add text field and buttons for the queries

    global query_field, go_btn, rst_btn, search_txt, combo, topspace, date1, date1text, date2, date2text, scrollbar


    search_txt = tk.Label(window, text="Search:", background='#edf0f5', font=('Open Sans', 12))   
    query_field = tk.Text(window, height=1, width=40, font=('Open Sans', 12))
    topspace = tk.Label(window, text="", background='#edf0f5')
    go_btn = tk.Button(window, text="Go!", width=8, command=start_new_query, font=('Open Sans', 11))
    rst_btn = tk.Button(window, text="Reset", width=8, command=reset_query_field, font=('Open Sans', 11))

    combo = ttk.Combobox(window, values=[""])

    date1 = tk.Text(window, height=1, width=5, font=('Open Sans', 12))
    date2 = tk.Text(window, height=1, width=5, font=('Open Sans', 12))

    date1text = tk.Label(window, text="Start Date:", background='#edf0f5', font=('Open Sans', 12))
    date2text = tk.Label(window, text="End Date:", background='#edf0f5', font=('Open Sans', 12))
    
    global radio_value 
    radio_value = tk.StringVar(value=1) # radio_value contains the value corresponding to the selected radio button. It's needed in order to tell the selected button.
    
    tk.Label(window, text="\nSelect your query:", background='#edf0f5', font=('Open Sans', 13)).grid(row=1, column=0, sticky='W', padx=35, pady=5)

    radio1 = tk.Radiobutton(window, variable = radio_value, text = "View All", value = "1", background='#edf0f5', font=('Open Sans', 11), command=draw_searchbox)
    radio2 = tk.Radiobutton(window, variable = radio_value, text = "View By Country", value = "2", background='#edf0f5', font=('Open Sans', 11), command=draw_searchbox)
    radio3 = tk.Radiobutton(window, variable = radio_value, text = "View By Name", value = "3", background='#edf0f5', font=('Open Sans', 11), command=draw_searchbox)
    radio4 = tk.Radiobutton(window, variable = radio_value, text = "View By State", value = "4", background='#edf0f5', font=('Open Sans', 11), command=draw_searchbox)
    radio5 = tk.Radiobutton(window, variable = radio_value, text = "View By Main Category", value = "5", background='#edf0f5', font=('Open Sans', 11), command=draw_searchbox)
    radio6 = tk.Radiobutton(window, variable = radio_value, text = "View By Sub-Category", value = "6", background='#edf0f5', font=('Open Sans', 11), command=draw_searchbox)
    radio7 = tk.Radiobutton(window, variable = radio_value, text = "Range date deadline", value = "7", background='#edf0f5', font=('Open Sans', 11), command=draw_searchbox)
    radio8 = tk.Radiobutton(window, variable = radio_value, text = "Range date launched", value = "8", background='#edf0f5', font=('Open Sans', 11), command=draw_searchbox)
    radio9 = tk.Radiobutton(window, variable = radio_value, text = "Count by Country", value = "9", background='#edf0f5', font=('Open Sans', 11), command=draw_searchbox)



    radio1.grid(row=2, column=0, sticky='W', pady=2, padx=55)
    radio2.grid(row=3, column=0, sticky='W', pady=2, padx=55)
    radio3.grid(row=4, column=0, sticky='W', pady=2, padx=55)

    radio4.grid(row=2, column=0, sticky='W', pady=2, padx=305)
    radio5.grid(row=3, column=0, sticky='W', pady=2, padx=305)
    radio6.grid(row=4, column=0, sticky='W', pady=2, padx=305)

    radio7.grid(row=2, column=0, sticky='W', pady=2, padx=605)
    radio8.grid(row=3, column=0, sticky='W', pady=2, padx=605)
    radio9.grid(row=4, column=0, sticky='W', pady=2, padx=605)


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
    
    tree.grid(row=7, column=0, padx=10, pady=(10,0))

    
    # Add horizontal scrollbar
    scrollbar = ttk.Scrollbar(window,orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(xscroll=scrollbar.set)
    scrollbar.grid(row=8, column=0, sticky='new', padx=110)
    
    # The data table will contain all entries by default in order to show the database contents
    view_all()
    add_topspacing()

    # Add paging buttons and text
    global prevbutton, nextbutton

    prevbutton = tk.Button(window, text="Show Previous", command=prev_btn, font=('Open Sans', 11))
    nextbutton = tk.Button(window, text="Show Next", command=next_btn, font=('Open Sans', 11))

    prevbutton.grid(row=9, column=0, padx=110, pady=10, sticky='W')
    nextbutton.grid(row=9, column=0, padx=110, pady=10, sticky='E')
    
    
    global entries_label
    entries_label = tk.Label(window, text="Showing entries 1-20 of "+str(collection.count_documents({}))+" values", background='#edf0f5', font=('Open Sans', 12))
    entries_label.grid(row=9, column=0, pady=10)


    window.configure(background='#edf0f5')
    window.resizable(0,0)

    window.mainloop()






def draw_searchbox():
    """ Command for the radio buttons. Used to draw a search text field or a combobox containing search parameters"""

    global combo, search_txt, rst_btn, go_btn, radio_value, skipvalue, row_index, date1, date2, date1text, date2text, scrollbar
    
    # Reset paging values
    skipvalue, row_index = 0, 1


    # Clear any previous searchbox and its related buttons
    combo.grid_forget()
    query_field.grid_forget() 
    search_txt.grid_forget()
    go_btn.grid_forget()
    rst_btn.grid_forget()
    date1.grid_forget()
    date2.grid_forget()
    date1text.grid_forget()
    date2text.grid_forget()
    

    # Get the value of the radio button to process the requested query
    query_type = radio_value.get()

    # If needed, check and change the table headings to show the query results properly
    edit_table(query_type)

    # Clear previous table contents
    if len(tree.get_children()) > 0:
        tree.delete(*tree.get_children())

    # Check the requested query
    # view all
    if(query_type == '1'):
        start_new_query()
        add_topspacing()

    # view by country
    if(query_type == '2'):
        showcombo(collection.distinct("Country"))
    
    #view by name
    if(query_type == '3'):
        showsearchfield()

    # view by state    
    if(query_type == '4'):
        showcombo(collection.distinct("State"))

    # view by main cat
    if(query_type == '5'): 
        showcombo(collection.distinct("Main Category"))

    # view by subcat 
    if(query_type == '6'):
        showcombo(collection.distinct("Sub Category"))

    # deadline range, launched range
    if(query_type in ('7','8')):
        show_datefields()
        
        #if query_type in ('7','8'):
        #   query_field.insert("1.0","Example: 2010-2012")

    # count by country
    if(query_type == '9'):
        count_by_country()
        add_topspacing()


def edit_table(query_type):
    """ Edit the treeview in order to show the proper table for the selected query"""

    global nextbutton, prevbutton, tree, scrollbar

    if query_type in ('1','2','3','4','5','6','7','8'):

        tree.grid_forget()

        tree.configure(columns=('0','1','2','3','4','5','6','7','8','9','10','11','12'))

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

    
        # Add horizontal scrollbar

        tree.configure(xscroll=scrollbar.set)
        scrollbar.grid(row=8, column=0, sticky='new', padx=110)
        
        # Add paging buttons    
        prevbutton.grid(row=9, column=0, padx=110, pady=10, sticky='W')
        nextbutton.grid(row=9, column=0, padx=110, pady=10, sticky='E')
    
    
    if query_type == '9':
        
        tree.grid_forget()
        scrollbar.grid_forget()
        
        tree.grid(row=7, column=0, padx=10, pady=10)

        tree.configure(columns=('0','1','2'))
        tree.heading('0', text='#')
        tree.heading('1', text='Country')
        tree.heading('2', text='Number of projects')
        
        
        tree.column('0',  minwidth=60,  width=60,  stretch=NO) 
        tree.column('1',  minwidth=100, width=100, stretch=NO)
        tree.column('2',  minwidth=140, width=140, stretch=NO)

        nextbutton.grid_forget()
        prevbutton.grid_forget()




def count_by_country():
    """ Executes a query which counts the number of projects for each country in the database"""
    
    search_label.configure(text="Number of projects by country:")
    entries_label.configure(text="")
    projects = collection.aggregate([
        {
            '$project': {
                '_id': 0, 
                'Country': 1
            }
        }, {
            '$group': {
                '_id': '$Country', 
                'num_of_projects': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                '_id': 1
            }
        }
        ])
    print_to_table(projects)


def add_topspacing():
    """ Adds a white blank space on top of the window in order to avoid flickering"""
    global topspace
    topspace.grid(row=0, column=0, sticky='W', padx=35, pady=(40,0))


def show_datefields():
    """ Shows the proper texts and fields needed to execute date-based queries"""
    global date1, date2, date1text, date2text, go_btn, rst_btn

    date1.delete("1.0", "end-1c")
    date2.delete("1.0", "end-1c")


    date1text.grid(row=0, column=0, sticky='W', padx=(5,0), pady=(5,0))
    date1.grid(row=0, column=0, sticky='W', padx=90, pady=(5,0))

    date2text.grid(row=0, column=0, sticky='W', padx=150, pady=(5,0))
    date2.grid(row=0, column=0, sticky='W', padx=230, pady=(5,0))

    go_btn.grid(row=0, column=0, sticky='W', padx=350, pady=5)
    rst_btn.grid(row=0, column=0, sticky='W', padx=440, pady=5)



def showcombo(boxvalues):
    """Adds a combobox and its related buttons on top of the window"""
    global search_txt, query_field, go_btn, rst_btn

    search_txt.grid(row=0, column=0, sticky='W', padx=5, pady=5)
    go_btn.grid(row=0, column=0, sticky='W', padx=450, pady=5)
    rst_btn.grid(row=0, column=0, sticky='W', padx=540, pady=5)
    
    combo.set("")
    combo.configure(values=boxvalues, font=('Open Sans', 12), width=40)
    combo.grid(row=0, sticky='W', padx=65, pady=5)


def showsearchfield():
    """Adds a search field and its related buttons on top of the window"""
    global search_txt, query_field, go_btn, rst_btn

    search_txt.grid(row=0, column=0, sticky='W', padx=5, pady=5)
    query_field.grid(row=0, sticky='W', padx=65, pady=5)
    query_field.delete("1.0", "end-1c")

    go_btn.grid(row=0, column=0, sticky='W', padx=450, pady=5)
    rst_btn.grid(row=0, column=0, sticky='W', padx=540, pady=5)





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


def view_all():
    """ Wrapper of the print_to_table function, used over all the database entries"""
    global already_counted, total_entries
    
    if(radio_value.get() == "1"):
        search_label.configure(text="All Database contents:")
        if already_counted == 0:
            total_entries = collection.count_documents({})
            already_counted = 1
        
    print_to_table(collection.find({}, skip=skipvalue, limit=20).sort("Name", pymongo.ASCENDING))




def print_to_table(projects):
    """ Used to add values to the database-contents table"""
    global row_index
    
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
    already_counted, skipvalue, row_index = 0, 0, 1
    start_query()





def start_query():
    """ Starts a query based on the selected radio button and content of the query-text field"""
    global skipvalue, search_label, entries_label, total_entries, already_counted

    query_content = query_field.get("1.0", "end-1c") # prende dal primo al penultimo carattere, altrimenti considera anche newline
    
    if DEBUG: print(query_content)

    query_type = radio_value.get()

    #view all
    if(query_type == "1"):
        search_label.configure(text="All Database contents:")
        if already_counted == 0:
            total_entries = collection.count_documents({})
            already_counted = 1
        view_all()
        edit_entries_labels()

    #view by country
    if(query_type == "2"): 
        country = combo.get()
        projects = collection.find({"Country":country}, skip = skipvalue, limit=20)
        if already_counted == 0:
            total_entries = collection.count_documents({"Country":country})
            already_counted = 1

        search_label.configure(text="Results of [View by Country] with value ["+combo.get()+"]")
        print_to_table(projects)
        edit_entries_labels()

    #view by name
    if(query_type == "3"): 
        name = query_field.get("1.0", "end-1c") #prende dal primo al penultimo carattere, altrimenti considera anche newline
        projects = collection.find({"Name":name}, skip = skipvalue, limit = 20)
        projects = collection.find({"Name":{"$regex":name}}, skip = skipvalue, limit = 20)
        if already_counted == 0:
            total_entries = collection.count_documents({"Name":{"$regex":name}})
            already_counted = 1

        search_label.configure(text="Results of [View by Name] with value ["+query_field.get("1.0", "end-1c")+"]")
        print_to_table(projects)
        edit_entries_labels()

    #view by state
    if(query_type == "4"):
        state = combo.get()
        projects = collection.find({"State":state}, skip = skipvalue, limit = 20)
        
        if already_counted == 0:
            total_entries = collection.count_documents({"State":state})
            already_counted = 1

        search_label.configure(text="Results of [View by State] with value ["+combo.get()+"]")
        print_to_table(projects)
        edit_entries_labels()

    #view by main category
    if(query_type == "5"):
        category = combo.get()
        projects = collection.find({"Main Category":category}, skip = skipvalue, limit = 20)
       
        if already_counted == 0:
            total_entries = collection.count_documents({"Main Category":category})
            already_counted = 1

        search_label.configure(text="Results of [View by Main Category] with value ["+combo.get()+"]")
        print_to_table(projects)
        edit_entries_labels()

    #view by sub-category
    if(query_type == "6"):
        category = combo.get()
        projects = collection.find({"Sub Category":category}, skip = skipvalue, limit = 20)
        
        if already_counted == 0:
            total_entries = collection.count_documents({"Sub Category":category})
            already_counted = 1
        
        search_label.configure(text="Results of [View by Sub-Category] with value ["+combo.get()+"]")
        print_to_table(projects)
        edit_entries_labels()

    #by deadline
    if(query_type == "7"):
 
        min_year = int(date1.get("1.0", "end-1c"))
        max_year = int(date2.get("1.0", "end-1c"))

        projects = collection.find({"Deadline":{"$gte":min_year, "$lte":max_year}}, skip = skipvalue, limit = 20).sort("Deadline", pymongo.ASCENDING)
        
        if already_counted == 0:
            total_entries = collection.count_documents({"Deadline":{"$gte":min_year, "$lte":max_year}})
            already_counted = 1

        search_label.configure(text="Results of [View by deadline date] with value ["+str(min_year)+"-"+str(max_year)+"]")
        print_to_table(projects)
        edit_entries_labels()

    #launched
    if(query_type == "8"):

        min_year = int(date1.get("1.0", "end-1c"))
        max_year = int(date2.get("1.0", "end-1c"))

        projects = collection.find({"Launched":{"$gte":min_year, "$lte":max_year}}, skip = skipvalue, limit = 20).sort("Launched", pymongo.ASCENDING)
        
        if already_counted == 0:
            total_entries = collection.count_documents({"Launched":{"$gte":min_year, "$lte":max_year}})
            already_counted = 1

        search_label.configure(text="Results of [View by launched date] with value ["+str(min_year)+"-"+str(max_year)+"]")
        print_to_table(projects)
        edit_entries_labels()
    
    



def edit_entries_labels():
    """Used to edit all labels due to a requested query's results"""
    global row_index, entries_label

    if(row_index > 0):
        entries_text = "Showing entries "+str(int(row_index-len(tree.get_children())))+"-"+str(row_index-1) + " over "+str(total_entries)+" values"
        entries_label.configure(text=entries_text)
    
    if(len(tree.get_children()) == 0):
        entries_text = "No entries to show"
        entries_label.configure(text=entries_text)
    

def reset_query_field():
    """Wrapper of the delete function, used to delete the all query fields"""
    
    query_field.delete("1.0", "end-1c")
    combo.set("")
    date1.delete("1.0", "end-1c")
    date2.delete("1.0", "end-1c")

    item_count = len(tree.get_children())

    entries_label.configure(text="")
    search_label.configure(text="")
    
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







window = tk.Tk(className=" Login")
window.geometry("300x300")
window.resizable(0,0)
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