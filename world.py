__author__ = 'nacho'

BOARDSIZE=10

import random

import bug
import cell
import hab

class world:
    def __init__(self):
        self.habs=[]
        self.habs_ptr=0
        self.board=[[cell.cell() for x in range(BOARDSIZE)] for x in range(BOARDSIZE)]



    def add_hab(self,b):
        h=hab.hab()
        h.bug=b
        p=(random.randint(0,BOARDSIZE),random.randint(0,BOARDSIZE))
        h.pos=p
        self.habs.append(h)

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
        pos=pos%9
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


        if b.dead():
            self.habs[self.habs_ptr].remove()
            return
        elif b.mature():
            # offspring
            n=b.offspring()
            e=b.energy()/n
            for i in range(0,n):
                a=b.copy(e)
                self.add_hab(a)

        else:
            pos=self.habs[self.habs_ptr].pos
            # tests for food...


            # tests if the bug asks for an action
            c=b.readcomm()
            op=bug.OPS[c]
            if op=='MOV':
                    v=b.pop()

                    self.habs[self.habs_ptr].pos=self.new_pos(pos,v)
            else:
                b.step()

        self.habs_ptr+=1
        if self.habs_ptr==len(self.habs):
            self.habs_ptr=0


