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
block_size = 10
FPS = 30

direction = 'right'

font = pygame.font.SysFont(None,25)

###VARIABLES------------------------



###IMAGES---------------------------
snake_head = pygame.image.load('snakehead.png')
###IMAGES---------------------------







###FUNCTIONS------------------------
def text_objects(text,color):
    textSurface = font.render(text,True,color)
    return textSurface, textSurface.get_rect()
def message_to_screen(msg,color):
    textSurf, textRect = text_objects(msg,color)
    textRect.center = (display_width / 2), (display_height / 2)
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

    randAppleX = round(random.randrange(0,display_width - block_size))#/10.0) * 10.0
    randAppleY = round(random.randrange(0,display_height - block_size))#/10.0) * 10.0
    
    while gameExit == False:

        while gameOver == True:
            direction = 'right'
            gameDisplay.fill(white)
            message_to_screen("Game over, press C to play again or Q to quit",red)
            pygame.display.update()

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

        AppleThickness = 30
        pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,AppleThickness,AppleThickness])

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
                randAppleX = round(random.randrange(0,display_width - block_size)/10.0) * 10.0
                randAppleY = round(random.randrange(0,display_height - block_size)/10.0) * 10.0
                snakeLength += 1
            
            
        clock.tick(FPS)
    
    pygame.quit() 
    quit()

###GAME LOOP-------------------------

###MAIN------------------------------
        
gameLoop()
###---------------------------------- 


