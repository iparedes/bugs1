__author__ = 'nacho'

#
BOARDSIZE=10
# Food per cell
FOODPACK=10

SOWRATE=5

MUTRATE=1 # percentage
STDDEV=10 # percentage

import random
import logging
import numpy.random

logger=logging.getLogger('bugs')

import bug
import cell
import hab

class world:
    def __init__(self):
        self.habs=[]
        self.habs_ptr=0
        self.cycles=0
        self.habcount=0
        self.board=[[cell.cell() for x in range(BOARDSIZE)] for x in range(BOARDSIZE)]


    def cell(self,pos):
        return self.board[pos[0]][pos[1]]



    def add_hab(self,b):
        h=hab.hab()
        h.bug=b
        self.habcount+=1
        ident=hex(self.habcount)[2:]
        h.bug.id=ident
        #p=(random.randint(0,BOARDSIZE-1),random.randint(0,BOARDSIZE-1))
        p=(numpy.random.randint(0,BOARDSIZE),numpy.random.randint(0,BOARDSIZE))
        h.pos=p
        self.habs.append(h)
        logger.debug('Added bug '+ident)

    def new_pos(self,pos,dir):
        """

        :param pos:
        :param dir:
           812
           7*3
           654
           0:random
        :return:
        """
        # normalizes to an address code
        dir=dir%9
        shift={
            1: (0,-1),
            2: (1,-1),
            3: (1,0),
            4: (1,1),
            5: (0,1),
            6: (-1,1),
            7: (-1,0),
            8: (-1,-1),
            0: (random.randint(-1,1),random.randint(-1,1)),
        }[dir]

        a=pos[0]+shift[0]
        b=pos[1]+shift[1]
        if a<0:
            a=BOARDSIZE-1
        elif a==BOARDSIZE:
            a=0
        if b<0:
            b=BOARDSIZE-1
        elif b==BOARDSIZE:
            b=0

        return (a,b)


    def step(self):
        # get current bug
        b=self.habs[self.habs_ptr].bug
        pos=self.habs[self.habs_ptr].pos
        cell=self.cell(pos)
        ident=b.id

        # This actions are lead by the world, when to be realistic should be part of the behaviour of the bug, but...
        if b.dead():
            logger.debug('Dead bug '+ident)
            del self.habs[self.habs_ptr]
            self.habs_ptr-=1
        elif b.mature():
            # offspring
            logger.debug('Offspringing '+ident)
            l=b.offspring()
            for i in l:
                self.mutate(i)
                self.add_hab(i)
        else:
            if cell.has_food():
                logger.debug('Feeding '+ident)
                b.feed(FOODPACK)
                cell.consume_food()
            # tests if the bug asks for an action
            c=b.readcomm()
            op=bug.OPS[c]
            if op=='MOV':
                    logger.debug('MOV '+ident)
                    v=b.pop()
                    self.habs[self.habs_ptr].pos=self.new_pos(pos,v)
            else:
                b.step()

        self.habs_ptr+=1
        if self.habs_ptr==len(self.habs):
            if self.habs_ptr==0:
                logger.debug('The end of the world')
                return False
            self.cycles+=1
            logger.debug('New cycle '+str(self.cycles)+'. '+str(len(self.habs))+' bugs.')
            self.sow()
            self.habs_ptr=0

        return True

    def sow(self):
        logger.debug('Sowing...')
        m=BOARDSIZE*BOARDSIZE*SOWRATE/100
        for i in range(0,m):
            x=random.randint(0,BOARDSIZE-1)
            y=random.randint(0,BOARDSIZE-1)

            self.board[x][y].grow_food()

    def mutate(self,bug):
        size=bug.size()
        average=size*MUTRATE/100
        stdev=average*STDDEV/100
        tomut=numpy.random.normal(average,stdev+1)
        listmut=numpy.random.randint(0,size,size=int(tomut))
        bug.mutate(listmut)


