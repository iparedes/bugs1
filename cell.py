__author__ = 'nacho'

import random

class cell:
    def __init__(self):
        a=random.randint(0,1)
        if a==1:
            self.grow_food()
        else:
            self.consume_food()

    def has_food(self):
        return self.food

    def grow_food(self):
        self.food=True

    def consume_food(self):
        self.food=False

