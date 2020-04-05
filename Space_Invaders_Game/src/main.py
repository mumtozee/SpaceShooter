import pygame
import classes
import os
from pygame import mixer

pygame.init()
resource_path = os.path.join(os.getcwd(), os.path.dirname(__file__), '..\\res\\')

# setting up the game window
screen = pygame.display.set_mode((800, 600))

# Background
bg_img = pygame.image.load(resource_path + 'background.jpg')

# Background Music
mixer.music.load(resource_path + 'bg_music.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders 1.0")
icon = pygame.image.load(resource_path + 'ufo_icon.png')
pygame.display.set_icon(icon)

# Player
player = classes.PlayerCreator.create(classes.PlayerCreator())

# Enemy
enemy_list = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemy_list.append(classes.EnemyCreator.create(classes.EnemyCreator()))

# Score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
gameover_font = pygame.font.Font('freesansbold.ttf', 64)


def show_gameover():
    gameover_text = gameover_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(gameover_text, (200, 250))


def show_score(x, y):
    score = font.render('Score: ' + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Loop
running = True
while running:
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.x_change = 2
            if event.key == pygame.K_LEFT:
                player.x_change = -2
            if event.key == pygame.K_SPACE:
                if player.bullet_state == 'ready':
                    bullet_sound = mixer.Sound(resource_path + 'shot.wav')
                    bullet_sound.play()
                    player.bullet.X = player.X
                    player.fire(player.bullet.X, player.bullet.Y, screen)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.x_change = 0

    # Enemy movement
    for i in range(number_of_enemies):
        # GameOver: if enemies get under the line of the player or all dead
        if enemy_list[i].Y >= 440:
            for tmp_enemy in enemy_list:
                tmp_enemy.Y = 2000
            show_gameover()
            break

        enemy_list[i].draw(enemy_list[i].X, enemy_list[i].Y, screen)
        enemy_list[i].move()

        # Collision
        collision = enemy_list[i].collide(player.bullet)
        if collision:
            explosion_sound = mixer.Sound(resource_path + 'explosion.wav')
            explosion_sound.play()
            player.bullet.Y = 480
            player.bullet_state = 'ready'
            score_val += 1
            number_of_enemies -= 1
            del enemy_list[i]
            break

    if number_of_enemies == 0:
        show_gameover()

    # Bullet movement
    if player.bullet.Y <= 0:
        player.bullet.Y = 480
        player.bullet_state = 'ready'

    if player.bullet_state == 'fire':
        player.fire(player.bullet.X, player.bullet.Y, screen)
        player.bullet.Y -= player.bullet.y_change

    player.move()
    player.draw(player.X, player.Y, screen)
    show_score(textX, textY)
    pygame.display.update()
