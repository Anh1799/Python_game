
import turtle
import random
import time

screen = turtle.Screen()
screen.title("Snake Game 🐍")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

head = turtle.Turtle()
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(100, 100)

segments = []
score = 0

pen = turtle.Turtle()
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

def show_score():
    pen.clear()
    pen.write(f"Score: {score}", align="center",
              font=("Arial", 20, "bold"))

show_score()

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    x = head.xcor()
    y = head.ycor()

    if head.direction == "up":
        head.sety(y + 20)
    elif head.direction == "down":
        head.sety(y - 20)
    elif head.direction == "left":
        head.setx(x - 20)
    elif head.direction == "right":
        head.setx(x + 20)

screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

def reset_game():
    global score

    time.sleep(0.5)
    head.goto(0, 0)
    head.direction = "stop"

    for segment in segments:
        segment.hideturtle()

    segments.clear()
    score = 0
    show_score()

while True:
    screen.update()

    if abs(head.xcor()) >= 290 or abs(head.ycor()) >= 290:
        reset_game()

    if head.distance(food) < 20:
        food.goto(
            random.randrange(-13, 14) * 20,
            random.randrange(-13, 13) * 20
        )

        segment = turtle.Turtle()
        segment.shape("square")
        segment.color("green")
        segment.penup()
        segments.append(segment)

        score += 10
        show_score()

    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    for segment in segments:
        if segment.distance(head) < 10:
            reset_game()
            break

    time.sleep(0.1)
