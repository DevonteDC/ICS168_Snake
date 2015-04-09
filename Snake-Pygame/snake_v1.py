import pygame

pygame.init() #initializes pygame

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((800,600)) #creates a surface
pygame.display.set_caption('Snake 168') #title

# pygame.display.update() updates entire surface or parameter
# pygame.display.flip() updates entire screen at once

gameExit = False;

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
            
    gameDisplay.fill(white)      #fill background with white
    pygame.draw.rect(gameDisplay, black,[400,300,10,100]) #creates rectangles
    pygame.draw.rect(gameDisplay, red,[400,300,10,10])
    gameDisplay.fill(red,rect=[200,200,50,50])

    
    pygame.display.update()
        #print(event) shows all the events that are occuring


pygame.quit() #exits pygame
quit() #exits python
