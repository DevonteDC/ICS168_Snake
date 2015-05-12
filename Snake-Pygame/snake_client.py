import pygame
import time
import random
import inputbox
import sqlite3
import socket
import ipgetter
import hashlib
local = "127.0.0.1"
external = str(ipgetter.myip())


pygame.init()

host = local
port = 10001

server = (local,20000)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))




##VARIABLES-----------------------

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red = (255,0,0)
green = (0,155,0)
light_green = (0,255,0)
yellow = (200,200,0)
light_yellow = (255,255,0)

###USERS
username =""
###USERS
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height)) 
pygame.display.set_caption('Snake 168')






clock = pygame.time.Clock()
block_size = 20
AppleThickness = 30
FPS = 20

direction = 'right'

smallfont = pygame.font.SysFont("comicsansms",25)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",80)

###VARIABLES------------------------



###IMAGES---------------------------
snake_head = pygame.image.load('snakehead.png')
apple = pygame.image.load('apple.png')
background = pygame.image.load('SnakeBackground.png')
titleScreen = pygame.image.load('SnakeTitle.png')
###IMAGES---------------------------

#SOUND----------
titleMusic = pygame.mixer.Sound('pac.wav')
eatSound = pygame.mixer.Sound('eat.wav')
#SOUND----------

#---ICON---
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)
#---ICON---

#---DATABASE VARIABLES---
con = sqlite3.connect('snaketest.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Login (Username TEXT, Password TEXT)")
con.commit()

#---DATABASE VARIABLES---







###FUNCTIONS------------------------

def pause():
    paused = True

    message_to_screen("Paused",
                      black,
                      -100,
                      'large')
    message_to_screen("Press C to continue or Q to quit.",
                      black,
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
       
        
        clock.tick(5)

def score(score):
    text = smallfont.render("Score: " + str(score),True,black)
    gameDisplay.blit(text,[0,0])

def displayUsername():
    global username
    text = smallfont.render("Username: " + username,True,black)
    gameDisplay.blit(text,[200,0])

def randAppleGen():
    randAppleX = round(random.randrange(0,display_width - AppleThickness))#/10.0) * 10.0
    randAppleY = round(random.randrange(0,display_height - AppleThickness))#/10.0) * 10.0
    return randAppleX, randAppleY

    
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text,True,color)
    elif size == "medium":
        textSurface = medfont.render(text,True,color)
    elif size == "large":
        textSurface = largefont.render(text,True,color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight,size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (buttonx + (buttonwidth/2), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf,textRect)

def message_to_screen(msg,color,y_displace = 0, size = 'small'):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf,textRect)

def game_controls():
    gcont = True

    while gcont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                s.close()
                pygame.quit()
                quit()
            

        
        gameDisplay.blit(background,(0,0))
        message_to_screen("Controls",
                          green,
                          -100,
                          'large')

        message_to_screen("WASD Movement",
                          black,
                          -30)
        
        message_to_screen("Pause: P",
                          black,
                          10)
        
        


        

        button("Play",150,500,100,50,green,light_green, action = 'Play')
        #button("Main",350,500,100,50,yellow,light_yellow,action='main')
        button("Quit",550,500,100,50,red,light_red,action='Quit')

        

        pygame.display.update()
        clock.tick(15)
    

def button(text,x,y,width,height,inactive_color,active_color,action = None):
    #global titleMusic
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay,active_color,(x,y,width,height))
        if click[0] == 1 and action != None:
            if action == 'Quit':

                s.close()
                pygame.quit()
                quit()
            if action == 'Controls':
                game_controls()
                
            if action == 'Play' or action == 'Redo':
                titleMusic.stop()
                UserPass()
                

            
                

            
            
            
    else:
        pygame.draw.rect(gameDisplay,inactive_color,(x,y,width,height))

    text_to_button(text,black,x,y,width,height)


def InvalidPass():
    ipass = True

    while ipass:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                s.close()
                pygame.quit()
                quit()
            

        
        gameDisplay.blit(background,(0,0))

        message_to_screen("Invalid Password, Redo",
                          red,
                          -100,
                          'medium')
        button("Redo",150,500,100,50,green,light_green, action = 'Redo')

        pygame.display.update()
        clock.tick(15)
        
    

def UserPass():
    global username
    global cur
    global con
    global server
    userp = True
    noStartGame = True

    while userp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                s.close()
                pygame.quit()
                quit()
            

        
        gameDisplay.blit(background,(0,0))
      
        ##SERVER LOGIN##
        username = inputbox.ask(gameDisplay,"UserName")
        password = inputbox.ask(gameDisplay,"Password")
        password = hashlib.md5(password.encode()).hexdigest()
        print("PASSWORD BEFORE SENDING: ",password," TYPE: ",type(password))
        s.sendto("Login:{}:{}".format(username,password).encode(),server)
        while noStartGame == True:
            data, addr = s.recvfrom(1024)
            data = data.decode()
            data = data.split(":")
            if data[0] == "Gameloop":
                gameLoop()
            elif data[0] == "Invalidpass":
                InvalidPass()
        ##SERVER LOGIN##
        
                
                
            
        
        


        


        

        pygame.display.update()
        clock.tick(15)

def snake(block_size,snakeList):

    if direction == 'right':
        head = pygame.transform.rotate(snake_head,270)
    if direction == 'left':
        head = pygame.transform.rotate(snake_head,90)
    if direction == 'up':
        head = snake_head
    if direction == 'down':
        head = pygame.transform.rotate(snake_head,180)
        
    gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, black,[XnY[0],XnY[1],block_size,block_size])
        pygame.draw.rect(gameDisplay,green,[XnY[0],XnY[1],block_size - 1,block_size - 1])

def game_intro():

    intro = True

    
    titleMusic.play()
    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                s.close()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                    
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.blit(titleScreen,(0,0))
        #gameDisplay.fill(white)
        


        #message_to_screen("Press C to play, P to pause, or Q to quit",
                          #black,
                          #180)
        

        button("play",500,120,100,50,green,light_green, action = 'Play')
        button("controls",500,190,100,50,yellow,light_yellow,action='Controls')
        button("quit",500,260,100,50,red,light_red,action='Quit')

        

        pygame.display.update()
        clock.tick(15)
    
###FUNCTIONS------------------------







###GAME LOOP------------------------
def gameLoop():

    
    global direction
    gameExit = False
    gameOver = False
    lead_x = display_width/2
    lead_y = display_height/2
   
        
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX,randAppleY = randAppleGen()
    
    
    while gameExit == False:

    

        

        if gameOver == True:
            message_to_screen("Game over",
                              red,
                              -50,
                              size = 'large')
            
            message_to_screen("Press C to play again or Q to quit",
                              black,
                              50,
                              size = 'medium')
            pygame.display.update()
            

        while gameOver == True:
            direction = 'right'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'right':
                    lead_x_change =  -block_size
                    lead_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP and direction !='down':
                    lead_y_change =  -block_size
                    lead_x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction !='up':
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = 'down'

                elif event.key ==  pygame.K_p:
                    pause()
                    
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
            
           
              
                    
        lead_x += lead_x_change
        lead_y += lead_y_change
       
                
        gameDisplay.blit(background,(0,0))

        
        #pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,AppleThickness,AppleThickness])
        gameDisplay.blit(apple,(randAppleX,randAppleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]
        
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
            
        snake(block_size,snakeList)
        score(snakeLength - 1)
        displayUsername()
        
        
        pygame.display.update()



        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                eatSound.play()
                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1
                
            
            
        clock.tick(FPS)
    s.close()
    pygame.quit() 
    quit()

###GAME LOOP-------------------------

###MAIN------------------------------
game_intro()        

###---------------------------------- 


