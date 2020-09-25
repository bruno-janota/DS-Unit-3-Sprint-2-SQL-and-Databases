'''
## Starting From Scratch
Create a file named `study_part1.py` and complete the exercise below. The only library you should need to import is `sqlite3`. Don't forget to be PEP8 compliant!
1. Create a new database file call `study_part1.sqlite3`
2. Create a table with the following columns
```
 student - string
 studied - string
 grade - int
 age - int
 sex - string
 ```
3. Fill the table with the following data
```
 'Lion-O', 'True', 85, 24, 'Male'
 'Cheetara', 'True', 95, 22, 'Female'
 'Mumm-Ra', 'False', 65, 153, 'Male'
 'Snarf', 'False', 70, 15, 'Male'
 'Panthro', 'True', 80, 30, 'Male'
 ```
4. Save your data. You can check that everything is working so far if you can view the table and data in DBBrowser
5. Write the following queries to check your work. Query outputs should be formatted for readability, don't simply print a number to the screen with no explanation, add context.
'''

import sqlite3

# Make sure to check the path when connecting (wrong path will create a new empty database)
conn = sqlite3.connect('study_part1.sqlite3')
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    studied TEXT,
    grade INT,
    age INT,
    sex TEXT
)
'''
cursor.execute(create_table_query)

sample_data = [
    ('Lion-O', 'True', 85, 24, 'Male' ),
    ('Cheetara', 'True', 95, 22, 'Female'),
    ('Mumm-Ra', 'False', 65, 153, 'Male'), 
    ('Snarf', 'False', 70, 15, 'Male'),
    ('Panthro', 'True', 80, 30, 'Male')
]

for row in sample_data:
    insert_query = f'''INSERT INTO students (student, studied, grade, age, sex) 
    VALUES {row};   
    '''
    cursor.execute(insert_query)
conn.commit()

# What is the average age? Expected Result - 48.8
query1 = 'SELECT AVG(age) FROM students'
result = cursor.execute(query1).fetchone()
print(f'What is the average age? {result[0]}')

# Skipping these but feel free to practice if you'd like...
# What are the name of the female students? Expected Result - 'Cheetara'
# How many students studied? Expected Results - 3
# Return all students and all columns, sorted by student names in alphabetical order.

cursor.close()
conn.close()