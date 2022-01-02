import pygame

#Initializes the code
pygame.init()

#Create the window
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("")
pygame.display.set_icon(icon)

#Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False