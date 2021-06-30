from tkinter.constants import E
import pymongo
import pprint
import csv

from pymongo import MongoClient
client = MongoClient()

#admin:oNWZDGjCxDHtnp8o
client = pymongo.MongoClient("mongodb+srv://admin:oNWZDGjCxDHtnp8o@cluster0.bkvuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
print("Info: "+str(client))
db = client.attacks
collection = db.data
collection.drop() #ripulisce la collection prima di aggiungere i dati

#CSV to JSON Conversion 
csvfile = open('dataset/all.csv', 'r') 
reader = csv.DictReader(csvfile, delimiter=';') # è una variabile di tipo dizionario
#           0        1         2              3                4              5
header= ["Attack", "Year", "Records", "Organization Type", "Country", "Attack Vector"] 
records = []
for each in reader: 
    attack = each["Attack"]
    year = int(each["Year"])
    org_type = each["Organization Type"]
    country = each["Country"]
    attack_vector = each["Attack Vector"]
    record = {header[0]: attack, header[1]:year, header[3]:org_type, header[4]:country, header[5]:attack_vector}
    
    records.append(record)
    #collection.insert_one(record) #inserimento nel db un record alla volta (più chiamate al server)

#pprint.pprint(records)
collection.insert_many(records) #inserimento nel db di tutti i record (una sola chiamata al server)

client.close()