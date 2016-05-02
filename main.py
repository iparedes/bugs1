__author__ = 'nacho'

import sys
import pygame
from pygame.locals import *
import pyconsole
import logging
import pickle
import codecs
from operator import attrgetter

import bug
import world
from constants import *



logger = logging.getLogger('bugs')
hdlr=logging.FileHandler('./bugs.log')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)



def preload(fich):
    L=[]
    with open(fich,'r') as f:
        for line in f:
            for word in line.split():
                L.append(word)
    return L



def dump():
    '''\
    Dumps bugs contents to dump.log
    '''
    global W
    f=open('./dump.log','w')
    W.dump(f)
    f.close()


def pause():
    '''\
    Pauses the execution.
    '''
    global RUNNING
    RUNNING=False

def cont():
    '''\
    Continues the execution.
    '''
    global RUNNING
    RUNNING=True

def step():
    '''\
    Pauses and Runs one cycle.
    '''
    global RUNNING
    global STEP
    RUNNING=False
    STEP=True

def screen():
    '''\
    Turns on and off the display of the map
    '''
    global SCREEN
    SCREEN=not SCREEN

def terminate():
    '''\
    Terminates the world
    '''
    global GO
    GO=False

pygame.init()
DISPLAYSURF=pygame.display.set_mode((MAPWIDTH+INFOWIDTH,MAPHEIGHT+CONSOLEHEIGHT))
console = pyconsole.Console(
                            DISPLAYSURF, #The surface you want the console to draw on
                            (0,MAPHEIGHT,MAPWIDTH+INFOWIDTH,CONSOLEHEIGHT), #A rectangle defining the size and position of the console
                            functions={"pause":pause,"cont":cont,"step":step,"dump":dump,"screen":screen,"terminate":terminate}, # Functions for the console
                            key_calls={}, # Defines what function Control+char will call, in this case ctrl+d calls sys.exit()
                            syntax={}
                            )

l=preload('./prog')
B=bug.bug()
B.compile(l)

# f=codecs.open('./bug.dat','wb')
# #data_stringB=pickle.dumps(B)
# #f.write(data_stringB)
# pickle.dump(B,f)
#
#
# l=preload('./prog3')
# C=bug.bug()
# C.compile(l)
#
# #data_stringC=pickle.dumps(C)
# #f.write(data_stringC)
# pickle.dump(C,f)
# f.close()
# exit()



W=world.world()
W.add_hab(B,(10,20))
#W.add_hab(C,(10,20))

while(GO):

    console.process_input()

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==MOUSEBUTTONDOWN:
            # Watchout swap rows,cols to match x,y
            y,x=event.pos
            if (x<MAPHEIGHT) and (y<MAPWIDTH):
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


    if RUNNING or STEP:
        go=W.cycle()
        if SCREEN:
            for y in range(TILESHEIGHT):
                for x in range(TILESWIDTH):
                    a=W.board.cell((x,y))
                    if a.is_hab():
                        color=YELLOW
                    elif a.has_food(CARN):
                        color=RED
                    elif a.has_food(HERB):
                        color=GREEN
                    else:
                        color=BROWN
                    pygame.draw.rect(DISPLAYSURF,color,(y*TILESIZE,x*TILESIZE,TILESIZE,TILESIZE))
    if STEP:
        STEP=False

    text=console.font.render("Cycle:",1,WHITE)
    textpos=text.get_rect()
    DISPLAYSURF.blit(text,(MAPWIDTH+MARGIN,MARGIN))
    y=textpos.bottom+MARGIN

    text=console.font.render(str(W.cycles),1,WHITE)
    textpos=text.get_rect()
    textpos=textpos.move((MAPWIDTH+MARGIN,y))
    pygame.draw.rect(DISPLAYSURF,BLACK,textpos)
    DISPLAYSURF.blit(text,(textpos.x,textpos.y))
    y=textpos.bottom+MARGIN

    text=console.font.render("Bugs #:",1,WHITE)
    textpos=text.get_rect()
    DISPLAYSURF.blit(text,(MAPWIDTH+MARGIN,y))
    y+=textpos.bottom+MARGIN

    t=str(len(W.habs))
    text=console.font.render(t,1,WHITE)
    textpos=text.get_rect()
    textpos.width=INFOWIDTH
    textpos=textpos.move((MAPWIDTH+MARGIN,y))
    pygame.draw.rect(DISPLAYSURF,BLACK,textpos)
    DISPLAYSURF.blit(text,(textpos.x,textpos.y))
    y=textpos.bottom+MARGIN

    console.draw()
    pygame.display.update()


L=W.graveyard
M=[x.bug for x in W.habs.values()]
oldest=max(L+M,key=attrgetter('age'))
print "Oldest bug:"
print "Id: "+oldest.id
print "Age: "+str(oldest.age)
l=oldest.decompile()
print l



# for w in W.habs:
#     l=w.bug.decompile()
#     print l
#     print "----------------------"


