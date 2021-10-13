import _sqlite3

with _sqlite3.connect("Response.db") as database:
    cursor = database.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS responses(
BasicID INTEGER PRIMARY KEY,
Question VARCHAR(20) NOT NULL,
Response VARCHAR(20) NOT NULL);
''')

