import _sqlite3

with _sqlite3.connect("Response.db") as database:
	cursor = database.cursor()

cursor.execute("SELECT * FROM responses")
printingInfo = cursor.fetchall()

for i in printingInfo:
	print(i)