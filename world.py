__author__ = 'nacho'

#
BOARDSIZE=50
# Food per cell
FOODPACK=10

SOWRATE=1

MUTRATE=10 # percentage
STDDEV=10 # percentage

import random
import logging
import numpy.random

logger=logging.getLogger('bugs')

import bug
import hab
import board

class world:
    def __init__(self):
        self.habs={}
        self.cycles=0
        self.habcount=0
        self.board=board.board(BOARDSIZE,BOARDSIZE)
        self.deaths=[] # Ident of bugs dead during the cycle
        self.newborns=[] # Newborns during the cycle


    def add_hab(self,b):
        h=hab.hab()
        h.bug=b
        self.habcount+=1
        ident=hex(self.habcount)[2:]
        h.bug.id=ident


        # tries to generate a free pos randomly
        # WATCH OUT!!
        p=self.rand_pos()
        while self.board.cell(p).is_hab():
            p=self.rand_pos()

        h.pos=p
        #self.habs.append(h)
        self.habs[ident]=h

        self.board.cell(p).set_hab(ident)
        logger.debug('Added bug '+ident)

    def rand_pos(self):
        return numpy.random.randint(0,BOARDSIZE),numpy.random.randint(0,BOARDSIZE)

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


    def step(self,hab):
        """
        Steps an inhabitant
        :param hab:
        :return:
        """
        # get current bug
        b=hab.bug
        pos=hab.pos
        cell=self.board.cell(pos)
        ident=b.id

        # This actions are lead by the world, when to be realistic should be part of the behaviour of the bug, but...
        if b.dead():
            logger.debug('Dead bug '+ident)
            self.deaths.append(ident)
            cell.del_hab()
        elif b.mature():
            # offspring
            logger.debug('Offspringing '+ident)
            l=b.offspring()
            for i in l:
                self.mutate(i)
                self.newborns.append(i)
                #self.add_hab(i)
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
                    # WATCH HERE
                    newpos=self.new_pos(pos,v)
                    if not self.board.cell(newpos).is_hab():
                        hab.pos=newpos
                        self.board.cell(pos).del_hab()
                        self.board.cell(newpos).set_hab(ident)
            else:
                b.step()


    def cycle(self):
        for i in self.deaths:
            self.habs.pop(i,None)
        self.deaths=[]
        for i in self.newborns:
            self.add_hab(i)
        self.newborns=[]
        if len(self.habs)==0:
            logger.debug('The end of the world')
            return False
        logger.debug('New cycle '+str(self.cycles)+'. '+str(len(self.habs))+' bugs.')
        for k,h in self.habs.iteritems():
            self.step(h)

        self.cycles+=1
        self.sow()
        return True

    def sow(self):
        logger.debug('Sowing...')
        m=BOARDSIZE*BOARDSIZE*SOWRATE/100
        for i in range(0,int(m)):
            #x=numpy.random.randint(0,BOARDSIZE/5)*5
            x=numpy.random.randint(0,BOARDSIZE)
            y=numpy.random.randint(0,BOARDSIZE)

            self.board.cell((x,y)).grow_food()

    def mutate(self,bug):
        size=bug.size()
        average=size*MUTRATE/100
        stdev=average*STDDEV/100
        tomut=numpy.random.normal(average,stdev+1)
        listmut=numpy.random.randint(0,size,size=int(tomut))
        bug.mutate(listmut)


