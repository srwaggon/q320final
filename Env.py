#!/usr/bin/env python

import Food, math, random, turtle

class Env(object):

    def __init__(self, render=True):
        self.progs = []
        self.food = []
        self.render = render


    def addProg(self, prog):
        self.progs.append(prog)

    def getProgs(self):
        return self.progs

    def removeProg(self, prog):
        self.progs.remove(prog)

    def addFood(self, food):
        self.food.append(food)

    def getFood(self):
        return self.food

    def removeFood(self, food):
        self.food.remove(food)

    def tick(self):
        for nom in self.food:
            if nom.isConsumed():
                self.food.remove(nom)
            

        for prog in self.progs:
            prog.tick(self)
            if not prog.isAlive():
                self.progs.remove(prog)
    

if __name__ == "__main__":
    e = Env()
