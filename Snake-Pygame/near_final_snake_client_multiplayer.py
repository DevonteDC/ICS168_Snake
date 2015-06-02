import pygame
import time
import random
import inputbox
import sqlite3
import socket
import ipgetter
import hashlib
import threading


class SnakeGame():

    def initGraphics(self):
        ###IMAGES---------------------------
        self.snake_head = pygame.image.load('snakehead.png')
        self.apple = pygame.image.load('apple.png')
        self.background = pygame.image.load('SnakeBackground.png')
        self.titleScreen = pygame.image.load('SnakeTitle.png')
        ###IMAGES---------------------------

        #SOUND----------
        self.titleMusic = pygame.mixer.Sound('pac.wav')
        self.eatSound = pygame.mixer.Sound('eat.wav')
        #SOUND----------

        #---ICON---
        self.icon = pygame.image.load('apple.png')
        pygame.display.set_icon(self.icon)
        #---ICON---
        
    def __init__(self):
        pygame.init()

        self.tLock = threading.Lock()
        self.shutdown = False

        self.host = '127.0.0.1'
        self.port = 10019

        self.server = ('127.0.0.1',20000)
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind((self.host,self.port))
        self.s.setblocking(0)
        self.rt = threading.Thread(target = self.receiving, args = ('RecvThread',self.s))
        self.rt.start()

        
        self.display_width = 800
        self.display_height = 600

        self.username = ""
        self.username2 = ""
        self.username3 = ""
        self.username4 = ""
        self.name = ""
        self.session = ""
        self.numberOfPlayers = 0
   

        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Snake 168')

        self.clock = pygame.time.Clock()

        self.block_size = 20
        self.AppleThickness = 30
        self.FPS = 20

        self.direction = 'right'
        self.direction2 = 'left'
        self.direction3 = 'right'
        self.direction4 = 'left'

        self.lead_x = 0
        self.lead_x_change = 0
        self.lead_y = 0
        self.lead_y_change = 0
        
        self.lead_x2 = 0
        self.lead_y2 = 0
        self.lead_x2_change = 0
        self.lead_y2_change = 0

        self.lead_x3 = 0
        self.lead_y3 = 0
        self.lead_y3_change = 0
        self.lead_y3_change = 0

        self.lead_x4 = 0
        self.lead_y4 = 0
        self.lead_y4_change = 0
        self.lead_y4_change = 0
        
        self.snakeList = []
        self.snakeList2 = []
        self.snakeList3 = []
        self.snakeList4 = []
        
        self.snakeHead = []
        self.snakeHead2 = []
        self.snakeHead3 = []
        self.snakeHead4 = []
        
        self.snakeLength = 1
        self.snakeLength2 = 1
        self.snakeLength3 = 1
        self.snakeLength4 = 1
        
        self.randAppleX = 0
        self.randAppleY = 0

        self.tinyfont = pygame.font.SysFont("comicsansms",12)
        self.smallfont = pygame.font.SysFont("comicsansms",25)
        self.medfont = pygame.font.SysFont("comicsansms",50)
        self.largefont = pygame.font.SysFont("comicsansms",80)

        self.white = (255,255,255)
        self.black = (0,0,0)
        self.red = (200,0,0)
        self.light_red = (255,0,0)
        self.green = (0,155,0)
        self.light_green = (0,255,0)
        self.yellow = (200,200,0)
        self.light_yellow = (255,255,0)
        self.light_blue = (0,0,155)
        self.user1 = False
        self.user2 = False
        self.user3 = False
        self.user4 = False
        self.do_pause = False
        self.paused = False
        self.user1score = 0
        self.user2score = 0
        self.user3score = 0
        self.user4score = 0
        self.show1 = False
        self.show2 = False
        self.show3 = False
        self.show4 = False
        self.gametime = False
        self.invalidtime = False
        

        self.initGraphics()

        

    def receiving(self,name,sock):
        while not self.shutdown:
            try:
                self.tLock.acquire()
                while True:
                    data, addr = sock.recvfrom(1024)
                    data = data.decode()
                    data = data.split(":")
                    #print("THIS DATA: ",data)
                    if data[0] == "play":
                        pass
                        #print("We Are Playing")
                    if data[0] == "1score":
                        self.user1score += 1
                        self.score(int(data[1]),"user1")
                    if data[0] == "2score":
                        self.user2score += 1
                        self.score(int(data[1]),"user2")
                    if data[0] == "3score":
                        self.user3score += 1
                        self.score(int(data[1]),"user3")
                    if data[0] == "4score":
                        self.user4score += 1
                        self.score(int(data[1]),"user4")

                    if data[0] == "GameName":
                        if data[1] == "user1":
                            self.username = data[2]
                        if data[1] == "user2":
                            self.username2 = data[2]
                        if data[1] == "user3":
                            self.username3 = data[2]
                        if data[1] == "user4":
                            self.username4 = data[2]
                    if data[0] == "Pause":
                        self.do_pause = True

                    if data[0] == "Gameloop":
                        self.s.sendto("User:?:?".encode(),self.server)
                        self.s.sendto("NumberOfPlayers:?:?".encode(),self.server)
                        self.gametime = True
                    if data[0] == "Invalidpass":
                        self.invalidtime = True
                    if data[0] == "NumberOfPlayers":
                        self.numberOfPlayers = int(data[1])
                        if self.numberOfPlayers == 1:
                            self.show1 = True
                        if self.numberOfPlayers == 2:
                            self.show1 = True
                            self.show2 = True
                        if self.numberOfPlayers == 3:
                            self.show1 = True
                            self.show2 = True
                            self.show3 = True
                        if self.numberOfPlayers == 4:
                            self.show1 = True
                            self.show2 = True
                            self.show3 = True
                            self.show4 = True
                            
                    if data[0] == "DonePause":
                        self.do_pause = False
                        self.paused = False
                    if data[0] == "1Quit":
                        self.show1 = False
                    if data[0] == "2Quit": 
                        self.show2 = False
                    if data[0] == "3Quit":
                        self.show3 = False
                    if data[0] == "4Quit":
                        self.show4 = False
                        
        
                    if data[0] == "1User":
                        #print("I AM USER 1")
                        self.user1 = True
                        self.username = self.name
                    if data[0] == "2User":
                        #print("I AM USER 2")
                        self.user2 = True
                        self.username2 = self.name
                    if data[0] == "3User":
                        #print("I AM USER 3")
                        self.user3 = True
                        self.username3 = self.name
                    if data[0] == "4User":
                        #print("I AM USER 4")
                        self.user4 = True
                        self.username4 = self.name
                        
                    if data[0] == "RandApple":
                        #print("THIS IS THE DATA {} AND {}".format(data[1],data[2]))
                        self.randAppleX = int(data[1])
                        self.randAppleY = int(data[2])
                    
                    if data[0] == "User1" and self.show1:
                        if data[1] == "Left":
                            self.lead_x_change =  -self.block_size
                            self.lead_y_change = 0
                            self.direction = 'left'
                        if data[1] == "Right":
                            self.lead_x_change = self.block_size
                            self.lead_y_change = 0
                            self.direction = 'right'
                        if data[1] == "Up":
                            self.lead_y_change =  -self.block_size
                            self.lead_x_change = 0
                            self.direction = 'up'
                        if data[1] == "Down":
                            self.lead_y_change = self.block_size
                            self.lead_x_change = 0
                            self.direction = 'down'
                            
                    if data[0] == "User2" and self.show2:
                        if data[1] == "Left":
                            self.lead_x2_change =  -self.block_size
                            self.lead_y2_change = 0
                            self.direction2 = 'left'
                        if data[1] == "Right":
                            self.lead_x2_change = self.block_size
                            self.lead_y2_change = 0
                            self.direction2 = 'right'
                        if data[1] == "Up":
                            self.lead_y2_change =  -self.block_size
                            self.lead_x2_change = 0
                            self.direction2 = 'up'
                        if data[1] == "Down":
                            self.lead_y2_change = self.block_size
                            self.lead_x2_change = 0
                            self.direction2 = 'down'

                    if data[0] == "User3" and self.show3:
                        if data[1] == "Left":
                            self.lead_x3_change =  -self.block_size
                            self.lead_y3_change = 0
                            self.direction3 = 'left'
                        if data[1] == "Right":
                            self.lead_x3_change = self.block_size
                            self.lead_y3_change = 0
                            self.direction3 = 'right'
                        if data[1] == "Up":
                            self.lead_y3_change =  -self.block_size
                            self.lead_x3_change = 0
                            self.direction3 = 'up'
                        if data[1] == "Down":
                            self.lead_y3_change = self.block_size
                            self.lead_x3_change = 0
                            self.direction3 = 'down'

                    if data[0] == "User4" and self.show4:
                        if data[1] == "Left":
                            self.lead_x4_change =  -self.block_size
                            self.lead_y4_change = 0
                            self.direction4 = 'left'
                        if data[1] == "Right":
                            self.lead_x4_change = self.block_size
                            self.lead_y4_change = 0
                            self.direction4 = 'right'
                        if data[1] == "Up":
                            self.lead_y4_change =  -self.block_size
                            self.lead_x4_change = 0
                            self.direction4 = 'up'
                        if data[1] == "Down":
                            self.lead_y4_change = self.block_size
                            self.lead_x4_change = 0
                            self.direction4 = 'down'
                            
                    
                    
                            
                    
            except:
                pass
            finally:
                self.tLock.release()
                
    def pause(self):
        self.paused = True
        self.message_to_screen("Paused",
                          self.black,
                          -100,
                          'large')
        self.message_to_screen("Press C to continue or Q to quit.",
                          self.black,
                          25)
        

        pygame.display.update()

        while self.paused:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.s.sendto("DonePause:?:?".encode(),self.server)
                        self.paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
           
            
            self.clock.tick(5)

    def score(self,score,user_score):
        text = self.smallfont.render("Score: " + str(score),True,self.black)
        if user_score == "user1":
            self.gameDisplay.blit(text,[0,0])
        elif user_score == "user2":
            self.gameDisplay.blit(text,[200,0])
        elif user_score == "user3":
            self.gameDisplay.blit(text,[400,0])
        elif user_score == "user4":
            self.gameDisplay.blit(text,[600,0])
            

    def displayUsername(self,user,x,y):
        text = self.tinyfont.render("Username: " + user,True,self.black)
        self.gameDisplay.blit(text,[x,y])
       

    def randAppleGen(self):
        randAppleX = round(random.randrange(0,self.display_width - self.AppleThickness))#/10.0) * 10.0
        randAppleY = round(random.randrange(0,self.display_height - self.AppleThickness))#/10.0) * 10.0
        return randAppleX, randAppleY

    def text_objects(self,text,color,size):
        if size == "small":
            textSurface = self.smallfont.render(text,True,color)
        elif size == "medium":
            textSurface = self.medfont.render(text,True,color)
        elif size == "large":
            textSurface = self.largefont.render(text,True,color)
        return textSurface, textSurface.get_rect()

    def text_to_button(self,msg, color, buttonx, buttony, buttonwidth, buttonheight,size = "small"):
        textSurf, textRect = self.text_objects(msg,color,size)
        textRect.center = (buttonx + (buttonwidth/2), buttony+(buttonheight/2))
        self.gameDisplay.blit(textSurf,textRect)

    def message_to_screen(self,msg,color,y_displace = 0, size = 'small'):
        textSurf, textRect = self.text_objects(msg,color,size)
        textRect.center = (self.display_width / 2), (self.display_height / 2) + y_displace
        self.gameDisplay.blit(textSurf,textRect)

    def game_controls(self):
        gcont = True

        while gcont:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    #s.close()
                    pygame.quit()
                    quit()
                

            
            self.gameDisplay.blit(self.background,(0,0))
            self.message_to_screen("Controls",
                              self.green,
                              -100,
                              'large')

            self.message_to_screen("WASD Movement",
                              self.black,
                              -30)
            
            self.message_to_screen("Pause: P",
                              self.black,
                              10)
            
            


            

            self.button("Play",150,500,100,50,self.green,self.light_green, action = 'Play')
            
            self.button("Quit",550,500,100,50,self.red,self.light_red,action='Quit')

            

            pygame.display.update()
            self.clock.tick(15)

    def button(self,text,x,y,width,height,inactive_color,active_color,action = None):
    
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        

        if x + width > cur[0] > x and y + height > cur[1] > y:
            pygame.draw.rect(self.gameDisplay,active_color,(x,y,width,height))
            if click[0] == 1 and action != None:
                if action == 'Quit':

                    #s.close()
                    pygame.quit()
                    quit()
                if action == 'Controls':
                    self.game_controls()
                    
                if action == 'Play' or action == 'Redo':
                    self.s.sendto("play:?:?".encode(),self.server)
                    self.tLock.acquire()
                    self.tLock.release()
                    self.titleMusic.stop()
                    self.UserPass()

                if action == 'Begin':
                    if self.user1:
                        self.s.sendto("GameName:user1:{}".format(self.username).encode(),self.server)
                    if self.user2:
                        self.s.sendto("GameName:user2:{}".format(self.username2).encode(),self.server)
                    if self.user3:
                        self.s.sendto("GameName:user3:{}".format(self.username3).encode(),self.server)
                    if self.user4:
                        self.s.sendto("GameName:user4:{}".format(self.username4).encode(),self.server)
                    self.gameLoop()

                if action == 'Join':
                    self.joinSession()
                    
                    

                
                    

                
                
                
        else:
            pygame.draw.rect(self.gameDisplay,inactive_color,(x,y,width,height))

        self.text_to_button(text,self.black,x,y,width,height)

    def InvalidPass(self):
        self.invalidtime = False
        ipass = True

        while ipass:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    #s.close()
                    pygame.quit()
                    quit()
                

            
            self.gameDisplay.blit(self.background,(0,0))

            self.message_to_screen("Invalid Password, Redo",
                              self.red,
                              -100,
                              'medium')
            self.button("Redo",150,500,100,50,self.green,self.light_green, action = 'Redo')

            pygame.display.update()
            self.clock.tick(15)
        
    

    def UserPass(self):
        
        userp = True
        noStartGame = True

        while userp:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    #s.close()
                    pygame.quit()
                    quit()
                

            
            self.gameDisplay.blit(self.background,(0,0))

            
            
            
            
            
            ##SERVER LOGIN##
           

            self.name = inputbox.ask(self.gameDisplay,"UserName")
            password = inputbox.ask(self.gameDisplay,"Password")

            #self.s.sendto("User:?:?".encode(),self.server)
            #self.s.sendto("NumberOfPlayers:?:?".encode(),self.server)

            
            
            
            self.tLock.acquire()
            self.tLock.release()
            time.sleep(0.2)
            #self.shutdown = True
            #rt.join()
            #self.s.close()
            
            
            password = hashlib.md5(password.encode()).hexdigest()
            #print("PASSWORD BEFORE SENDING: ",password," TYPE: ",type(password))
            self.s.sendto("Login:{}:{}".format(self.name,password).encode(),self.server)
            while noStartGame == True:
                if self.gametime == True:
                    self.waitingRoom()
                if self.invalidtime == True:
                    self.InvalidPass()
                
                
                
                    
            ##SERVER LOGIN##
            
                    
                    
                
            
            


            


            

            pygame.display.update()
            self.clock.tick(15)

    def joinSession(self):
        
        joins = True
        #noStartGame = True

        while joins:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    #s.close()
                    pygame.quit()
                    quit()
                

            
            self.gameDisplay.blit(self.background,(0,0))

            
          
            ##SERVER LOGIN##
            self.session = inputbox.ask(self.gameDisplay,"Session Name")
            self.s.sendto("User:?:?".encode(),self.server)
            self.tLock.acquire()
            self.tLock.release()
            time.sleep(0.2)
        

            
            
           
            self.waitingRoom()
            
                    
                
            
            


            


            

            pygame.display.update()
            self.clock.tick(15)

    def snake(self,block_size,snakeList,direc):

        if direc == 'right':
            head = pygame.transform.rotate(self.snake_head,270)
        if direc == 'left':
            head = pygame.transform.rotate(self.snake_head,90)
        if direc == 'up':
            head = self.snake_head
        if direc == 'down':
            head = pygame.transform.rotate(self.snake_head,180)
            
        self.gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
        for XnY in snakeList[:-1]:
            pygame.draw.rect(self.gameDisplay, self.black,[XnY[0],XnY[1],block_size,block_size])
            pygame.draw.rect(self.gameDisplay,self.green,[XnY[0],XnY[1],block_size - 1,block_size - 1])


    def game_intro(self):

        intro = True

        
        self.titleMusic.play()
        while intro:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    #s.close()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    
                        
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

            self.gameDisplay.blit(self.titleScreen,(0,0))
            #gameDisplay.fill(white)
            


            #message_to_screen("Press C to play, P to pause, or Q to quit",
                              #black,
                              #180)
            

            self.button("play",500,120,100,50,self.green,self.light_green, action = 'Play')
            self.button("controls",500,190,100,50,self.yellow,self.light_yellow,action='Controls')
            self.button("quit",500,260,100,50,self.red,self.light_red,action='Quit')
            self.button("join",500,330,100,50,self.light_blue,self.white,action ='Join')

            

            pygame.display.update()
            self.clock.tick(15)


    def waitingRoom(self):
        waiting = True

        if self.user1:
            self.username = self.name
        if self.user2:
            self.username2 = self.name
           
        if self.user3:
            self.username3 = self.name
            
        if self.user4:
            self.username4 = self.name
            
        
        
        
        
        
        

        
        while waiting:
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    #s.close()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                   
                        
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                

            self.gameDisplay.blit(self.background,(0,0))

           
                 
                

           
                
                #pygame.display.update()
            self.button("Ready",150,500,100,50,self.red,self.light_red,action = "Begin")
            
            
            pygame.display.update()
            self.clock.tick(15)



    def gameLoop(self):
        #global user1
        #global user2
        #global direction
        #global direction2

        
        gameExit = False
        gameOver = False
        self.lead_x = 100
        self.lead_y = 100

        self.lead_x2 = self.display_width - 100
        self.lead_y2 = 100

        self.lead_x3 = 100
        self.lead_y3 = self.display_height - 100

        self.lead_x4 = self.display_width - 100
        self.lead_y4 = self.display_height - 100

           
        self.lead_x_change = 0
        self.lead_y_change = 0


        self.lead_x2_change = 0
        self.lead_y2_change = 0

        self.lead_x3_change = 0
        self.lead_y3_change = 0

        self.lead_x4_change = 0
        self.lead_y4_change = 0


        self.snakeList = []
        self.snakeLength = 1

        self.snakeList2 = []
        self.snakeLength2 = 1

        self.snakeList3 = []
        self.snakeLength3 = 1

        self.snakeList4 = []
        self.snakeLength4 = 1

        self.s.sendto("RandApple:{}:{}:{}".format(self.display_width,self.display_height,self.AppleThickness).encode(),self.server)
        if self.numberOfPlayers == 1:
            self.show1 = True
        if self.numberOfPlayers == 2:
            self.show1 = True
            self.show2 = True
        if self.numberOfPlayers == 3:
            self.show1 = True
            self.show2 = True
            self.show3 = True
        if self.numberOfPlayers == 4:
            self.show1 = True
            self.show2 = True
            self.show3 = True
            self.show4 = True
        #print("INITIATION OF APPLE")
        self.tLock.acquire()
        self.tLock.release()
        #self.randAppleX,self.randAppleY = self.randAppleGen()
        
        
        while gameExit == False:
        

            

            if gameOver == True:
                self.message_to_screen("Game over",
                                  self.red,
                                  -50,
                                  size = 'large')
                
                self.message_to_screen("Press C to play again or Q to quit",
                                  self.black,
                                  50,
                                  size = 'medium')
                pygame.display.update()
                

            while gameOver == True:
                self.direction = 'right'
                self.direction2 = 'left'
                self.direction3 = 'right'
                self.direction4 = 'left'

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True
                            gameOver = False
                        
                            
            for event in pygame.event.get():
                if self.do_pause:
                    self.pause()
                    
                if event.type == pygame.QUIT:
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if self.user1:
                        if event.key == pygame.K_LEFT and self.direction != 'right':
                            self.s.sendto("User1:Left:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                                
                            
                        elif event.key == pygame.K_RIGHT and self.direction != 'left':
                            self.s.sendto("User1:Right:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                            
                        
                        elif event.key == pygame.K_UP and self.direction !='down':
                            self.s.sendto("User1:Up:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                           
                       
                        elif event.key == pygame.K_DOWN and self.direction !='up':
                            self.s.sendto("User1:Down:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                            
                        elif event.key ==  pygame.K_p:
                            self.s.sendto("Pause:?:?".encode(),self.server)
                            
                            
                            
                
                            
                                
                           
                    if self.user2:
                        if event.key == pygame.K_LEFT and self.direction2 != 'right':
                                self.s.sendto("User2:Left:?".encode(),self.server)
                                self.tLock.acquire()
                                self.tLock.release()
                                
                                
                            
                        elif event.key == pygame.K_RIGHT and self.direction2 != 'left':
                            self.s.sendto("User2:Right:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                            
                        
                        elif event.key == pygame.K_UP and self.direction2 !='down':
                            self.s.sendto("User2:Up:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                            
                       
                        elif event.key == pygame.K_DOWN and self.direction2 !='up':
                            self.s.sendto("User2:Down:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                            
                        
                        elif event.key ==  pygame.K_p:
                            self.s.sendto("Pause:?:?".encode(),self.server)

                    if self.user3:
                        if event.key == pygame.K_LEFT and self.direction3 != 'right':
                            self.s.sendto("User3:Left:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                                
                            
                        elif event.key == pygame.K_RIGHT and self.direction3 != 'left':
                            self.s.sendto("User3:Right:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                            
                        
                        elif event.key == pygame.K_UP and self.direction3 !='down':
                            self.s.sendto("User3:Up:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                           
                       
                        elif event.key == pygame.K_DOWN and self.direction3 !='up':
                            self.s.sendto("User3:Down:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                            
                        elif event.key ==  pygame.K_p:
                            self.s.sendto("Pause:?:?".encode(),self.server)

                    if self.user4:
                        if event.key == pygame.K_LEFT and self.direction4 != 'right':
                            self.s.sendto("User4:Left:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                                
                            
                        elif event.key == pygame.K_RIGHT and self.direction4 != 'left':
                            self.s.sendto("User4:Right:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                            
                        
                        elif event.key == pygame.K_UP and self.direction4 !='down':
                            self.s.sendto("User4:Up:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                           
                       
                        elif event.key == pygame.K_DOWN and self.direction4 !='up':
                            self.s.sendto("User4:Down:?".encode(),self.server)
                            self.tLock.acquire()
                            self.tLock.release()
                            
                            
                        elif event.key ==  pygame.K_p:
                            self.s.sendto("Pause:?:?".encode(),self.server)
                        
                
                    
            
            
            
            
            if self.lead_x >= self.display_width or self.lead_x < 0 or self.lead_y >= self.display_height or self.lead_y < 0:
                self.show1 = False
                print("MY USERNAME!!! ",self.username)
                self.s.sendto("Score:{}:{}".format(self.username,self.user1score).encode(),self.server)
                gameOver = True

            if self.lead_x2 >= self.display_width or self.lead_x2 < 0 or self.lead_y2 >= self.display_height or self.lead_y2 < 0:
                self.show2 = False
                self.s.sendto("Score:{}:{}".format(self.username2,self.user2score).encode(),self.server)
                gameOver = True

            if self.lead_x3 >= self.display_width or self.lead_x3 < 0 or self.lead_y3 >= self.display_height or self.lead_y3 < 0:
                self.show3 = False
                self.s.sendto("Score:{}:{}".format(self.username3,self.user3score).encode(),self.server)
                gameOver = True

            if self.lead_x4 >= self.display_width or self.lead_x4 < 0 or self.lead_y4 >= self.display_height or self.lead_y4 < 0:
                self.show4 = False
                self.s.sendto("Score:{}:{}".format(self.username4,self.user4score).encode(),self.server)
                gameOver = True

            self.lead_x += self.lead_x_change
            self.lead_y += self.lead_y_change

            self.lead_x2 += self.lead_x2_change
            self.lead_y2 += self.lead_y2_change

            self.lead_x3 += self.lead_x3_change
            self.lead_y3 += self.lead_y3_change

            self.lead_x4 += self.lead_x4_change
            self.lead_y4 += self.lead_y4_change
                
               
                    
            self.gameDisplay.blit(self.background,(0,0))

            
            #pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,AppleThickness,AppleThickness])
            self.gameDisplay.blit(self.apple,(self.randAppleX,self.randAppleY))

            
            self.snakeHead = []
            self.snakeHead.append(self.lead_x)
            self.snakeHead.append(self.lead_y)
            self.snakeList.append(self.snakeHead)

            self.snakeHead2 = []
            self.snakeHead2.append(self.lead_x2)
            self.snakeHead2.append(self.lead_y2)
            self.snakeList2.append(self.snakeHead2)

            self.snakeHead3 = []
            self.snakeHead3.append(self.lead_x3)
            self.snakeHead3.append(self.lead_y3)
            self.snakeList3.append(self.snakeHead3)

            self.snakeHead4 = []
            self.snakeHead4.append(self.lead_x4)
            self.snakeHead4.append(self.lead_y4)
            self.snakeList4.append(self.snakeHead4)

            if len(self.snakeList) > self.snakeLength:
                del self.snakeList[0]

            if len(self.snakeList2) > self.snakeLength2:
                del self.snakeList2[0]

            if len(self.snakeList3) > self.snakeLength3:
                del self.snakeList3[0]

            if len(self.snakeList4) > self.snakeLength4:
                del self.snakeList4[0]
            
            for eachSegment in self.snakeList[:-1]:
                if eachSegment == self.snakeHead:
                    gameOver = True

            for eachSegment in self.snakeList2[:-1]:
                if eachSegment == self.snakeHead2:
                    gameOver = True

            for eachSegment in self.snakeList3[:-1]:
                if eachSegment == self.snakeHead3:
                    gameOver = True

            for eachSegment in self.snakeList4[:-1]:
                if eachSegment == self.snakeHead4:
                    gameOver = True

        

            if self.show1:
                self.snake(self.block_size,self.snakeList,self.direction)
                self.score(self.user1score,"user1")
                self.displayUsername(self.username,0,25)
            if self.show2:
                self.snake(self.block_size,self.snakeList2,self.direction2)
                self.score(self.user2score,"user2")
                self.displayUsername(self.username2,200,25)
            if self.show3:
                self.snake(self.block_size,self.snakeList3,self.direction3)
                self.score(self.user3score,"user3")
                self.displayUsername(self.username3,400,25)
            if self.show4:
                self.snake(self.block_size,self.snakeList4,self.direction4)
                self.score(self.user4score,"user4")
                self.displayUsername(self.username4,600,25)
            
            """if self.user1:
                self.score(self.user1score,"user1")
                self.score(self.user2score,"user2")
                self.score(self.user3score,"user3")
                self.score(self.user4score,"user4")
            if self.user2:
                self.score(self.user2score,"user2")
                self.score(self.user1score,"user1")
                self.score(self.user3score,"user3")
                self.score(self.user4score,"user4")
            if self.user3:
                self.score(self.user3score,"user3")
                self.score(self.user1score,"user1")
                self.score(self.user2score,"user2")
                self.score(self.user4score,"user4")
            if self.user4:
                self.score(self.user4score,"user4")
                self.score(self.user1score,"user1")
                self.score(self.user2score,"user2")
                self.score(self.user3score,"user3") 
            self.displayUsername(self.username,0,25)
            self.displayUsername(self.username2,200,25)
            self.displayUsername(self.username3,400,25)
            self.displayUsername(self.username4,600,25) """
           

            
            
            
            
            pygame.display.update()



            if self.lead_x > self.randAppleX and self.lead_x < self.randAppleX + self.AppleThickness or self.lead_x + self.block_size > self.randAppleX and self.lead_x + self.block_size < self.randAppleX + self.AppleThickness:
                if self.lead_y > self.randAppleY and self.lead_y < self.randAppleY + self.AppleThickness or self.lead_y + self.block_size > self.randAppleY and self.lead_y + self.block_size < self.randAppleY + self.AppleThickness:
                    self.eatSound.play()
                    self.s.sendto("RandApple:{}:{}:{}".format(self.display_width,self.display_height,self.AppleThickness).encode(),self.server)
                    #print("COLLISION WITH SNAKE 1")
                    self.tLock.acquire()
                    self.tLock.release()
                    self.snakeLength += 1
                    self.s.sendto("1score:{}:?".format(self.snakeLength - 1).encode(),self.server)

            if self.lead_x2 > self.randAppleX and self.lead_x2 < self.randAppleX + self.AppleThickness or self.lead_x2 + self.block_size > self.randAppleX and self.lead_x2 + self.block_size < self.randAppleX + self.AppleThickness:
                if self.lead_y2 > self.randAppleY and self.lead_y2 < self.randAppleY + self.AppleThickness or self.lead_y2 + self.block_size > self.randAppleY and self.lead_y2 + self.block_size < self.randAppleY + self.AppleThickness:
                    self.eatSound.play()
                    self.s.sendto("RandApple:{}:{}:{}".format(self.display_width,self.display_height,self.AppleThickness).encode(),self.server)
                    #print("COLLISION WITH SNAKE 2")
                    self.tLock.acquire()
                    self.tLock.release()
                    self.snakeLength2 += 1
                    self.s.sendto("2score:{}:?".format(self.snakeLength2 - 1).encode(),self.server)

            if self.lead_x3 > self.randAppleX and self.lead_x3 < self.randAppleX + self.AppleThickness or self.lead_x3 + self.block_size > self.randAppleX and self.lead_x3 + self.block_size < self.randAppleX + self.AppleThickness:
                if self.lead_y3 > self.randAppleY and self.lead_y3 < self.randAppleY + self.AppleThickness or self.lead_y3 + self.block_size > self.randAppleY and self.lead_y3 + self.block_size < self.randAppleY + self.AppleThickness:
                    self.eatSound.play()
                    self.s.sendto("RandApple:{}:{}:{}".format(self.display_width,self.display_height,self.AppleThickness).encode(),self.server)
                    #print("COLLISION WITH SNAKE 3")
                    self.tLock.acquire()
                    self.tLock.release()
                    self.snakeLength3 += 1
                    self.s.sendto("3score:{}:?".format(self.snakeLength3 - 1).encode(),self.server)

            if self.lead_x4 > self.randAppleX and self.lead_x4 < self.randAppleX + self.AppleThickness or self.lead_x4 + self.block_size > self.randAppleX and self.lead_x4 + self.block_size < self.randAppleX + self.AppleThickness:
                if self.lead_y4 > self.randAppleY and self.lead_y4 < self.randAppleY + self.AppleThickness or self.lead_y4 + self.block_size > self.randAppleY and self.lead_y4 + self.block_size < self.randAppleY + self.AppleThickness:
                    self.eatSound.play()
                    self.s.sendto("RandApple:{}:{}:{}".format(self.display_width,self.display_height,self.AppleThickness).encode(),self.server)
                    #print("COLLISION WITH SNAKE 4")
                    self.tLock.acquire()
                    self.tLock.release()
                    self.snakeLength4 += 1
                    self.s.sendto("4score:{}:?".format(self.snakeLength4 - 1).encode(),self.server)


            
                    
            
                
            self.clock.tick(self.FPS)
        if self.user1:
            self.s.sendto("1Quit:?:?".encode(),self.server)
        if self.user2:
            self.s.sendto("2Quit:?:?".encode(),self.server)
        if self.user3:
            self.s.sendto("3Quit:?:?".encode(),self.server)
        if self.user4:
            self.s.sendto("4Quit:?:?".encode(),self.server)
            
        pygame.quit() 
        quit()



SG = SnakeGame()
while 1:
    SG.game_intro()
    
    

    
