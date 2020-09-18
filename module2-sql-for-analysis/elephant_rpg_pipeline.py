import os
import psycopg2
from dotenv import load_dotenv

# Load .env file and get credentials
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

# Connect to ElephantSQL-hosted PostgreSQL DB
conn = psycopg2.connect(dbname=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST)

cursor = conn.cursor()
cursor.execute("SELECT * from test_table;")
results = cursor.fetchall()
# print(results)

############ Connect to SQLite DB for RPG Data ####################

import sqlite3

sl_conn = sqlite3.connect('rpg_db.sqlite3')
sl_cursor = sl_conn.cursor()
characters = sl_cursor.execute('SELECT * FROM charactercreator_character;').fetchall()
# print(characters)

############ Create the Character Table in Postgres and Insert Data ##################

create_character_table_query = '''
CREATE TABLE IF NOT EXISTS rpg_characters (
    character_id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    level INT,
    exp INT,
    hp INT,
    strength INT, 
    intelligence INT,
    dexterity INT,
    wisdom INT
)
'''

cursor.execute(create_character_table_query)
conn.commit()

# Generate individual row insert queries
for character in characters:
    insert_query = f'''INSERT INTO rpg_characters
    (character_id, name, level, exp, hp, strength, intelligence, dexterity, wisdom) VALUES
    {character}   
    '''
    cursor.execute(insert_query)
conn.commit()

# Generate one big insert query (10-20x faster than individual inserts)
big_query = '''INSERT INTO rpg_characters
(character_id, name, level, exp, hp, strength, intelligence, dexterity, wisdom) VALUES'''

for character in characters:
    big_query += f' {character}, '

big_query = big_query.rstrip(',') + ';'   # Replace trailing ',' with a ';'

# cursor.execute(big_query)
# conn.commit()
