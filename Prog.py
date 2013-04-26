#!/usr/bin/env python
#
# Prog.py


import Entity, math, random, turtle


class Prog(Entity.Entity):

    PUBERTY = 30
    GESTATION = 20

    # Colours:
    BOY_COLOUR   = (128,128,196)  # sexually immature male
    GIRL_COLOUR  = (196,128,128)  # sexually immature female
    MAN_COLOUR   = (  0,  0,255)  # sexually mature male
    WOMAN_COLOUR = (255,  0,  0)  # sexually mature female
    PREG_COLOUR  = (255,128,255)  # pregnant female (must be sexually mature)

    HUNGER_THRESHOLD = 100
    MUTATION_RATE = .25
    REPRODUCTION_COST = 10 # Subtracted from prog's energy upon fertilization.

    def __init__(self, velocity=None, gender=None, x=0.0, y=0.0, render=True):
        """
        Create a new Prog with a genecode (32-bit integer).
        """
        Entity.Entity.__init__(self, x, y, render)

        # Non genetic traits
        self.age = 0#random.randint(0, Prog.PUBERTY)
        self.energy = 50
        self.gender = gender if gender is not None else random.choice(["male", "female"])
        self.s = 1 # Sense of.. smell...

        self.velocity = velocity if velocity is not None else random.randint(0, 1000)
        
        if random.random() <= Prog.MUTATION_RATE:
            self.velocity += random.randint(-5, 5)

        # Reproductive Fields
        self.gestationPeriod = 0 # Not preggers. Males won't become preggers.
        self.baby = None 

        # Render Fields
        if render:
            self.turtle = turtle.Turtle()
            self.turtle.speed(0)
            self.turtle.penup()
            self.turtle.goto(self.x, self.y)
            self.turtle.setheading(math.degrees(self.o))
            color = Prog.BOY_COLOUR if self.isMale() else Prog.GIRL_COLOUR
            self.turtle.color(color)


    def die(self, cause=""):
        s = str(self) + " has died"

        if cause != "":
            s += " from " + cause

        if self.gestationPeriod > 0:
            s += " while pregnant"

        s += "!"

        print s

        self.energy = 0
        if self.turtle is not None:
            self.turtle.hideturtle()



    def moveSelf(self):
        self.move(math.cos(self.o) * self.getVelocity(), math.sin(self.o) * self.getVelocity())



    def hunt_for_mates(self, env):
        self.ps = self.s
        self.s = 0.0
        for prog in env.getProgs():
            if self.canMateWith(prog):
                d = self.distFrom(prog.getX(), prog.getY())
                if d != 0:
                    self.s += 1.0 / d

    def hunt_for_food(self, env):
        self.ps = self.s
        self.s = 0.0
        for nom in env.getFood():
            if nom.isEdible(self):
                d = self.distFrom(nom.getX(), nom.getY())
                if d != 0:
                    self.s += 1.0 / d


    def klinokinesis(self):
        if self.ps >= self.s:
            self.o += random.uniform(0, math.pi)



    def tick(self, env):

        if self.isAlive():

            # Age, set colour.
            self.age += 1
            if self.turtle is not None and self.age == Prog.PUBERTY:
                c = Prog.MAN_COLOUR if self.isMale() else Prog.WOMAN_COLOUR
                self.turtle.color(c)


            # Hunt for mates if satiated, else for food.
            if not self.isHungry() and not self.isPregnant():
                self.hunt_for_mates(env)
            else:
                self.hunt_for_food(env)
            self.klinokinesis()
            self.moveSelf()

            # Eat anything underneath.
            for food in env.getFood():
                if food.isEdible(self) and self.overlaps(food):
                    self.consume(food)
        
            ## Handle preggers. Give birth if time is right.
            if self.gestationPeriod > 0:
                self.gestationPeriod -= 1
                if self.gestationPeriod == 0:
                    self.giveBirth(env)

            # Else.. and if male.. try to knock 'em up!
            elif self.isMale() and self.ofAge():
                for prog in env.getProgs():
                    if self.canMateWith(prog) and self.overlaps(prog):
                        prog.empregnateBy(self)

            self.energy -= 1
            if self.energy <= 0:
                self.die("starvation")
            


    def isPregnant(self):
        return not self.isMale() and self.baby != None
            


    def isFertile(self):
        return self.ofAge() and not self.isPregnant()



    def empregnateBy(self, mate):
        ## Called by female's perspective only.
        if not self.isMale() and self.isFertile() and mate.isMale():
            # Takes energy, man.
            self.energy -= Prog.REPRODUCTION_COST
            mate.energy -= Prog.REPRODUCTION_COST
            
            self.gestationPeriod = Prog.GESTATION
            self.mate = mate

            if self.turtle is not None:
                self.turtle.color(Prog.PREG_COLOUR)
            


    def giveBirth(self, env):
        gender = random.choice(["male", "female"])
        velocity = random.choice([self.velocity, self.mate.velocity])
        baby = Prog(velocity, gender=gender, x=self.x, y=self.y, render=self.turtle != None)
        env.addProg(baby)
        print str(baby), "was born!"
        self.baby = None
        self.mate = None
        self.gestationPeriod = 0
        if self.turtle is not None:
            self.turtle.color(Prog.WOMAN_COLOUR)




    def __str__(self):
        return "%s(%d,%d)" % (self.gender, self.age, self.getVelocity())


            
#################
### ACCESSORS ###
#################


    def getAge(self):
        return self.age

    
    def isAlive(self):
        return self.energy > 0
    
    def isHungry(self):
        return self.energy < Prog.HUNGER_THRESHOLD

    def isMale(self):
        return True if self.gender == "male" else False

    def getEnergy(self):
        return self.energy


    def getGender(self):
        return self.gender


    def getVelocity(self):
        return self.velocity


    def ofAge(self):
        return self.age >= Prog.PUBERTY


    def isOppositeGender(self, prog):
        return self.isMale() != prog.isMale()


    def canMateWith(self, other):
        return self.ofAge() and self.isOppositeGender(other) and other.isFertile()


        

if __name__ == "__main__":
    pass


