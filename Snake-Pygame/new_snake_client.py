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
        self.port = 10012

        self.server = ('127.0.0.1',5000)
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind((self.host,self.port))
        self.s.setblocking(0)
        self.rt = threading.Thread(target = self.receiving, args = ('RecvThread',self.s))
        self.rt.start()

        
        self.display_width = 800
        self.display_height = 600

        self.username = ""

        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Snake 168')

        self.clock = pygame.time.Clock()

        self.block_size = 20
        self.AppleThickness = 30
        self.FPS = 20

        self.direction = 'right'
        self.direction2 = 'left'

        self.lead_x = 0
        self.lead_x_change = 0
        self.lead_y = 0
        self.lead_y_change = 0
        self.lead_x2 = 0
        self.lead_y2 = 0
        self.lead_x2_change = 0
        self.lead_y2_change = 0
        self.snakeList = []
        self.snakeList2 = []
        self.snakeHead = []
        self.snakeHead2 = []
        self.snakeLength = 1
        self.snakeLength2 = 1
        self.randAppleX = 0
        self.randAppleY = 0

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
        self.user1 = False
        self.user2 = False

        self.initGraphics()

        

    def receiving(self,name,sock):
        while not self.shutdown:
            try:
                self.tLock.acquire()
                while True:
                    data, addr = sock.recvfrom(1024)
                    data = data.decode()
                    data = data.split(":")
                    if data[0] == "a":
                        print("WE GOT AN A")
                    if data[0] == "play":
                        print("We Are Playing")
                    if data[0] == "1User":
                        print("I AM USER 1")
                        self.user1 = True
                    if data[0] == "2User":
                        print("I AM USER 2")
                        self.user2 = True
                    if data[0] == "Pause":
                        self.pause()
                    if data[0] == "User1":
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
                            
                    if data[0] == "User2":
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
                    
                            
                    
            except:
                pass
            finally:
                self.tLock.release()
                
    def pause(self):
        paused = True

        self.message_to_screen("Paused",
                          self.black,
                          -100,
                          'large')
        self.message_to_screen("Press C to continue or Q to quit.",
                          self.black,
                          25)

        pygame.display.update()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
           
            
            self.clock.tick(5)

    def score(self,score):
        text = self.smallfont.render("Score: " + str(score),True,self.black)
        self.gameDisplay.blit(text,[0,0])

    def displayUsername(self):
        text = self.smallfont.render("Username: " + self.username,True,self.black)
        self.gameDisplay.blit(text,[200,0])

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
                    self.gameLoop()
                    
                    

                
                    

                
                
                
        else:
            pygame.draw.rect(self.gameDisplay,inactive_color,(x,y,width,height))

        self.text_to_button(text,self.black,x,y,width,height)

    def InvalidPass(self):
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
        #noStartGame = True

        while userp:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    #s.close()
                    pygame.quit()
                    quit()
                

            
            self.gameDisplay.blit(self.background,(0,0))

            
          
            ##SERVER LOGIN##
            self.username = inputbox.ask(self.gameDisplay,"UserName")
            password = inputbox.ask(self.gameDisplay,"Password")

            
            
            self.s.sendto("User:?:?".encode(),self.server)
            self.tLock.acquire()
            self.tLock.release()
            time.sleep(0.2)
            #self.shutdown = True
            #rt.join()
            #self.s.close()
            
            self.waitingRoom()
            """
            password = hashlib.md5(password.encode()).hexdigest()
            print("PASSWORD BEFORE SENDING: ",password," TYPE: ",type(password))
            s.sendto("Login:{}:{}".format(username,password).encode(),server)
            while noStartGame == True:
                data, addr = s.recvfrom(1024)
                data = data.decode()
                data = data.split(":")
                if data[0] == "Gameloop":
                    s.sendto("User:?:?".encode(),server)
                    data, addr = s.recvfrom(1024)
                    data = data.decode()
                    data = data.split(":")
                    if data[0] == "User1":
                        print("USER!!!")
                        user1 = True
                        waitingRoom()
                    if data[0] == "User2":
                        user2 = True
                        waitingRoom()
                
                if data[0] == "Invalidpass":
                    InvalidPass()
                
                
                    
            ##SERVER LOGIN##
            """
                    
                    
                
            
            


            


            

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

            

            pygame.display.update()
            self.clock.tick(15)


    def waitingRoom(self):
        waiting = True
        
        
        
        lobby = [[self.username,-100]]
        

        
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

           
                 
                

            for player in lobby:
                self.message_to_screen("Waiting for " + player[0],self.red,player[1],'medium')
                
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

           
        self.lead_x_change = 0
        self.lead_y_change = 0

        self.lead_x2_change = 0
        self.lead_y2_change = 0


        self.snakeList = []
        self.snakeLength = 1

        self.snakeList2 = []
        self.snakeLength2 = 1


        self.randAppleX,self.randAppleY = self.randAppleGen()
        
        
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

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True
                            gameOver = False
                        elif event.key == pygame.K_c:
                            self.gameLoop()
                            
            for event in pygame.event.get():
                
                    
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
                            self.tLock.acquire()
                            self.tLock.release()
                            
                
                            
                                
                           
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
                            self.tLock.acquire()
                            self.tLock.release()
                        
                
                    
            
            
            
            
            if self.lead_x >= self.display_width or self.lead_x < 0 or self.lead_y >= self.display_height or self.lead_y < 0:
                gameOver = True

            if self.lead_x2 >= self.display_width or self.lead_x2 < 0 or self.lead_y2 >= self.display_height or self.lead_y2 < 0:
                gameOver = True

            self.lead_x += self.lead_x_change
            self.lead_y += self.lead_y_change

            self.lead_x2 += self.lead_x2_change
            self.lead_y2 += self.lead_y2_change
                
               
                    
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

            if len(self.snakeList) > self.snakeLength:
                del self.snakeList[0]

            if len(self.snakeList2) > self.snakeLength2:
                del self.snakeList2[0]
            
            for eachSegment in self.snakeList[:-1]:
                if eachSegment == self.snakeHead:
                    gameOver = True

            for eachSegment in self.snakeList2[:-1]:
                if eachSegment == self.snakeHead2:
                    gameOver = True
                
            self.snake(self.block_size,self.snakeList,self.direction)
            self.snake(self.block_size,self.snakeList2,self.direction2)
            
            if self.user1:
                self.score(self.snakeLength - 1)
            if self.user2:
                self.score(self.snakeLength2 - 1)
            self.displayUsername()

            
            
            
            
            pygame.display.update()



            if self.lead_x > self.randAppleX and self.lead_x < self.randAppleX + self.AppleThickness or self.lead_x + self.block_size > self.randAppleX and self.lead_x + self.block_size < self.randAppleX + self.AppleThickness:
                if self.lead_y > self.randAppleY and self.lead_y < self.randAppleY + self.AppleThickness or self.lead_y + self.block_size > self.randAppleY and self.lead_y + self.block_size < self.randAppleY + self.AppleThickness:
                    self.eatSound.play()
                    self.randAppleX,self.randAppleY = self.randAppleGen()
                    self.snakeLength += 1

            if self.lead_x2 > self.randAppleX and self.lead_x2 < self.randAppleX + self.AppleThickness or self.lead_x2 + self.block_size > self.randAppleX and self.lead_x2 + self.block_size < self.randAppleX + self.AppleThickness:
                if self.lead_y2 > self.randAppleY and self.lead_y2 < self.randAppleY + self.AppleThickness or self.lead_y2 + self.block_size > self.randAppleY and self.lead_y2 + self.block_size < self.randAppleY + self.AppleThickness:
                    self.eatSound.play()
                    self.randAppleX,self.randAppleY = self.randAppleGen()
                    self.snakeLength2 += 1

            
                    
            
                
            self.clock.tick(self.FPS)
            
        #s.close()
        pygame.quit() 
        quit()



SG = SnakeGame()
while 1:
    SG.game_intro()
    
    

    
