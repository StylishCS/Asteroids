Run the game via exe!!

requirements:
install the following libraries
pygame
subprocess
sqlite3
win32api
datetime



Instructions:
the game has two modes: Singleplayer - Multiplayer
controls for singleplayer mode:

W - forward
R - right
L - left
SPACE - fire
M - mute sound effects

controls for Multiplayer mode:

Player 1 (Blue):
W - forward
R - right
L - left
P - fire
M - mute sound effects

Player 2 (Yellow):
Up Arrow Key - forward
Right Arrow Key  - right
Left Arrow Key  - left
Space - fire
M - mute sound effects


The Game has a database to save Highscore in it.
Astroids has 3 levels (sizes)
every astroid get hit get divided into two smaller astroids depends on it's level
the game has a score system which is:
level 1 asteroid gives 30 points
level 2 asteroid gives 20 points
level 3 asteroid gives 10 points

Alienship spawns and start aiming bullets towards the spaceship
if you kill it you'll gain a 50 points on score and 1 additional live
in singleplayer mode you have 3 lives to get hit by an asteroid
in multiplayer mode you have 4 lives shared by two players, which means if one player get hit
by 3 asteroids and the other player git hit by one asteroid the game will be over

