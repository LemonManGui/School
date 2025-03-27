import tkinter
from tkinter import messagebox
import sqlite3 as SQL
import tkinter.messagebox
import bcrypt
import pygame
import random
import time


###
# Tkinter windows
###

def database_interaction():
    file_path = '/Users/gui/Desktop/RTDE/Login_program/User_info.db'
    conn = SQL.connect(file_path)
    cur = conn.cursor()
    
    get_usernames_query = '''SELECT Username FROM login_info'''
    
    usernames = []

    cur.execute(get_usernames_query)
    res = cur.fetchall()
    for tup in res:
        for string in tup:
            usernames.append(string)

    def login():
        username = user_name_entry.get()
        password = password_entry.get()
    
        if not username or not password:
            messagebox.showwarning(title='ERROR', message='Please enter username AND password')
            return
        
        check_password_query ='''
                        SELECT Password
                        FROM login_info
                        WHERE Username = ?;
                        '''
        cur.execute(check_password_query, (username,))
        res = cur.fetchone()
        
        if res:
            stored_hased_password = res[0]

            if bcrypt.checkpw(password.encode('utf-8'), stored_hased_password):
                messagebox.showinfo(title='CONGRATS', message='Username and Password are correct!')
                keuze_window()
            else:
                messagebox.showwarning(title='ERROR', message='Incorrect password')
        else:
            messagebox.showwarning(title='ERROR', message='User not found in database. Please try again or register')
    

    def register():
        username = user_name_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showwarning(title='ERROR', message='Please enter Username and Password')
            return
        
        cur.execute('SELECT Username FROM login_info WHERE Username = ?', (username,))
        if cur.fetchone():
            messagebox.showwarning(title='ERROR', message='This Username has already been taken')
        else:
            hased_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            register_query = '''
                            INSERT INTO Login_info (Username, Password)
                            VALUES (?, ?);
                            '''
            cur.execute(register_query, (username, hased_password))
            conn.commit()
            messagebox.showinfo(title='Account has been created', message=f'Your account has been created.\nUsername: {username}\nPassword: {len(password)*'*'}')


    window = tkinter.Tk()
    window.title('Login')

    # Open window in middel of screen:
    window_width = window.winfo_width()
    window_height = window.winfo_height() 
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f"+{x}+{y}")
    #

    frame = tkinter.Frame(window)
    frame.pack()

    user_info_frame = tkinter.LabelFrame(frame, text='User information')
    user_info_frame.grid(row=0, column=0, padx=20, pady=20)

    user_name_label = tkinter.Label(user_info_frame, text='Username:')
    user_name_entry = tkinter.Entry(user_info_frame)
    user_name_label.grid(row=0, column=0)
    user_name_entry.grid(row=1, column=0)

    password_label = tkinter.Label(user_info_frame, text='Password:')
    password_entry = tkinter.Entry(user_info_frame, show='*')
    password_label.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    option_window = tkinter.LabelFrame(frame)
    option_window.grid(row=1, column=0, padx=10)

    login_button = tkinter.Button(option_window, text='Login', command=login)
    register_button = tkinter.Button(option_window, text='Register', command=register)
    login_button.grid(row=2, column=0, padx=10, pady=10)
    register_button.grid(row=2, column=1, padx=10, pady=10)

    window.mainloop()

def keuze_window():
    window = tkinter.Tk()
    window.title('Choose a game')

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f"+{x}+{y}")

    frame = tkinter.Frame(window)
    frame.pack(padx=25, pady=25)


    pong_game_button = tkinter.Button(frame, text='Pong', command=pong_game)
    snake_game_button = tkinter.Button(frame, text='Snake', command=snake_game)
    chess_game_button = tkinter.Button(frame, text='Chess')

    pong_game_button.grid(row=1, column=0)
    snake_game_button.grid(row=1, column=1)
    chess_game_button.grid(row=1, column=2)


    window.mainloop()

###
# Games #
###

def pong_game():
    pygame.init()
    pygame.font.init()

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


def snake_game():
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

database_interaction()
