import pygame

pygame.init() #initializes pygame

gameDisplay = pygame.display.set_mode((800,600)) #creates a surface
pygame.display.set_caption('Snake 168') #title

pygame.display.update() #updates entire surface or parameter
# pygame.display.flip() updates entire screen at once

gameExit = False;

while not gameExit:
    for event in pygame.event.get():
        print(event)


pygame.quit() #exits pygame
quit() #exits python
