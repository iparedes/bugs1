__author__ = 'nacho'

import sys
import pygame
from pygame.locals import *
import logging

MAPWIDTH=50
MAPHEIGHT=50
TILESIZE=10

RED=(255,0,0)
ORANGE=(255,165,0)
YELLOW=(255,255,0)
GREEN=(0,205,0)
BROWN=(153,76,0)

logger = logging.getLogger('bugs')
hdlr=logging.FileHandler('./bugs.log')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


import bug
import world

def preload(fich):
    L=[]
    with open(fich,'r') as f:
        for line in f:
            for word in line.split():
                L.append(word)
    return L


pygame.init()
DISPLAYSURF=pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))

l=preload('./prog')

B=bug.bug()
B.compile(l)


W=world.world()
W.add_hab(B)

go=True
while(go):
    go=W.cycle()
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            a=W.board.cell((x,y))
            if a.is_hab():
                color=YELLOW
            elif a.has_food():
                color=GREEN
            else:
                color=BROWN
            pygame.draw.rect(DISPLAYSURF,color,(y*TILESIZE,x*TILESIZE,TILESIZE,TILESIZE))



    pygame.display.update()
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==MOUSEBUTTONDOWN:
            # Watchout swap rows,cols to match x,y
            y,x=event.pos
            mx=x/TILESIZE
            my=y/TILESIZE
            cell=W.board.cell((mx,my))
            if cell.is_hab():
                id=cell.hab
                l=W.habs[id].bug.decompile()
                print "================="
                for i in l:
                    print i
                print "================="
            print str(mx)+","+str(my)

for w in W.habs:
    l=w.bug.decompile()
    print l
    print "----------------------"


