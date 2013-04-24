import math, turtle


turt = turtle.Turtle()

def graph():
    scr = turtle.Screen()
    scr.delay(1)
    turt.speed(0)

    #render(10, .1, 100)
    render(50, .1, 100)
    #render(50, .1, 100)
    #render(100, .1, 100)

    scr.exitonclick()
    

def sigmoid(x, a, b):
    return b * 1 / (1 + math.exp(-x*a))


def render(r, a, b):
    turt.penup()
    turt.goto(-r, b - sigmoid(-r, a, b))
    turt.pendown()
    for x in range(-r, r):
        y = sigmoid(x, a, b)
        print x, ":", b - int(y)
        turt.goto(x, b - int(y))

graph()
