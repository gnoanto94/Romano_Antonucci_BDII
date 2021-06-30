import pymongo
import pprint

from pymongo import MongoClient
client = MongoClient()

def stampa(attacks):
    for attack in attacks:
        pprint.pprint(attack)

#admin:oNWZDGjCxDHtnp8o
client = pymongo.MongoClient("mongodb+srv://admin:oNWZDGjCxDHtnp8o@cluster0.bkvuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
print("Info: "+str(client))
db = client.attacks
collection = db.data


#visualizza tutti gli attacchi
def all_attacks():
    print("Documenti presenti: " + str(collection.count_documents({})) + "[Exp: 321]")
    attacks = collection.find()
    stampa(attacks)

#visualizza gli attacchi in un determinato Country (nome esatto)
#esempio: country = "United Kingdom"
def attack_by_exact_country(country):
    attacks = collection.find({"Country":country})
    stampa(attacks)

#visualizza gli attacchi in un determinato Country (nome parziale)
#esempio: country = "Kingdom"
def attacks_by_country(country):
    attacks = collection.find({"Country":{"$regex":country}})
    stampa(attacks)

#visualizza gli attacchi in base al tipo di Organizzazione
#esempio: organization_type = "Pretroleum"
def attacks_by_organization_type(organization_type):
    #per questa query probabilmente conviene creare un elenco
    #da cui l'utente puo' selezionare il tipo di organizzazione
    attacks = collection.find({"Organization Type":organization_type})
    stampa(attacks)

#visualizza gli attacchi tra un intervallo di anni
#esempio: min_year = 2008
#         max_year = 2012
def attacks_between_years(min_year, max_year):
    #ordinamento dal meno recente al piu' recente
    attacks = collection.find({"Year":{"$gte":min_year, "$lte":max_year}}).sort("Year", pymongo.ASCENDING)
    stampa(attacks)

print("TUTTI")
all_attacks()
print("REGNO UNITO (ESATTO)")
attack_by_exact_country("United Kingdom")
print("REGNO UNITO (PARZIALE)")
attacks_by_country("Kingdom")
print("TIPO ORGANIZZAZIONE: PETROLEUM")
attacks_by_organization_type("Petroleum")
print("TRA IL 2008 e il 2012")
attacks_between_years(2008, 2012)

client.close()