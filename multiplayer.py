import math
import random
import pygame
import sqlite3
from win32api import GetSystemMetrics
import time

pygame.init()

#############################
conn = sqlite3.connect('database_multiplayer.db')

c = conn.cursor()

'''c.execute("""CREATE TABLE scores (
    HIGHSCORE integer
        )
""")'''



##############################

sw = GetSystemMetrics(0)
sh = GetSystemMetrics(1)

win = pygame.display.set_mode((sw,sh))

bg = pygame.image.load('asteroidsPics/starbgfull.png')
alienImg = pygame.image.load('asteroidsPics/alienShip.png')
playerRocket = pygame.image.load('asteroidsPics/spaceRocket.png')
playerRocket2 = pygame.image.load('asteroidsPics/spaceRocket2.png')
star = pygame.image.load('asteroidsPics/star.png')
asteroid50 = pygame.image.load('asteroidsPics/asteroid50.png')
asteroid100 = pygame.image.load('asteroidsPics/asteroid100.png')
asteroid150 = pygame.image.load('asteroidsPics/asteroid150.png')
muted = pygame.image.load('asteroidsPics/muted.png')

shoot = pygame.mixer.Sound('sounds/shoot.wav')
bangSmallSound = pygame.mixer.Sound('sounds/bangSmall.wav')
bangLargeSound = pygame.mixer.Sound('sounds/bangLarge.wav')
gameoverSound = pygame.mixer.Sound('sounds/gameover.mp3')
rocketEngine = pygame.mixer.Sound('sounds/rocket engine.mp3')
#windSound = pygame.mixer.Sound('sounds/background sound.mp3')
alienSound = pygame.mixer.Sound('sounds/Alien Sound.mp3')

shoot.set_volume(.25)
bangLargeSound.set_volume(.25)
bangSmallSound.set_volume(.25)
#windSound.set_volume(.25)

pygame.display.set_caption('Asteroids')

clock = pygame.time.Clock()

c.execute("""SELECT MAX(HIGHSCORE) FROM scores""")
recordd = c.fetchall()
highScore = int(recordd[0][0])

print(highScore)

class Player(object):
    def __init__(self):
        self.img = playerRocket
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2
        self.y = sh//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x,self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def draw(self, win):
        #win.blit(self.img, [self.x, self.y, self.w, self.h])
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def moveForward(self):
        self.x += self.cosine*6
        self.y -= self.sine*6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def updateLocation(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0


class Player2(object):
    def __init__(self):
        self.img = playerRocket2
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2
        self.y = sh//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head2 = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def draw(self, win):
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head2 = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head2 = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def moveForward(self):
        self.x += self.cosine*6
        self.y -= self.sine*6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head2 = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def updateLocation(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0


class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self,win):
        pygame.draw.rect(win, ('white'), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x <-50 or self.x > sw or self.y > sh or self.y < -50:
            return True

class Bullet2(object):
    def __init__(self):
        self.point = player2.head2
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player2.cosine
        self.s = player2.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self,win):
        pygame.draw.rect(win, ('white'), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x <-50 or self.x > sw or self.y > sh or self.y < -50:
            return True

class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid50
        elif self.rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

class Star(object):
    def __init__(self):
        self.img = star
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0,sw-self.w), random.choice([-1*self.h-5, sh+5])),(random.choice([-1*self.w-5, sw+5]), random.randrange(0, sh-self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self,win):
        win.blit(self.img, (self.x, self.y))


class Alien(object):
    def __init__(self):
        self.img = alienImg
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self,win):
        win.blit(self.img, (self.x, self.y))

class AlienBullet(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 4
        self.dx, self.dy = player.x - self.x, player.y - self.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.dist, self.dy / self.dist
        self.xv = self.dx * 5
        self.yv = self.dy * 5

    def draw(self,win):
        pygame.draw.rect(win, 'white', [self.x, self.y, self.w, self.h])

class Alien2(object):
    def __init__(self):
        self.img = alienImg
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self,win):
        win.blit(self.img, (self.x, self.y))

class AlienBullet2(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 4
        self.dx, self.dy = player2.x - self.x, player2.y - self.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.dist, self.dy / self.dist
        self.xv = self.dx * 5
        self.yv = self.dy * 5

    def draw(self,win):
        pygame.draw.rect(win, 'white', [self.x, self.y, self.w, self.h])


def redrawGameWindow():
    win.blit(bg, (0,0))
    font = pygame.font.SysFont('arial', 30)
    livesText = font.render('Lives: ' + str(lives), 1, ('white'))
    playAgainText = font.render('Press TAB to Play Again', 1, 'white')
    scoreText = font.render('Score: ' + str(score), 1, 'white')
    highScoreText = font.render('High Score: ' + str(highScore), 1, 'white')
    if not isSoundOn:
        win.blit(muted, (25,750))

    player2.draw(win)
    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)
    for b2 in playerBullets2:
        b2.draw(win)
    for s in stars:
        s.draw(win)
    for a in aliens:
        a.draw(win)
    for b in alienBullets:
        b.draw(win)
    for a in aliens2:
        a.draw(win)
    for b in alienBullets2:
        b.draw(win)

    if rapidFire:
        pygame.draw.rect(win, 'black', [sw//2-51, 19, 102, 22])
        pygame.draw.rect(win, 'white', [sw//2-50, 20, 100 - 100*(count - rfStart)/500, 20])

    if rapidFire2:
        pygame.draw.rect(win, 'black', [sw//2-51, 19, 102, 22])
        pygame.draw.rect(win, 'white', [sw//2-50, 20, 100 - 100*(count - rfStart2)/500, 20])

    if gameover:
        win.blit(playAgainText, (sw//2-playAgainText.get_width()//2, sh//2-playAgainText.get_height()//2))
    win.blit(scoreText, (sw-scoreText.get_width()-25, 25))
    win.blit(livesText, (25,25))
    win.blit(highScoreText, (sw - highScoreText.get_width()-25, 35 + scoreText.get_height()))
    pygame.display.update()



player = Player()
playerBullets = []
player2 = Player2()
playerBullets2 = []
asteroids = []
count = 0
stars = []
aliens = []
alienBullets = []
aliens2 = []
alienBullets2 = []
rocketEngine.play()


run = True
gameover = False
lives = 4
score = 0
rapidFire = False
rfStart = -1
rapidFire2 = False
rfStart2 = -1
isSoundOn = True




#windSound.play(-1)


while run:
    clock.tick(60)

    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(ran))
        if count % 1000 == 0:
            stars.append(Star())
        if count % 750 == 0:
            aliens.append(Alien())
        if count % 1500 == 0:
            aliens2.append(Alien2())


        for i, a in enumerate(aliens):
            a.x += a.xv
            a.y += a.yv
            if a.x > sw + 150 or a.x + a.w < -100 or a.y > sh + 150 or a.y + a.h < -100:
                aliens.pop(i)
            if count % 60 == 0:
                if isSoundOn:
                    alienSound.play()
                alienBullets.append(AlienBullet(a.x+a.w//2, a.y+a.h//2))
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        aliens.pop(i)
                        if isSoundOn:
                            bangLargeSound.play()
                        score += 50
                        lives += 1
                        break

            for b in playerBullets2:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        aliens.pop(i)
                        if isSoundOn:
                            bangLargeSound.play()
                        score += 50
                        lives += 1
                        break


        for i, a in enumerate(aliens2):
            a.x += a.xv
            a.y += a.yv
            if a.x > sw + 150 or a.x + a.w < -100 or a.y > sh + 150 or a.y + a.h < -100:
                aliens2.pop(i)
            if count % 60 == 0:
                if isSoundOn:
                    alienSound.play()
                alienBullets2.append(AlienBullet2(a.x+a.w//2, a.y+a.h//2))

            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        aliens2.pop(i)
                        if isSoundOn:
                            bangLargeSound.play()
                        score += 50
                        lives += 1
                        break

            for b in playerBullets2:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        aliens2.pop(i)
                        if isSoundOn:
                            bangLargeSound.play()
                        score += 50
                        lives += 1
                        break


        for i, b in enumerate(alienBullets):
            b.x += b.xv
            b.y += b.yv
            if (b.x >= player.x - player.w//2 and b.x <= player.x + player.w//2) or b.x + b.w >= player.x - player.w//2 and b.x + b.w <= player.x + player.w//2:
                if (b.y >= player.y - player.h//2 and b.y <= player.y + player.h//2) or b.y + b.h >= player.y - player.h//2 and b.y + b.h <= player.y + player.h//2:
                    lives -= 1
                    alienBullets.pop(i)
                    break
            if (b.x >= player2.x - player2.w//2 and b.x <= player2.x + player2.w//2) or b.x + b.w >= player2.x - player2.w//2 and b.x + b.w <= player2.x + player2.w//2:
                if (b.y >= player2.y - player2.h//2 and b.y <= player2.y + player2.h//2) or b.y + b.h >= player2.y - player2.h//2 and b.y + b.h <= player2.y + player2.h//2:
                    lives -= 1
                    alienBullets.pop(i)
                    break

        for i, b in enumerate(alienBullets2):
            b.x += b.xv
            b.y += b.yv
            if (b.x >= player.x - player.w//2 and b.x <= player.x + player.w//2) or b.x + b.w >= player.x - player.w//2 and b.x + b.w <= player.x + player.w//2:
                if (b.y >= player.y - player.h//2 and b.y <= player.y + player.h//2) or b.y + b.h >= player.y - player.h//2 and b.y + b.h <= player.y + player.h//2:
                    lives -= 1
                    alienBullets2.pop(i)
                    break
            if (b.x >= player2.x - player2.w//2 and b.x <= player2.x + player2.w//2) or b.x + b.w >= player2.x - player2.w//2 and b.x + b.w <= player2.x + player2.w//2:
                if (b.y >= player2.y - player2.h//2 and b.y <= player2.y + player2.h//2) or b.y + b.h >= player2.y - player2.h//2 and b.y + b.h <= player2.y + player2.h//2:
                    lives -= 1
                    alienBullets2.pop(i)
                    break

        player.updateLocation()
        player2.updateLocation()
        for b in playerBullets:
            b.move()
            if b.checkOffScreen():
                playerBullets.pop(playerBullets.index(b))
        for b2 in playerBullets2:
            b2.move()
            if b2.checkOffScreen():
                playerBullets2.pop(playerBullets2.index(b2))

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (a.x >= player.x-player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if (a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y + a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    if isSoundOn:
                        bangLargeSound.play()
                    break

            if (a.x >= player2.x-player2.w//2 and a.x <= player2.x + player2.w//2) or (a.x + a.w <= player2.x + player2.w//2 and a.x + a.w >= player2.x - player2.w//2):
                if (a.y >= player2.y - player2.h//2 and a.y <= player2.y + player2.h//2) or (a.y + a.h >= player2.y - player2.h//2 and a.y + a.h <= player2.y + player2.h//2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    if isSoundOn:
                        bangLargeSound.play()
                    break

            # collision
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            if isSoundOn:
                                bangLargeSound.play()
                            score += 10
                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            if isSoundOn:
                                bangSmallSound.play()
                            score += 20
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                            if isSoundOn:
                                bangSmallSound.play()
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))

            for b2 in playerBullets2:
                if (b2.x >= a.x and b2.x <= a.x + a.w) or b2.x + b2.w >= a.x and b2.x + b2.w <= a.x + a.w:
                    if (b2.y >= a.y and b2.y <= a.y + a.h) or b2.y + b2.h >= a.y and b2.y + b2.h <= a.y + a.h:
                        if a.rank == 3:
                            if isSoundOn:
                                bangLargeSound.play()
                            score += 10
                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            if isSoundOn:
                                bangSmallSound.play()
                            score += 20
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                            if isSoundOn:
                                bangSmallSound.play()
                        asteroids.pop(asteroids.index(a))
                        playerBullets2.pop(playerBullets2.index(b2))
                        break

        for s in stars:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100-s.h or s.x > sw+100 or s.y > sh+100 or s.y < -100-s.h:
                stars.pop(stars.index(s))
                break
            for b in playerBullets:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapidFire = True
                        rfStart = count
                        stars.pop(stars.index(s))
                        playerBullets.pop(playerBullets.index(b))
                        break

            for b2 in playerBullets2:
                if (b2.x >= s.x and b2.x <= s.x + s.w) or b2.x + b2.w >= s.x and b2.x + b2.w <= s.x + s.w:
                    if (b2.y >= s.y and b2.y <= s.y + s.h) or b2.y + b2.h >= s.y and b2.y + b2.h <= s.y + s.h:
                        rapidFire2 = True
                        rfStart2 = count
                        stars.pop(stars.index(s))
                        playerBullets2.pop(playerBullets2.index(b2))
                        break


        if lives <= 0:
            if isSoundOn:
                gameoverSound.play()
            gameover = True

        if rfStart != -1:
            if count - rfStart > 500:
                rapidFire = False
                rfStart = -1

        if rfStart2 != -1:
            if count - rfStart2 > 500:
                rapidFire2 = False
                rfStart2 = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()
        if keys[pygame.K_p]:
            if rapidFire:
                playerBullets.append(Bullet())
                if isSoundOn:
                    shoot.play()
                ##########
        if keys[pygame.K_d]:
            player2.turnLeft()
        if keys[pygame.K_a]:
            player2.turnRight()
        if keys[pygame.K_w]:
            player2.moveForward()
        if keys[pygame.K_SPACE]:
            if rapidFire2:
                playerBullets2.append(Bullet2())
                if isSoundOn:
                    shoot.play()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
                ##########

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not gameover:
                    if not rapidFire:
                        playerBullets.append(Bullet())
                        if isSoundOn:
                            shoot.play()
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidFire2:
                        playerBullets2.append(Bullet2())
                        if isSoundOn:
                            shoot.play()
            if event.key == pygame.K_m:
                isSoundOn = not isSoundOn
            if event.key == pygame.K_TAB:
                if gameover:
                    gameover = False
                    lives = 4
                    asteroids.clear()
                    aliens.clear()
                    alienBullets.clear()
                    aliens2.clear()
                    alienBullets2.clear()
                    stars.clear()
                    if score > highScore:
                        highScore = score
                        c.execute("INSERT INTO scores VALUES (:score)",
                                  {'score': score}
                                  )
                        conn.commit()
                    score = 0


    redrawGameWindow()

pygame.quit()



