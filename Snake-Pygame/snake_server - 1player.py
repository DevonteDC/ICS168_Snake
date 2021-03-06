import pygame
import time
import random
import inputbox
import sqlite3
import socket
import ipgetter
local = "127.0.0.1"
external = str(ipgetter.myip())


host = local
port = 20000


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))

num_users = 0


##DATABASE VARIABLES----
con = sqlite3.connect('snaketest.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Login (Username TEXT, Password TEXT)")
con.commit()
print("Server Started")


##DATABASE VARIABLES----

while True:
    data,addr = s.recvfrom(1024)
    data = data.decode()
    data = data.split(":")
    if data[0] == "Login":
        username = data[1]
        password = data[2]
        print("PASSWORD RECEIVED: ",password," TYPE: ",type(password))
        cur.execute("SELECT COUNT(*) FROM Login WHERE Username = '{}'".format(username))
        info = cur.fetchone()
        print(info)
        if info[0] == 0:
            print("New User Acquired: {}   Password {}".format(username,password))
            cur.execute("INSERT INTO Login VALUES('{}','{}')".format(username,password))
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
            s.sendto("User1:?:?".encode(),addr)
        else:
            s.sendto("User2:?:?".encode(),addr)

        
    



            
            
        
    
    
