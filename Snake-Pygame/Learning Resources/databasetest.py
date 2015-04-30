import sqlite3


def Main():
    a = 'Cat'
    try:
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        cur.executescript('''
   DROP TABLE IF EXISTS Pets;
    CREATE TABLE Pets (Id INT, Name TEXT, Price INT);
    INSERT INTO Pets VALUES(1, 'Cat', 400);
    INSERT INTO Pets VALUES(2, 'Dog', 600);
    ''')

        pets = ((3,'Rabbit',200),
                (4,'Bird',60),
                (5,'Goat',500))
        
        cur.executemany("INSERT INTO Pets VALUES(?,?,?)",pets)
        con.commit()

        cur.execute("SELECT * FROM Pets WHERE Name = '{}'".format(a))

        data = cur.fetchone()
        print(data[1])
        #for row in data:
            #print(row)

        
    except sqlite3.Error as e:
        print(e)
        if con:
            con.rollback()
            print("There was a problem with the SQL")
    finally:
        if con:
            con.close()


if __name__ == '__main__':
    Main()
