import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
import pandas

load_dotenv() #> loads contents of the .env file into the script's environment

DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASS = os.getenv("DB_PASS", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")

CSV_FILEPATH = "titanic.csv"
#CSV_FILEPATH = os.path.join(os.path.dirname(__file__), "titanic.csv")
#CSV_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "module2-sql-for-analysis", "titanic.csv")

#
# CONNECT TO THE PG DATABASE
#

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
print(type(connection)) #> <class 'psycopg2.extensions.connection'>

cursor = connection.cursor()
print(type(cursor)) #> <class 'psycopg2.extensions.cursor'>

#
# CREATE A TABLE TO STORE THE PASSENGERS
#
# ... optionally renaming some of the columns, adding a primary key, and changing survived to a bool

sql = """
DROP TABLE IF EXISTS passengers;
CREATE TABLE IF NOT EXISTS passengers (
    id SERIAL PRIMARY KEY,
    survived boolean,
    pclass int4,
    full_name text,
    gender text,
    age int4,
    sib_spouse_count int4,
    parent_child_count int4,
    fare float8
);
"""
cursor.execute(sql)

#
# READ PASSENGER DATA FROM THE CSV FILE
#

df = pandas.read_csv(CSV_FILEPATH)
print(df.columns.tolist())
#print(df.dtypes)
#print(df.head())

#
# INSERT DATA INTO THE PASSENGERS TABLE
#

# how to convert dataframe to a list of tuples?
list_of_tuples = list(df.to_records(index=False))

insertion_query = f"INSERT INTO passengers (survived, pclass, full_name, gender, age, sib_spouse_count, parent_child_count, fare) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples) # third param: data as a list of tuples!

# CLEAN UP

connection.commit() # actually save the records / run the transaction to insert rows

cursor.close()
connection.close()