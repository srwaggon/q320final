#!/usr/bin/env python

import Food, math, random, turtle

class Env(object):

    def __init__(self, render=True):
        self.agents = []
        self.food = []
        self.timer = 0
        self.range = 300
        self.render = render


    def addAgent(self, agent):
        self.agents.append(agent)

    def getAgents(self):
        return self.agents

    def removeAgent(self, agent):
        self.agents.remove(agent)

    def addFood(self, food):
        self.food.append(food)

    def getFood(self):
        return self.food

    def removeFood(self, food):
        self.food.remove(food)

    def tick(self):
        self.timer += 1

        if self.timer % 4 == 0:
            self.timer = 0
            
            x = random.uniform(-self.range, self.range)
            y = random.uniform(-self.range, self.range)
            nutrients = random.uniform(50,100)
            self.addFood(Food.Food(x, y, nutrients, self.render))

        for food in self.food:
            food.tick(self)

        for agent in self.agents:
            agent.tick(self)
            if not agent.isAlive():
                self.agents.remove(agent)


if __name__ == "__main__":
    e = Env()
