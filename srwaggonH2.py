#!/usr/bin/env python


import Prog, Env, Food, random, turtle

def sim(steps=1000, pop=40, noms=100, nutrients=40, bounds=300, render=True, log=None):

    if render:
        scr = turtle.Screen()
        scr.colormode(255)
        scr.delay(1)

    env = Env.Env(render=render)

    for i in range(noms):
        x = random.uniform(-bounds, bounds)
        y = random.uniform(-bounds, bounds)
        env.addFood(Food.Food(x, y, nutrients, render=render))

    for i in range(pop):
        gender = random.choice([True,False])
        env.addProg(Prog.Prog(x=random.randint(-bounds,bounds), y=random.randint(-bounds, bounds), render=render))


    if log:
        log = open(log, "w")


    while steps != 0:
        env.tick()
        p = len(env.getProgs())


        if log:
            v = [str(prog.getVelocity()) for prog in env.getProgs()]
            v = [str(len(env.getFood()))] + v
            log.write(",".join(v)+"\n")

        if p == 0:
            print "All progs deceased."
            break
        steps -= 1


        nrg = 0
        v = 0
        progs = env.getProgs()
        numProgs = len(progs)
        for prog in progs:
            nrg += prog.getEnergy()
            v += prog.getVelocity()


        print steps, len(env.getFood()) * nutrients, nrg, numProgs, 1.0*nrg / numProgs, 1.0* v / numProgs
            
    print "final population:", p
    print "Simulation ended."

    if log:
        log.close()

    if render:
        scr.exitonclick()


if __name__ == "__main__":
    steps = 1000
    bounds = 500
    pop = 100
    food = 5000
    nutrients = 20
    render=True
    #render=False


    food_density = float(food) / (bounds*bounds)
    nut_density = float(nutrients)*food / (bounds*bounds)
    print "food density", food_density
    print "nutritional density", nut_density
    
    sim(steps, pop, food, nutrients, bounds, render, "log.txt")
