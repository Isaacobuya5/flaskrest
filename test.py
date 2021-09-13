import sqlite3  # interact with sqlite database that is inbuilt

# initialize connection to database
connection = sqlite3.connect("data.db")

# cursor allows you to select things - responsible for excecute queries and storing results
cursor = connection.cursor()

# create a table - query
create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

# store data
user = (1, "Isaac", "qwerty1234")

# insert query
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# insert into the table
cursor.execute(insert_query, user)

users = [
    (2, "john", "john1234"),
    (3, "tom", "tom1234")
]

# insert many users
cursor.executemany(insert_query, users)

# retrieve users
select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
