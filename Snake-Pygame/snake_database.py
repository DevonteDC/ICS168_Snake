import sqlite3


con = sqlite3.connect('snaketest.db')
cur = con.cursor()

cur.execute("SELECT * FROM Login")
data = cur.fetchall()

for row in data:
    print(row)
