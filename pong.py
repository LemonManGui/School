import pygame
import random

# Initialiseer pygame
pygame.init()

# Kleuren
zwart = (0, 0, 0)
wit = (255, 255, 255)

# Scherminstellingen
breedte = 800
hoogte = 600
scherm = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption("Pong Game")

# Snelheid
klok = pygame.time.Clock()
fps = 60

# Paddle-instellingen
paddle_breedte = 10
paddle_hoogte = 100
snelheid_paddle = 10

# Bal-instellingen
bal_diameter = 20
bal_snelheid_x = random.choice([-4, 4])
bal_snelheid_y = random.choice([-4, 4])

# Paddles en bal startposities
paddle1_y = (hoogte - paddle_hoogte) // 2
paddle2_y = (hoogte - paddle_hoogte) // 2
bal_x = breedte // 2
bal_y = hoogte // 2

# Scores
score1 = 0
score2 = 0

# Lettertype
lettertype = pygame.font.SysFont("bahnschrift", 35)


def toon_score():
    score_text = lettertype.render(f"{score1} - {score2}", True, wit)
    scherm.blit(score_text, [breedte // 2 - 50, 20])


# Het hoofdprogramma
def game():
    global paddle1_y, paddle2_y, bal_x, bal_y, bal_snelheid_x, bal_snelheid_y, score1, score2

    running = True
    while running:
        # Event-afhandeling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Toetsen voor paddle-beweging
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= snelheid_paddle
        if keys[pygame.K_s] and paddle1_y < hoogte - paddle_hoogte:
            paddle1_y += snelheid_paddle
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= snelheid_paddle
        if keys[pygame.K_DOWN] and paddle2_y < hoogte - paddle_hoogte:
            paddle2_y += snelheid_paddle

        # Beweging van de bal
        bal_x += bal_snelheid_x
        bal_y += bal_snelheid_y

        # Bal tegen de boven- of onderkant
        if bal_y <= 0 or bal_y >= hoogte - bal_diameter:
            bal_snelheid_y *= -1

        # Bal raakt paddle 1
        if (
            bal_x <= paddle_breedte
            and paddle1_y < bal_y < paddle1_y + paddle_hoogte
        ):
            bal_snelheid_x *= -1

        # Bal raakt paddle 2
        if (
            bal_x >= breedte - paddle_breedte - bal_diameter
            and paddle2_y < bal_y < paddle2_y + paddle_hoogte
        ):
            bal_snelheid_x *= -1

        # Scoor en reset bal
        if bal_x <= 0:
            score2 += 1
            bal_x = breedte // 2
            bal_y = hoogte // 2
            bal_snelheid_x = random.choice([-4, 4])
            bal_snelheid_y = random.choice([-4, 4])

        if bal_x >= breedte - bal_diameter:
            score1 += 1
            bal_x = breedte // 2
            bal_y = hoogte // 2
            bal_snelheid_x = random.choice([-4, 4])
            bal_snelheid_y = random.choice([-4, 4])

        # Scherm bijwerken
        scherm.fill(zwart)
        pygame.draw.rect(scherm, wit, [0, paddle1_y, paddle_breedte, paddle_hoogte])
        pygame.draw.rect(
            scherm,
            wit,
            [breedte - paddle_breedte, paddle2_y, paddle_breedte, paddle_hoogte],
        )
        pygame.draw.ellipse(scherm, wit, [bal_x, bal_y, bal_diameter, bal_diameter])
        pygame.draw.line(scherm, wit, [breedte // 2, 0], [breedte // 2, hoogte], 2)
        toon_score()

        pygame.display.update()
        klok.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    game()
