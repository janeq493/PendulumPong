import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50" 


import pygame as pg
from pendulum import pendulum
from ball import ball
from math import pi
pg.init()
h,w=600,400
scr=pg.display.set_mode((h,w))

pg.draw.rect(scr,(0,0,0),[0,0,600,600])

p1 = pendulum(50,100,1,1,0,0,50)
p2 = pendulum(50,100,1,1,-0,-0,550)

b= ball(160,38,0.6)
clc = pg.time.Clock()
while True: 

    p1.checkCollision(b,scr)  
    p2.checkCollision(b,scr)  

    b.collideWalls(h-1,w-1)   
    p1.move()
    p2.move()
    b.move()

    pg.draw.rect(scr,(0,0,0),[0,0,600,600])

    p1.draw(scr)
    p2.draw(scr)
    b.draw(scr)
    pg.display.flip()
    #clc.tick(300)
