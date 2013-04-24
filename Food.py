#!/usr/bin/env python

# Samuel Waggoner
# srwaggon@indiana.edu
# Q320
# Assignment 5


import Entity, random, turtle


class Food(Entity.Entity):

    def __init__(self, x=0.0, y=0.0, nutrients=(random.uniform(5,25)+10), render=True):
        Entity.Entity.__init__(self, x, y, render)

        self.nutrients = nutrients

        if self.turtle is not None:
            self.turtle.penup()
            self.turtle.hideturtle()
            self.turtle.setpos(self.x, self.y)
            self.turtle.color((128-nutrients, 255, 128-nutrients))
            self.turtle.dot()



    def tick(self, env):
        pass # Don't do anything. Food need not.


    def isAlive(self):
        return False


    def isConsumed(self):
        return self.nutrients <= 0


    def isEdible(self, consumer):
        return self.nutrients > 0


    def onConsumedBy(self, consumer):
        consumer.energy += self.nutrients
        self.nutrients = 0
        if self.turtle is not None:
            self.turtle.color((255,255,255))
            self.turtle.dot()



    def __str__(self):
        return "food@(%0.0f, %0.0f)" % (self.x, self.y)



def run_tests():
    screen = turtle.Screen()
    screen.colormode(255)
    f = Food()
    screen.exitonclick()


if __name__ == "__main__":
    run_tests()
