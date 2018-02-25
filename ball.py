import pygame as pg
class ball:
    def __init__(self,x,y,m):
        self.x=x
        self.y=y
        self.vx=-155/2
        self.vy= 150/2
        self.h=0.008
        self.size = 4
        self.mass = m

    def draw(self,scr):
        pg.draw.circle(scr,(255, 255, 255),[int(self.x), int(self.y)],self.size)
    def move(self):
        self.x+=self.vx*self.h
        self.y+=self.vy*self.h

    def collideWalls(self,wallx,wally):
        if self.x+self.size>wallx or self.x-self.size<1:
            self.vx*=-1
        if self.y+self.size>wally or self.y-self.size<1:
            self.vy*=-1
