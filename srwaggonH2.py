#!/usr/bin/env python


import Prog, Env, Food, random, turtle

def sim(steps=1000, pop=40, noms=100, nutrients=40, bounds=300, render=True):
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


    outfile = open("log.txt", 'w')


    while steps != 0:
        env.tick()
        p = len(env.getProgs())
        outfile.write(str(p) + "\n")
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


        print len(env.getFood()) * nutrients, nrg, numProgs, 1.0*nrg / numProgs, 1.0* v / numProgs

    print "final population:", p
    print "Simulation ended."

    outfile.close()
    if render:
        scr.exitonclick()


if __name__ == "__main__":
    steps = -1
    bounds = 600
    pop = 40
    food = pop * 100 # 400
    nutrients = 10
    render=True
    #render=False

    food_density = 1.0 * food / (bounds*bounds)
    nut_density = 1.0 * nutrients*food / (bounds*bounds)
    print "food density", food_density
    print "nutritional density", nut_density
    
    sim(steps, pop, food, nutrients, bounds, render)

    
