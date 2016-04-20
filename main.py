__author__ = 'nacho'

import logging

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

l=preload('./prog')

B=bug.bug()
B.compile(l)


W=world.world()
W.add_hab(B)

go=True
while(go):
    go=W.step()


