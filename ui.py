import tkinter as tk
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure



def login_btn():
    db_login(username.get(), password.get())


def db_login(usr, pwd):

    #client = pymongo.MongoClient("mongodb+srv://admin:oNWZDGjCxDHtnp8o@cluster0.bkvuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    client = MongoClient()
    client = pymongo.MongoClient("mongodb+srv://"+usr+":"+pwd+"@cluster0.bkvuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    try:
        # The ismaster command is cheap and does not require auth --> usato per controllare se login ha successo
        client.admin.command('ismaster')
        
        #AGGIUNGERE GESTIONE FRASE ERRORE CHE COMPARE E SCOMPARE SE LOGIN NON HA SUCCESSO


    except ConnectionFailure:
        print("Server not available")

    db = client.attacks
    collection = db.data

    print("Logging as: "+usr)


window = tk.Tk(className="login")

window.geometry("300x300")


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

window.mainloop()
