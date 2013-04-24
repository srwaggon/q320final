#!/usr/bin/env python


import Agent, Env, Food, random, turtle

def sim(steps=1000, pop=40, startingFood=100, boundary=300, render=True):
    if render:
        scr = turtle.Screen()
        scr.colormode(255)
        scr.delay(1)

    e = Env.Env(render=render)

    for i in range(pop):
        code = Agent.randomCode()
        gender = random.choice([True,False])
        e.addAgent(Agent.Agent(code, isMale=gender, x=random.randint(-boundary,boundary), y=random.randint(-boundary, boundary), render=render))

    for i in range(startingFood):
        x = random.uniform(-boundary, boundary)
        y = random.uniform(-boundary, boundary)
        nutrients = random.uniform(50,100)
        e.addFood(Food.Food(x, y, nutrients, render=render))

    outfile = open("log.txt", 'w')
    while steps != 0:
        e.tick()
        p = len(e.getAgents())
        outfile.write(str(p) + "\n")
        if p == 0:
            print "All agents deceased."
            break
        steps -= 1
    print "final population:", p
    print "Simulation ended."

    outfile.close()
    if render:
        scr.exitonclick()


if __name__ == "__main__":
    sim(steps=1000, render=False)

    
