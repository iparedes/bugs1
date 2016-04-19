__author__ = 'nacho'

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

C=B.copy()

W=world.world()
W.add_hab(B)
#W.add_hab(C)

while(True):
    W.step()


