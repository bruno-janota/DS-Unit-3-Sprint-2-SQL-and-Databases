import os
import json
from pdb import set_trace as breakpoint
from dotenv import load_dotenv
import pymongo
import pandas as pd

load_dotenv() #> loads contents of the .env file into the script's environment

MONGO_USER = os.getenv("MONGO_USER", default="OOPS")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
MONGO_CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER_NAME}?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
print('URI:', uri)
print(client.list_database_names())

# Set the DB to Analytics
analytics_db = client.sample_analytics
print(analytics_db.list_collection_names())

# Access a specific collection
transactions = analytics_db.transactions
print(transactions.count_documents({}))

# How many customers have more than 50 transcations
print(transactions.count_documents({'transaction_count': {'$gt': 50}}))

# Get all the customers into a dataframe
customers = analytics_db.customers
all_customers = customers.find()
df = pd.DataFrame(all_customers)
print(df.shape)
df.head()

# One of the problems with Mongo
customers.insert_one({'full_name': 'Bruno Janota'})
all_customers = customers.find()
df = pd.DataFrame(all_customers)
print(df.shape)
df.tail()

#
#### Write JSON Data from RPG DB to MongoDB
#

# Read the JSON file (copied from: https://raw.githubusercontent.com/LambdaSchool/Django-RPG/master/testdata.json)
with open('./test_data_json.txt') as json_file:
    rpg_data = json.load(json_file)

# Create an rpg_data database
my_db = client.rpg_data

# Create a characters collection in the rpg_data DB
character_table = my_db.characters

# Insert the JSON data into characters collection
character_table.insert_many(rpg_data)
print(character_table.count_documents({}))