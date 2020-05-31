import pygame
from pygame import mixer
import random

pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("spc.jpg")

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
run = True

# player
playerImage = pygame.image.load("space-invaders (1).png")
playerX = 336
playerY = 500
changeX = 0
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 5
for i in range(num_enemies):
    enemyImage.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0, 734))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(3)
    enemyY_change.append(50)

bulletImage = pygame.image.load("bullet.png")
bulletX = playerX
bulletY = playerY + 10
bull_Y_change = -5

lives = 3
live = pygame.font.Font('freesansbold.ttf', 32)
liveX = 500
liveY = 10

score = 0

font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

line = pygame.font.Font('freesansbold.ttf', 100)
lineX = 0
lineY = 420

def show_line(x, y):
    lines = live.render("_____________________________________________", True, (255, 255, 0))
    screen.blit(lines, (x, y))


def show_lives(x, y):
    show = live.render("Lives: "+"Y " * lives, True, (255, 255, 255))
    screen.blit(show, (x, y))


def points(x, y):
    value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(value, (x, y))


over = pygame.font.Font('freesansbold.ttf', 64)
gameX = 180
gameY = 250


def game_over_text(x, y):
    game = over.render("|GAME OVER|", True, (255, 255, 255))
    screen.blit(game, (x, y))


def player(x, y):
    # to draw the player
    screen.blit(playerImage, (x, y))


def enemy(Image, x, y):
    # to draw the player
    screen.blit(Image, (x, y))


state = "ready"


def bullet(x, y):
    global state
    state = "fire"
    screen.blit(bulletImage, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) ** 0.5
    if distance < 54:
        return True
    else:
        return False


while run:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                changeX = -5
            elif event.key == pygame.K_RIGHT:
                changeX = 5
            elif event.key == pygame.K_SPACE:
                if state == "ready":
                    bullSound = mixer.Sound('laser.wav')
                    bullSound.play()
                    bulletX = playerX + 28
                    bullet(bulletX, bulletY)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                changeX = 0

    playerX += changeX
    for i in range(num_enemies):
        if lives == 0:
            for k in range(num_enemies):
                enemyY[k] = 2000
            game_over_text(gameX, gameY)
            break
        enemy(enemyImage[i], enemyX[i], enemyY[i])
        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 734:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] < 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        if enemyY[i] > 400:
            enemyX[i] = random.randint(0, 734)
            enemyY[i] = random.randint(0, 100)
            lives -= 1

        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            collision = mixer.Sound('explosion.wav')
            collision.play()
            bulletY = playerY + 10
            state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 734)
            enemyY[i] = random.randint(0, 100)

    if playerX > 734:
        playerX = 734
    elif playerX < 0:
        playerX = 0

    if state is "fire":
        bullet(bulletX, bulletY)
        bulletY += bull_Y_change

    if bulletY == 0:
        state = "ready"
        bulletY = playerY + 10

    player(playerX, playerY)
    # updates every time
    points(textX, textY)
    show_lives(liveX, liveY)
    show_line(lineX, lineY)
    pygame.display.update()
