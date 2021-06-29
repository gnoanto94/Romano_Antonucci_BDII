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
reader = csv.DictReader(csvfile, delimiter=';')  
header= ["Attack", "Year", "Records", "Organization Type", "Country", "Attack Vector"] 
records = []
for each in reader: 
    #pprint.pprint(each)
    records.append(each)
    #collection.insert_one(each) #inserimento nel db un record alla volta (più chiamate al server)

pprint.pprint(records)
collection.insert_many(records) #inserimento nel db di tutti i record (una sola chiamata al server)

client.close()
    



