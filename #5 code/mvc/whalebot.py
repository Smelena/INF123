from random import randint
from time import sleep
import common


################### MODEL #############################


    


            

################### CONTROLLER #############################

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT

class Controller():
    def __init__(self, m):
        self.m = m
        pygame.init()
    
    def poll(self):
        
        ##move randomly
        '''        cmd = ["right", "up", "down", "left"]
        rand = randint(0,3)
        direction = cmd[rand]
        self.m.do_cmd(direction)'''
        ##Eat Pellets
        x = self.m.pellets[0]
        if(self.m.mybox[0]<x[0]):
            self.m.do_cmd('right')
        if(self.m.mybox[0]>x[0]):
            self.m.do_cmd('left')
        if(self.m.mybox[1]<x[1]):
            self.m.do_cmd('down')
        if(self.m.mybox[1]>x[1]):
            self.m.do_cmd('up')


################### VIEW #############################

class View():
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        self.frames =0;
        
    def display(self):
        
        if self.frames==50:
            print "Position: "+ str(self.m.mybox[0]) + ", " + str(self.m.mybox[1])
            self.frames=0;
        else:
            self.frames+=1
        
     
################### LOOP #############################

model = common.Model()
c = Controller(model)
v = View(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()
