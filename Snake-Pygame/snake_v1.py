import pygame

pygame.init()

##VARIABLES-----------------------

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((800,600)) 
pygame.display.set_caption('Snake 168') 

gameExit = False;

lead_x = 300
lead_y = 300
lead_x_change = 0
lead_y_change = 0

clock = pygame.time.Clock()
###VARIABLES------------------------



###GAME LOOP------------------------
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change =  -10
            if event.key == pygame.K_RIGHT:
                lead_x_change = 10
          
                
    lead_x += lead_x_change
   
            
    gameDisplay.fill(white)     
    pygame.draw.rect(gameDisplay, black,[lead_x,lead_y,10,10])
    
    
    pygame.display.update()
    clock.tick(15)

###GAME LOOP-------------------------
        


pygame.quit() 
quit() 
