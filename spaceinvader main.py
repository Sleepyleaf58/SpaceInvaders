import pygame
import random
import math

# Initializes the code
pygame.init()

# Create the window
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load("background.png")

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 368
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load("ghost.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change = 3
enemyY_change = 40

# Bullet
# Ready state means that you cannot see the bullet on the screen
# Fire state means that the bullet is moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 11
bullet_state = "ready"

# Score
score = 0

# Player Function
def player(x,y):
    screen.blit(playerImg, (x, y))

# Enemy Function
def enemy(x,y):
    screen.blit(enemyImg, (x, y))

# Fire Bullet Function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Collision Detection
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:
    # background colour RGB
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background,(0, 0))

    for event in pygame.event.get():
        # Closes window
        if event.type == pygame.QUIT:
            running = False

        # Key Down
        keypressed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = +5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    fire_bullet(playerX, bulletY)
                    bulletX = playerX

        #Key Up 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    # player boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    # enemy movement
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 3
        enemyY += enemyY_change
    if enemyX >= 736:
        enemyX_change = -3
        enemyY += enemyY_change

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    # Calling image functions
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    # Update display
    pygame.display.update()