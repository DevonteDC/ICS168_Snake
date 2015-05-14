import socket
import time
import sqlite3

host = '127.0.0.1'
port = 5000
@@ -10,6 +11,12 @@ s  = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

con = sqlite3.connect('snaketest.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Login (Username TEXT, Password TEXT)")
con.commit()
num_users = 0

quitting = False
print("Server Started")

@@ -18,12 +25,45 @@ while not quitting:

        data, addr = s.recvfrom(1024)
        data = data.decode()
        data = data.split(":")
        if addr not in clients:
            clients.append(addr)

        print(time.ctime(time.time()) + str(addr) + ' : : ' + str(data))
        
        if data[0] == "User":
            num_users += 1
            if num_users == 1:
                s.sendto("1User:?:?".encode(),addr)
            if num_users == 2:
                s.sendto("2User:?:?".encode(),addr)
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
        else:
            for client in clients:
                s.sendto("{}:?:?".format(data[0]).encode(),client)

    except:
        pass
