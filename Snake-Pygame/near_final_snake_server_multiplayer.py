import socket
import time
import sqlite3
import random

host = '127.0.0.1'
port = 20000
s  = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

clients = []

con = sqlite3.connect('snaketest.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Login (Username TEXT, Password TEXT,Highscore TEXT)")
con.commit()
num_users = 0

quitting = False
print("Server Started")

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        data = data.decode()
        data = data.split(":")
        if addr not in clients:
            clients.append(addr)

        #print(time.ctime(time.time()) + str(addr) + ' : : ' + str(data))
        if data[0] == "Login":
            username = data[1]
            password = data[2]
            print("PASSWORD RECEIVED: ",password," TYPE: ",type(password))
            cur.execute("SELECT COUNT(*) FROM Login WHERE Username = '{}'".format(username))
            info = cur.fetchone()
            print(info)
            if info[0] == 0:
                print("New User Acquired: {}   Password {}".format(username,password))
                cur.execute("INSERT INTO Login VALUES('{}','{}','0')".format(username,password))
                con.commit()
                s.sendto("Gameloop:?:?".encode(),addr)
            elif info[0] == 1:
                cur.execute("SELECT * FROM Login WHERE Username = '{}'".format(username))
                info = cur.fetchone()
                print("THE INFO: ",info[1])
                if info[1] == password:
                    print("Returning User: {}   Password {}".format(username,password))
                    s.sendto("Gameloop:?:?".encode(),addr)
                else:
                    print("Invalid Password for User: {}".format(username))
                    s.sendto("Invalidpass:?:?".encode(),addr)
            
        if data[0] == "User":
            num_users += 1
            if num_users == 1:
                s.sendto("1User:?:?".encode(),addr)
            if num_users == 2:
                s.sendto("2User:?:?".encode(),addr)
            if num_users == 3:
                s.sendto("3User:?:?".encode(),addr)
            if num_users == 4:
                s.sendto("4User:?:?".encode(),addr)
        if data[0] == "User1":
            if data[1] == "Left":
                for client in clients:
                    s.sendto("User1:Left:?".encode(),client)
            if data[1] == "Right":
                for client in clients:
                    s.sendto("User1:Right:?".encode(),client)
            if data[1] == "Up":
                for client in clients:
                    s.sendto("User1:Up:?".encode(),client)
            if data[1] == "Down":
                for client in clients:
                    s.sendto("User1:Down:?".encode(),client)
        if data[0] == "User2":
            if data[1] == "Left":
                for client in clients:
                    s.sendto("User2:Left:?".encode(),client)
            if data[1] == "Right":
                for client in clients:
                    s.sendto("User2:Right:?".encode(),client)
            if data[1] == "Up":
                for client in clients:
                    s.sendto("User2:Up:?".encode(),client)
            if data[1] == "Down":
                for client in clients:
                    s.sendto("User2:Down:?".encode(),client)
        if data[0] == "User3":
            if data[1] == "Left":
                for client in clients:
                    s.sendto("User3:Left:?".encode(),client)
            if data[1] == "Right":
                for client in clients:
                    s.sendto("User3:Right:?".encode(),client)
            if data[1] == "Up":
                for client in clients:
                    s.sendto("User3:Up:?".encode(),client)
            if data[1] == "Down":
                for client in clients:
                    s.sendto("User3:Down:?".encode(),client)
        if data[0] == "User4":
            if data[1] == "Left":
                for client in clients:
                    s.sendto("User4:Left:?".encode(),client)
            if data[1] == "Right":
                for client in clients:
                    s.sendto("User4:Right:?".encode(),client)
            if data[1] == "Up":
                for client in clients:
                    s.sendto("User4:Up:?".encode(),client)
            if data[1] == "Down":
                for client in clients:
                    s.sendto("User4:Down:?".encode(),client)
        if data[0] == "Score":
            cur.execute("SELECT * FROM Login WHERE Username = '{}'".format(data[1]))
            info = cur.fetchone()
            if int(info[2]) < int(data[2]):
                cur.execute("UPDATE Login SET Highscore = '{}' WHERE Username = '{}'".format(data[2],data[1]))
                con.commit()

        if data[0] == "NumberOfPlayers":
            for client in clients:
                s.sendto("NumberOfPlayers:{}:?".format(num_users).encode(),client)
                
        if data[0] == "RandApple":
            display_width = int(data[1])
            display_height = int(data[2])
            apple_thickness = int(data[3])
            randapplex = round(random.randrange(0,display_width - apple_thickness))
            randappley = round(random.randrange(0,display_height - apple_thickness))
            #print("NEW X {} and NEW Y {} FOR APPLE".format(randapplex,randappley))
            for client in clients:
                s.sendto("RandApple:{}:{}".format(randapplex,randappley).encode(),client)
        
            
            
        
        else:
            for client in clients:
                s.sendto("{}:{}:{}".format(data[0],data[1],data[2]).encode(),client)

    except:
        pass
