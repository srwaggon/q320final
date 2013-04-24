#!/usr/bin/env python

# Samuel Waggoner
# srwaggon@indiana.edu
# Q320
# Assignment 5

import math
import random
import turtle

class Entity(object):
    
    def __init__(self, x=0.0, y=0.0, render=True):
        self.x = x
        self.y = y
        self.size = 3.0
        self.o = random.uniform(0, math.pi*2)

        self.turtle = None

        if render:
            self.turtle = turtle.Turtle()
            self.turtle.speed(0)


    def tick(self, env):
        """Represents a 'tick' of lifetime for this entity"""
        pass



    def isAlive(self):
        return False

    

    def isConsumed(self):
        return False



    def isEdible(self, consumer):
        return False


    def onConsumedBy(self, consumer):
        pass


    def consume(self, edible):
        edible.onConsumedBy(self)


    def sense(self, env):
        pass


    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.o = math.atan2(dy, dx)
        if self.turtle is not None:
            self.turtle.setheading(math.degrees(self.o))
            self.turtle.goto(self.x, self.y)



    def moveTo(self, x, y):
        self.x = x
        self.y = y
        self.o = math.atan2(y, x)
        if self.turtle is not None:
            self.turtle.setheading(math.degrees(self.o))
            self.turtle.goto(x, y)


        
    def forward(self, distance):
        self.move(distance * math.cos(self.o), distance * math.sin(self.o))
        


    def left(self, angle):
        self.o += math.radians(angle)
        if self.turtle is not None:
            self.turtle.setheading(math.degrees(self.o))



    def right(self, angle):
        self.o -= math.radians(angle)
        if self.turtle is not None:
            self.turtle.setheading(math.degrees(self.o))



    def getX(self):
        return self.x



    def getY(self):
        return self.y



    def getAngle(self):
        return self.o

    

    def getSize(self):
        return self.size



    def distFrom(self, x, y):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)



    def overlaps(self, entity): ## overlapping circle algorithm, where self.size represents radius
        return math.sqrt((self.x - entity.x)**2 + (self.y - entity.y)**2) <= self.size + entity.size
        

        
    def __str__(self):
        return "entity@(%0.1f,%0.1f)" % (self.x, self.y)



def run_tests():
    a = Entity()
    a.move(100, 50)
    a.move(-100, 0)
    a.left(30)
    a.forward(30)
    a.right(45)

if __name__ == "__main__":
    screen = turtle.Screen()
    run_tests()
    screen.exitonclick()
    
