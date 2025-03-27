import pygame
import time
import random

# Initialiseer pygame
pygame.init()

# Kleuren
wit = (255, 255, 255)
zwart = (0, 0, 0)
rood = (213, 50, 80)
groen = (0, 255, 0)
blauw = (50, 153, 213)

# Scherminstellingen
breedte = 800
hoogte = 600
scherm = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption("Snake Game")

# Snake instellingen
snake_blok = 10
snake_snelheid = 15


# Lettertype
lettertype = pygame.font.SysFont("bahnschrift", 25)

def jouw_score(score):
    waarde = lettertype.render(f"Score: {score}", True, blauw)
    scherm.blit(waarde, [0, 0])

def onze_snake(snake_blok, snake_lijst):
    for blok in snake_lijst:
        pygame.draw.rect(scherm, groen, [blok[0], blok[1], snake_blok, snake_blok])

def game():
    game_over = False
    game_af = False

    x1 = breedte // 2
    y1 = hoogte // 2

    x1_verandering = 0
    y1_verandering = 0

    snake_lijst = []
    lengte_snake = 1

    # Voedsel
    voedsel_x = round(random.randrange(0, breedte - snake_blok) / 10.0) * 10.0
    voedsel_y = round(random.randrange(0, hoogte - snake_blok) / 10.0) * 10.0

    klok = pygame.time.Clock()

    while not game_over:

        while game_af:
            scherm.fill(zwart)
            bericht = lettertype.render("Game Over! Druk op Q om te stoppen of C om opnieuw te spelen", True, rood)
            scherm.blit(bericht, [breedte // 6, hoogte // 3])
            jouw_score(lengte_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_af = False
                    if event.key == pygame.K_c:
                        game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_verandering = -snake_blok
                    y1_verandering = 0
                elif event.key == pygame.K_RIGHT:
                    x1_verandering = snake_blok
                    y1_verandering = 0
                elif event.key == pygame.K_UP:
                    y1_verandering = -snake_blok
                    x1_verandering = 0
                elif event.key == pygame.K_DOWN:
                    y1_verandering = snake_blok
                    x1_verandering = 0

        if x1 >= breedte or x1 < 0 or y1 >= hoogte or y1 < 0:
            game_af = True

        x1 += x1_verandering
        y1 += y1_verandering
        scherm.fill(zwart)
        pygame.draw.rect(scherm, rood, [voedsel_x, voedsel_y, snake_blok, snake_blok])
        snake_hoofd = [x1, y1]
        snake_lijst.append(snake_hoofd)

        if len(snake_lijst) > lengte_snake:
            del snake_lijst[0]

        for blok in snake_lijst[:-1]:
            if blok == snake_hoofd:
                game_af = True

        onze_snake(snake_blok, snake_lijst)
        jouw_score(lengte_snake - 1)
        pygame.display.update()

        if x1 == voedsel_x and y1 == voedsel_y:
            voedsel_x = round(random.randrange(0, breedte - snake_blok) / 10.0) * 10.0
            voedsel_y = round(random.randrange(0, hoogte - snake_blok) / 10.0) * 10.0
            lengte_snake += 1

        klok.tick(snake_snelheid)

    pygame.quit()
    quit()

game()
