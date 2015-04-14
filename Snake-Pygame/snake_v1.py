import pygame
import time
import random

pygame.init()

##VARIABLES-----------------------

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height)) 
pygame.display.set_caption('Snake 168')




clock = pygame.time.Clock()
block_size = 15
AppleThickness = 20
FPS = 30

direction = 'right'

smallfont = pygame.font.SysFont("comicsansms",25)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",80)

###VARIABLES------------------------



###IMAGES---------------------------
snake_head = pygame.image.load('snakehead.png')
apple = pygame.image.load('apple.png')
###IMAGES---------------------------

#---ICON---
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)
#---ICON---







###FUNCTIONS------------------------

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

def message_to_screen(msg,color,y_displace = 0, size = 'small'):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf,textRect)
    

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
        pygame.draw.rect(gameDisplay, green,[XnY[0],XnY[1],block_size,block_size])

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        
        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake",
                          green,
                          -100,
                          'large')

        message_to_screen("The objective of the game is to eat the red apples",
                          black,
                          -30)
        
        message_to_screen("The more apples you eat, the longer you get",
                          black,
                          10)
        
        message_to_screen("If you run into yourself, or the edges, you die!",
                          black,
                          50)

        message_to_screen("Press P to play or Q to quit",
                          black,
                          180)

        

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
    #randAppleX = round(random.randrange(0,display_width - AppleThickness))#/10.0) * 10.0
    #randAppleY = round(random.randrange(0,display_height - AppleThickness))#/10.0) * 10.0
    
    while gameExit == False:

        while gameOver == True:
            direction = 'right'
            gameDisplay.fill(white)
            message_to_screen("Game over",
                              red,
                              -50,
                              size = 'large')
            
            message_to_screen("Press P to play again or Q to quit",
                              black,
                              50,
                              size = 'medium')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_p:
                        gameLoop()
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change =  -block_size
                    lead_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    lead_y_change =  -block_size
                    lead_x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = 'down'
                    
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
            
           
              
                    
        lead_x += lead_x_change
        lead_y += lead_y_change
       
                
        gameDisplay.fill(white)

        
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
        
        pygame.display.update()



        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1
            
            
        clock.tick(FPS)
    
    pygame.quit() 
    quit()

###GAME LOOP-------------------------

###MAIN------------------------------
game_intro()        
gameLoop()
###---------------------------------- 


