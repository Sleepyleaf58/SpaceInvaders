import pygame
from pygame import mixer

import random
import math

# Initializes the code
pygame.init()

# Create the window
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 368
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ghost.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet

# Ready state means that you cannot see the bullet on the screen
# Fire state means that the bullet is moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 11
bullet_state = "ready"

# Home Planet
home_planetImg = pygame.image.load("HomePlanet.png")

#Replay

replayImg = pygame.image.load("replay.png")
game_state = "ready"

# Score Font
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# High Score Font
high_score_value = 0
high_score_font = pygame.font.Font("freesansbold.ttf", 32)

# Game Over Text Font
over_font = pygame.font.Font("freesansbold.ttf", 64)

# Show Score Function
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# High Score Function
def show_high_score():
    high_score = high_score_font.render("High Score: " + str(high_score_value), True, (255, 255, 255))
    screen.blit(high_score, (560, 10))

# Game Over Function
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 220))
    play_again_text = font.render("Play Again", True, (255, 255, 255))
    screen.blit(play_again_text, (310, 310))
    screen.blit(replayImg, (368, 380))

# Player Function
def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy Function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

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
    screen.blit(home_planetImg, (0, 480))

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

            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = +5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.set_volume(0.2)
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        #Key Up 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

        #Play Again
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if 432 >= mouseX >= 368 and 444 >= mouseY >= 380:
                if game_state == "gameover":
                    game_state = "ready"
                    for i in range(num_of_enemies):
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(50, 150)
                        score_value = 0


    # player boundaries
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    if playerY >= 532:
        playerY = 532

    # enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_state = "gameover"

            if game_state == "gameover":
                game_over_text()
            

        #enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.set_volume(0.1)
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            if score_value > high_score_value:
                high_score_value = score_value
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Calling image functions
        enemy(enemyX[i], enemyY[i], i)


    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_high_score()

    # Update display
    pygame.display.update()