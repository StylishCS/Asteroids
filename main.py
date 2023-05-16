import pygame, sys
from button import Button
from subprocess import call
import sqlite3
from win32api import GetSystemMetrics
from pyvidplayer import Video
import time
import datetime
#############################
conn = sqlite3.connect('database.db')

c = conn.cursor()

'''c.execute("""CREATE TABLE scores (
    HIGHSCORE integer
        )
""")'''
##############################
pygame.init()

sw = GetSystemMetrics(0)
sh = GetSystemMetrics(1)

SCREEN = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Menu")

BG = pygame.image.load("asteroidsPics/starbgfull.png")

windSound = pygame.mixer.Sound('sounds/background sound.mp3')

windSound.set_volume(.5)


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("Asteroids", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(sw//2, 300))

        SINGLE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(sw//2, 450),
                             text_input="SINGLE PLAYER", font=get_font(26), base_color="#d7fcd4", hovering_color="White")
        MULTI_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(sw//2, 600),
                                text_input="MULTIPLAYER", font=get_font(26), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(sw//2, 750),
                             text_input="QUIT", font=get_font(26), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [SINGLE_BUTTON, MULTI_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SINGLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    call(['python', 'single player.py'])

                if MULTI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    call(['python', 'multiplayer.py'])

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()


        pygame.display.update()


vid = Video('assets/intro muted.mp4')

vid.set_size((sw,sh))

endTime = datetime.datetime.now() + datetime.timedelta(milliseconds=9000)

def intro(endTime):
    while True:
        vid.draw(SCREEN, (0,0))
        font = pygame.font.SysFont('arial', 30)
        intro_continue = font.render('Press Mouse Button to Continue...' , 1, (255, 255, 255))
        SCREEN.blit(intro_continue, (25, sh-80))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or datetime.datetime.now() >= endTime:
                vid.close()
                main_menu()





windSound.play(-1)
intro(endTime)




