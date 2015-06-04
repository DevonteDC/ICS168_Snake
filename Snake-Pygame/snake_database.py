import sqlite3


con = sqlite3.connect('snaketest.db')
cur = con.cursor()
#cur.execute("UPDATE Login SET Highscore = '10' WHERE Username = 'c'")
#cur.execute("INSERT INTO Login VALUES('2','4')")

            
            
#cur.execute('DROP TABLE Login')
con.commit()
print("Database deleted")
cur.execute("SELECT * FROM Login")
data = cur.fetchall()

for row in data:
    print(row)
