import pygame as pg
from math import cos, sin, tan, atan2, pi,fabs
import numpy as np

class pendulum:
    def __init__(self, l1, l2, m1, m2, an1, an2, lineX, thickness=15, g=.8):
        self.an1 = an1
        self.an2 = an2
        self.lineY=0
        self.x1 = l1 * sin(self.an1) + lineX
        self.x2 = l2 * sin(self.an2) + self.x1
        self.y1 = l1 * cos(self.an1) + self.lineY
        self.y2 = l2 * cos(self.an2) + self.y1
        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2
        
        self.g = g
        self.h = 0.008
        self.thickness = thickness
        self.lineX = lineX

        self.ticksSinceLastCollision=30


        self.anVel1 = 0
        self.anVel2 = 0
        self.anAcc1 = 0
        self.anAcc2 = 0

    def draw(self, scr):
        #       '''
        c1 = (int(self.x1 - self.thickness * cos(-self.an2) / 2),
              int(self.y1 - self.thickness * sin(-self.an2) / 2))
        c2 = (int(self.x2 - self.thickness * cos(-self.an2) / 2),
              int(self.y2 - self.thickness * sin(-self.an2) / 2))
        c3 = (int(self.x2 + self.thickness * cos(-self.an2) / 2),
              int(self.y2 + self.thickness * sin(-self.an2) / 2))
        c4 = (int(self.x1 + self.thickness * cos(-self.an2) / 2),
              int(self.y1 + self.thickness * sin(-self.an2) / 2))
        #      '''

        pg.draw.line(scr, (255, 255, 255), [self.lineX, self.lineY], [self.x1, self.y1])
        pg.draw.line(scr, (255, 255, 255), [self.x1, self.y1], [self.x2, self.y2])
        #pg.draw.circle(scr,(255, 255, 255),[int(self.x1), int(self.y1)],9)
        #pg.draw.circle(scr,(255, 255, 255),[int(self.x2), int(self.y2)],9)
        pg.draw.polygon(scr, (255, 255, 255), [c1, c2, c3, c4])
        


    def move(self):
        self.an1,self.an2,self.anVel1,self.anVel2,self.anAcc1,self.anAcc2 = self.updateVal(self.an1,self.an2,self.anVel1,self.anVel2,self.anAcc1,self.anAcc2)
        
        
        self.x1 = self.l1 * sin(self.an1) + self.lineX
        self.x2 = self.l2 * sin(self.an2) + self.x1
        self.y1 = self.l1 * cos(self.an1) + self.lineY
        self.y2 = self.l2 * cos(self.an2) + self.y1
    
    def updateVal(self, an1, an2, anVel1, anVel2, anAcc1, anAcc2):

        anAcc1 = ((-(self.g * (2 * self.m1 + self.m2) * sin(an1)) - (self.m2 * self.g * sin(
                    an1 - an2 * 2)) - (2 * sin(an1 - an2) * self.m2 * (self.l2 * anVel2**2 + cos(an1 - an2) * self.l1 * (anVel1**2)))
                    / (self.l1 * (2 * self.m1 + self.m2 - self.m2 * cos(2 * (an1 - an2))))))

        anAcc2 = ((2 * sin(an1 - an2) * ((anVel1**2) * self.l1 + self.g * (self.m1 + self.m2) * cos(an1) + (anVel2 **
            2) * self.l2 * self.m2 * cos(an1 - an1))) / (self.l1 * (2 * self.m1 + self.m2 - self.m2 * cos(2 * (an1 - an2)))))
        
        anVel1 += anAcc1 * self.h 
        anVel2 += anAcc2 * self.h
        an1 += anVel1 * self.h
        an2 += anVel2 * self.h
        return (an1, an2, anVel1, anVel2, anAcc1, anAcc2)

    def checkCollision(self,ball,scr):
        self.ticksSinceLastCollision+=1
        if (self.ticksSinceLastCollision>55):
            self.ticksSinceLastCollision=55
        else:
             return


        cx = cos(self.an2)*(ball.x-self.x1)-sin(self.an2)*(ball.y-self.y1)+self.x1
        cy = sin(self.an2)*(ball.x-self.x1)+cos(self.an2)*(ball.y-self.y1)+self.y1
        colFromAbove=True
        if (cx<self.x1-self.thickness/2):
            clx=self.x1-self.thickness/2
        elif (cx>self.x1+self.thickness/2):
            clx=self.x1+self.thickness/2
        else:
            clx = cx
            colFromAbove=False

        if (cy<self.y1):
            cly=self.y1
        elif (cy>self.y1+self.l2):
            cly=self.y1+self.l2
        else:
            cly = cy


        #debugging
        if (True):
            pg.draw.rect(scr,(255,0,255),[self.x1-self.thickness/2,self.y1,self.thickness,self.l2])
            pg.draw.circle(scr,(0,255,0),[int(cx),int(cy)],5)
            pg.draw.circle(scr,(255,0,0),[int(self.x1),int(self.y1)],5)
            pg.draw.line(scr,(255,0,0),[clx,cly],[cx,cy])
            pg.display.flip()


        #check if collision happened and calculate new velocity

        a=clx-cx
        b=cly-cy



        if ((a**2+b**2)**(1/2)<=ball.size+1):
            #print("collision%d"%a)
            cf=0.05

            pv=self.anVel1*self.l1+self.anVel2*(cly-self.y1)
            bvx = cos(self.an2)*(ball.vx)-sin(self.an2)*(ball.vy)
            bvy = sin(self.an2)*(ball.vx)+cos(self.an2)*(ball.vy)

            if not colFromAbove:
                bvx*=-1
                #if (bvy>=0)!=(pv>=0):
                temp=bvy
                bvy=bvy-pv*cf*(self.m1+self.m2)-bvy*cf*ball.mass
                pv=(pv-temp*cf*ball.mass-pv*cf*(self.m1+self.m2))
                #else:
                    #bvy,pv=bvx-pv*cf*(self.m1+self.m2)-bvx*cf*ball.mass,(pv-bvx*cf*ball.mass-pv*cf*(self.m1+self.m2))

            else:
                bvy*=-1
                #bvx,pv=(bvx-pv*cf*(self.m1+self.m2)-bvx*cf*ball.mass/10),(pv-bvx*cf*ball.mass-pv*cf*(self.m1+self.m2))/10

            ball.vx= cos(-self.an2)*(bvx)-sin(-self.an2)*(bvy)
            ball.vy= sin(-self.an2)*(bvx)+cos(-self.an2)*(bvy)
            if cly-self.y1!=0:
                self.anVel2 = (pv-self.anVel1*self.l1)/(cly-self.y1)









 