#!/usr/bin/env python
#
# agent.py


import Entity, math, random, turtle


PUBERTY = 30
GESTATION = 20


# Genetic Code represented as a 32-bit integer:
# 0000 0000  0000 0000  0000 0000  0000 0000


# Traits represented by values on certain bits (shifted to 0th index).
                                   # Bits indices
VELOCITY_BITS =    8 +    4 +    2 +    1 # 0-3
TURNING_BITS  =          64 +   32 +   16 # 4-6
MOXIE_BITS    =         512 +  256 +  128 # 7-9
SASS_BITS     =        4096 + 2048 + 1024 # 10-12
ENERGY_BITS   = 16711680
LIFESPAN_BITS = 4278190080


# e.g, value of:
# ---- ----  ---- ----  ---- ----  ---- XXXX Velocity Bits, value 
# ---- ----  ---- ----  ---- ----  -XXX ---- Turning Radius Bits, value 3
# 0000 0000  0000 0000  0000 0000  0011 0101
# 



# Colours:
BOY_COLOUR   = (128,128,196)  # sexually immature male
GIRL_COLOUR  = (196,128,128)  # sexually immature female
MAN_COLOUR   = (  0,  0,255)  # sexually mature male
WOMAN_COLOUR = (255,  0,  0)  # sexually mature female
PREG_COLOUR  = (255,128,255)  # pregnant female (must be sexually mature)


REPRODUCTION_COST = 0 # Subtracted by agents upon fertilization.

class Agent(Entity.Entity):

    def __init__(self, genecode, isMale, x=0.0, y=0.0, render=True):
        """
        Create a new Agent with a genecode (32-bit integer).
        """
        Entity.Entity.__init__(self, x, y, render)

        # Non genetic traits
        self.age = random.randint(0,PUBERTY)
        self.energy = 100
        self.gender = "male" if isMale else "female"
        self.s = 1 # Sense of.. smell...

        # Genetic code
        self.code = genecode

        # Reproductive Fields
        self.gestationPeriod = 0 # Not preggers. Males won't become preggers.

        # Render Fields
        self.turtle = None
        self.render = render
        if render:
            self.turtle = turtle.Turtle()
            self.turtle.speed(0)
            self.turtle.penup()
            self.turtle.goto(self.x, self.y)
            self.turtle.setheading(math.degrees(self.o))
            # Use genetic colour -- Why not?
            # r = self.code >> 0 & 255
            # g = self.code >> 8 & 255
            # b = self.code >> 16 & 255
            # self.turtle.color((r,g,b))
            color = BOY_COLOUR if self.isMale() else GIRL_COLOUR
            self.turtle.color(color)


    def die(self, cause=""):
        s = str(self) + " has died"

        if cause != "":
            s += " from " + cause

        if self.gestationPeriod > 0:
            s += " while pregnant"

        s += "!"

        #print s

        self.energy = 0
        if self.turtle is not None:
            self.turtle.hideturtle()



    def moveSelf(self):
        self.move(math.cos(self.o) * self.getVelocity(), math.sin(self.o) * self.getVelocity())



    def hunt_for_mates(self, env):
        self.ps = self.s
        self.s = 0.0
        for agent in env.getAgents():
            if self.canMateWith(agent):
                d = self.distFrom(agent.getX(), agent.getY())
                if d != 0:
                    self.s += 1.0 / d

    def hunt_for_food(self, env):
        self.ps = self.s
        self.s = 0.0
        for food in env.getFood():
            if food.isEdible(self):
                d = self.distFrom(food.getX(), food.getY())
                if d != 0:
                    self.s += 1.0 / d


    def klinokinesis(self):
        if self.ps >= self.s:
            self.o += random.uniform(0, math.pi * self.getTurn())



    def tick(self, env):

        if self.isAlive():

            # Age, set colour.
            self.age += 1
            if self.turtle is not None and self.age == PUBERTY:
                c = MAN_COLOUR if self.isMale() else WOMAN_COLOUR
                self.turtle.color(c)


            # Hunt for mates if satiated, else for food.
            if self.energy > self.getMaxEnergy() and not self.isPregnant():
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
                    baby = self.giveBirth()
                    env.addAgent(baby)

            # Else.. and if male.. try to knock 'em up!
            elif self.isMale() and self.ofAge():
                for agent in env.getAgents():
                    if agent.isOppositeGender(self) and agent.isFertile() and self.overlaps(agent):
                        agent.empregnateBy(self)
                        self.energy -= REPRODUCTION_COST
                        agent.energy -= REPRODUCTION_COST

            self.energy -= 1
            if self.energy <= 0:
                self.die("starvation")
            


    def isPregnant(self):
        return self.gestationPeriod > 0
            


    def isFertile(self):
        return self.ofAge() and not self.isPregnant()



    def empregnateBy(self, mate):
        ## Called by female's perspective only.
        if not self.isMale() and self.isFertile() and mate.isMale():
            self.gestationPeriod = GESTATION
            self.babyCode = mutate(crossover(self.code, mate.code))
            #print str(self), "became pregnant by", str(mate)
            if self.turtle is not None:
                self.turtle.color(PREG_COLOUR)


    def giveBirth(self):
        self.gestationPeriod = 0
        gender = random.choice([True, False])
        baby = Agent(self.babyCode, isMale=gender, x=self.x, y=self.y, render=self.render )
        #print( str(baby) + " was born!")
        if self.turtle is not None:
            self.turtle.color(WOMAN_COLOUR)
        return baby


    def __str__(self):
        return "%s(%d,%d,%d,%d,%d,%d)" % (self.getGender(), self.getVelocity(), self.getTurn(), self.getMoxie(), self.getSass(), self.getMaxEnergy(), self.getLifeSpan())
    


            
#################
### ACCESSORS ###
#################


    def getAge(self):
        return self.age

    def getCode(self):
        """ Returns the genetic code of this Agent. """
        # 32-bit code of 1's and 0's.
        return self.code
        

    def printCode(self):
        """ Prints the bits of the genetic code of this Agent. """
        # Code prints in little-endian.
        s = ""
        for i in range(31, -1, -1):
            s += str((self.code >> i) & 1)
            if i % 4 == 0:
                s += " " 
        print(s)
        

    def getVelocity(self):
        """ Returns the velocity of this Agent [0, 15] """
        # Bits 1-4 of genecode (or 1 if == 0)
        # 00000000 00000000 00000000  00001111
        return (self.code & VELOCITY_BITS >> 0) or 1


    def getTurn(self):
        """ Returns the turn split of this Agent [0, 15] """
        # Bits 5-7 of genecode (or 1 if == 0)
        # 00000000 00000000 00000000 01110000
        return (self.code & TURNING_BITS >> 3) or 1


    def getMoxie(self):
        """ Returns the sexiness of this Agent [0, 15] """
        # Bits 8-10 of genecode
        # 00000000 00000000 00000011 10000000
        return self.code & MOXIE_BITS >> 7


    def getSass(self):
        """ Returns how picky this agent is to reproduce [0, 15] """
        # Bits 11-13 of genecode
        # 00000000 00000000 00011100 00000000
        return self.code & SASS_BITS >> 10


    def getMaxEnergy(self):
        """
        Returns the maximum amount of energy this Agent can store
        before he decides to hunt for food [0, 255]
        """
        # Bits 17-24 of genecode (3rd byte)
        # 00000000 11111111 00000000  00000000
        return self.code & ENERGY_BITS >> 16


    def getLifeSpan(self):
        """ Returns the maximum age of this Agent [0, 255] """
        # Bits 25-32 of genecode (4th byte)
        # 11111111 00000000 00000000  00000000
        return self.code & LIFESPAN_BITS >> 24
    
    def isAlive(self):
        return self.energy > 0


    def isMale(self):
        return True if self.gender == "male" else False


    def getGender(self):
        return self.gender

    def ofAge(self):
        return self.age >= PUBERTY

    def isOppositeGender(self, agent):
        return self.isMale() != agent.isMale()

    def canMateWith(self, other):
        return self.isOppositeGender(other) and self.ofAge() and other.ofAge()


    def printStatus(self):
        self.printCode()
        print self.getCode(), "code"
        print self.getGender()
        print self.getVelocity(), "velocity"
        print self.getTurn(), "turn"
        print self.getMoxie(), "moxie"
        print self.getSass(), "sass"
        print self.getMaxEnergy(), "energy"
        print self.getLifeSpan(), "lifespan"
        
def crossover(mothercode, fathercode):
    # For each trait, choose randomly from mother or father.
    codes = [mothercode, fathercode]
    code = 0
    code += random.choice(codes) & VELOCITY_BITS
    code += random.choice(codes) & TURNING_BITS
    code += random.choice(codes) & MOXIE_BITS
    code += random.choice(codes) & SASS_BITS
    code += random.choice(codes) & ENERGY_BITS
    code += random.choice(codes) & LIFESPAN_BITS
    return code
    # Genetic Code controls genetic traits, including:
    # velocity, turn radius, moxie, sass, max energy, max lifetime
    # ?? sight radius?



def mutate(code):
    """ Flip a random bit. """
    return code ^ (1 << random.randint(0, 31))

def randomCode():
    return random.randint(0, (2**32) - 1)

if __name__ == "__main__":
    f = Agent(randomCode(), isMale=False)
    m = Agent(randomCode(), isMale=True)

    f.printStatus()
    m.printStatus()

    f.empregnateBy(m)
    a = f.giveBirth()
    a.printStatus()



