import pymongo
import pprint

from pymongo import MongoClient
client = MongoClient()

DEBUG = True
_limit = 20

def stampa(projects):
    for project in projects:
        pprint.pprint(project)

#admin:oNWZDGjCxDHtnp8o
client = pymongo.MongoClient("mongodb+srv://admin:oNWZDGjCxDHtnp8o@cluster0.bkvuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
print("Info: "+str(client))
db = client.ksprojects
collection = db.data


#visualizza tutti i progetti limitando la query a _limit risultati 
def all_projects(_skip):
    print("Documenti presenti: " + str(collection.count_documents({})) + "[Exp: 319.328]")
    #per come è impostata ora restituisce i primi 15 risultati
    projects = collection.find({}, skip=_skip, limit=_limit)
    if DEBUG: stampa(projects)
    return projects

#visualizza i progetti in un determinato Country (nome esatto)
#esempio: country = "United Kingdom"
def projects_by_exact_country(country):
    projects = collection.find({"Country":country})
    if DEBUG: stampa(projects)
    return projects

#visualizza i progetti in un determinato Country (nome parziale)
#esempio: country = "Kingdom"
def projects_by_country(country):
    projects = collection.find({"Country":{"$regex":country}})
    if DEBUG: stampa(projects)
    return projects

#visualizza i progetti in base al Name (nome esatto)
#esempio: name = "The Cottage Market"
def projects_by_exact_name(project_name):
    #per questa query probabilmente conviene creare un elenco
    #da cui l'utente puo' selezionare il tipo di organizzazione
    projects = collection.find({"Name":project_name})
    if DEBUG: stampa(projects)
    return projects

#visualizza i progetti in base al Name (nome parziale)
#esempio: name = "The Cottage Market"
def projects_by_name(project_name):
    #per questa query probabilmente conviene creare un elenco
    #da cui l'utente puo' selezionare il tipo di organizzazione
    projects = collection.find({"Name":{"$regex":project_name}})
    if DEBUG: stampa(projects)
    return projects

#visualizza i progetti la cui deadline è tra un intervallo di anni
#esempio: min_year = 2008
#         max_year = 2012
def projects_deadline_between_years(min_year, max_year):
    #ordinamento dal meno recente al piu' recente
    projects = collection.find({"Deadline":{"$gte":min_year, "$lte":max_year}}).sort("Deadline", pymongo.ASCENDING)
    if DEBUG: stampa(projects)
    return projects

#visualizza i progetti che sono stati proposti tra un intervallo di anni
#esempio: min_year = 2008
#         max_year = 2012
def projects_lauched_between_years(min_year, max_year):
    #ordinamento dal meno recente al piu' recente
    projects = collection.find({"Launched":{"$gte":min_year, "$lte":max_year}}).sort("Launched", pymongo.ASCENDING)
    if DEBUG: stampa(projects)
    return projects

#visualizza i progetti in base al loro stato (valore esatto)
def projects_by_state(state):
    projects = collection.find({"State":state})
    if DEBUG: stampa(projects)
    return projects

#visualizza i progetti in base alla loro Main Category (valore esatto)
def projects_by_main_category(category):
    projects = collection.find({"Main Category":category})
    if DEBUG: stampa(projects)
    return projects

#visualizza i progetti in base alla loro Sub Category (valore esatto)
def projects_by_sub_category(category):
    projects = collection.find({"Sub Category":category})
    if DEBUG: stampa(projects)
    return projects


def num_of_projects_in_country():
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

    if DEBUG: stampa(projects)
    return projects

def num_of_projects_launched_in_year():
    projects = collection.aggregate([
    {
        '$project': {
            '_id': 0, 
            'Launched': 1
        }
    }, {
        '$group': {
            '_id': '$Launched', 
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
    if DEBUG: stampa(projects)
    return projects

# ******** VALORI PER EVENTUALE MENU' A TENDINA ********

#valori distinti per il field "State"
#restituisce una lista
def state_values():
    values = collection.distinct("State")
    values.sort()
    if DEBUG: print(values)
    return values

#valori distinti per il field "Main Category"
#restituisce una lista
def main_category_values():
    values = collection.distinct("Main Category")
    if DEBUG: print(values)
    return values

#valori distinti per il field "Sub Cateogory"
#restituisce una lista
def sub_category_values():
    values = collection.distinct("Sub Category")
    return values

def close_connection():
    client.close()

state_values()
close_connection()