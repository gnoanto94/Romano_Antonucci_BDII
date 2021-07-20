from os import name
from tkinter.constants import E
import pymongo
import pprint
import csv
import datetime

from pymongo import MongoClient

'''
Il file .csv del dataset non è presente nella consegna a causa di problemi con le dimensioni eccessive rispetto al limite.
E' stato inserito (all'interno dell'archivio) un link al dataset originale sulla piattaforma kaggle.com
'''

client = MongoClient()

#admin:oNWZDGjCxDHtnp8o
client = pymongo.MongoClient("mongodb+srv://admin:oNWZDGjCxDHtnp8o@cluster0.bkvuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
print("Info: "+str(client))
db = client.ksprojects
collection = db.data
collection.drop() #ripulisce la collection prima di aggiungere i dati

#CSV to JSON Conversion 
csvfile = open('dataset/2016.csv', 'r') 
records = []

def parse(csvfile):
    reader = csv.DictReader(csvfile, delimiter=';') # è una variabile di tipo dizionario
    #         0      1              2              3              4          5         6        7            8         9         10         11          12
    header= ["_id", "Name", "Main Category", "Sub Category", "Currency", "Deadline", "Goal", "Launched", "Pledged", "State", "Backers", "Country", "USD Pledged"] 
    from datetime import datetime

    for each in reader: 
        #pprint.pprint(each)
        id = each["\ufeffID"]
        name = each["name"]
        category = each["category"]
        main_category = each["main_category"]
        currency = each["currency"]
        deadline = each["deadline"]
        try:
                goal = float(each["goal"])
        except ValueError:
                goal = 0.0
        launched = each["launched"]
        #pprint.pprint(launched)
        try:
                pledged = float(each["pledged"])
        except ValueError:
                pledged = 0.0
        state = each["state"]
        backers = each["backers"]
        country = each["country"]

        date_format_deadline = '%m/%d/%Y %H:%M' #'%Y-%m-%d %H:%M:%S'
        date_format_launched = '%d/%m/%Y %H:%M'
        try:
                deadline_obj = datetime.strptime(deadline, date_format_deadline)
                deadline_obj = deadline_obj.date().year
        except ValueError:
                if deadline != '':
                        deadline_obj = datetime.strptime(deadline, date_format_launched)
                        deadline_obj = deadline_obj.date().year
                else:
                        deadline_obj = ''

        try:
                launched_obj = datetime.strptime(launched, date_format_launched)
                launched_obj = launched_obj.date().year
        except ValueError:
                if launched != '':
                        launched_obj = datetime.strptime(launched, date_format_deadline)
                        launched_obj = launched_obj.date().year
                else:
                        launched_obj = ''

        record = {header[0]: id, 
                header[1]:name, 
                header[2]:main_category, 
                header[3]:category, 
                header[4]:currency, 
                header[5]:deadline_obj, 
                header[6]:goal,
                header[7]:launched_obj,
                header[8]:pledged,
                header[9]:state,
                header[10]:backers,
                header[11]:country
                }
        
        records.append(record)

parse(csvfile)

collection.insert_many(records) #inserimento nel db di tutti i record (una sola chiamata al server)
print("HO FINITO")
client.close()