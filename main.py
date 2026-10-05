import os
from dotenv import load_dotenv
from astrapy import DataAPIClient

load_dotenv()  # read the secret keys from the .env file

client = DataAPIClient(token=os.environ["ASTRA_DB_APPLICATION_TOKEN"])
db = client.get_database(os.environ["ASTRA_DB_API_ENDPOINT"])

# A collection is a group of documents (here: a group of animals)
animals = db.create_collection("animals")

# CREATE: add documents (each document can have different fields)
animals.insert_many([
    {"name": "Kucing Oren", "type": "Cat", "habitat": "House", "cuteness": 9},
    {"name": "Panda", "type": "Bear", "habitat": "Bamboo forest", "cuteness": 10,
     "favorite_food": "Bamboo"},
    {"name": "Kelinci", "type": "Rabbit", "habitat": "Meadow", "cuteness": 8},
    {"name": "Red Panda", "type": "Red panda", "habitat": "Mountain forest",
     "cuteness": 10},
])

# READ: find documents with a filter
print("== Animals living in a forest ==")
for a in animals.find({"type": "Bear"}):
    print(a)

# UPDATE: change the cuteness score of the rabbit
animals.update_one({"name": "Kelinci"}, {"$set": {"cuteness": 10}})
print("== Rabbit after update ==")
print(animals.find_one({"name": "Kelinci"}))

# DELETE: remove the house cat
animals.delete_one({"name": "Kucing Oren"})
print("== Remaining animals ==")
for a in animals.find({}):
    print(a)