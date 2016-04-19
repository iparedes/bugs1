__author__ = 'nacho'

import random

class cell:
    def __init__(self):
        a=random.randint(0,1)
        if a==1:
            self.food=True
        else:
            self.food=False


