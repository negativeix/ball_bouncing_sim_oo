import copy
import random
import turtle
import heapq
import paddle
import ball
import my_event
import math
from movement import PaddleMovement

class BouncingSimulator:
    def __init__(self, num_balls):
        self.num_balls = num_balls
        self.ball_list = []
        self.t = 0.0
        self.pq = []
        self.HZ = 4
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)

        # Initial ball radius based on canvas size
        self.ball_radius = 0.05 * self.canvas_width

        # Create the initial balls

        x = -self.canvas_width + (len(self.ball_list) + 1) * (
                    2 * self.canvas_width / (self.num_balls + 1))
        y = self.canvas_height
        vx = 10 * random.uniform(-1.0, 1.0)
        vy = 10 * random.uniform(-1.0, 1.0)
        ball_color = (random.randint(0, 255), random.randint(0, 255),
                      random.randint(0, 255))
        id = len(self.ball_list)
        self.ball_list.append(
            ball.Ball(self.ball_radius, x, y, vx, vy, ball_color, id))

        # Create the paddle
        tom = turtle.Turtle()
        self.my_paddle = paddle.Paddle(30, 30, (128, 128, 128), tom)
        self.my_paddle.set_location([0, 0])

        self.screen = turtle.Screen()

        # Initializing game level and ball increment
        self.level = 1
        self.max_level = 5  # Set max level, after which no more balls will be added
        self.stage_ball_count = 1  # Starting with 1 ball

        self.paddle_movement = PaddleMovement(self)
    def add_new_ball(self):
        x = -self.canvas_width + (len(self.ball_list) + 1) * (
                2 * self.canvas_width / (self.num_balls + 1))
        y = self.canvas_height
        vx = 10 * random.uniform(-1.0, 1.0)
        vy = 10 * random.uniform(-1.0, 1.0)
        ball_color = (random.randint(0, 255), random.randint(0, 255),
                      random.randint(0, 255))
        id = len(self.ball_list)

        self.ball_list.append(
            ball.Ball(self.ball_radius, x, y, vx, vy, ball_color, id))

    # updates priority queue with all new events for a_ball
    def __predict(self, a_ball):
        if a_ball is None:
            return

        # particle-particle collisions
        for i in range(len(self.ball_list)):
            dt = a_ball.time_to_hit(self.ball_list[i])
            heapq.heappush(self.pq, my_event.Event(self.t + dt, a_ball,
                                                   self.ball_list[i], None))

        # particle-wall collisions
        dtX = a_ball.time_to_hit_vertical_wall()
        dtY = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self.pq,
                       my_event.Event(self.t + dtX, a_ball, None, None))
        heapq.heappush(self.pq,
                       my_event.Event(self.t + dtY, None, a_ball, None))

    def __draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color((0, 0, 0))
        for i in range(2):
            turtle.forward(2 * self.canvas_width)
            turtle.left(90)
            turtle.forward(2 * self.canvas_height)
            turtle.left(90)
    def __draw_level(self):
        # Display the level on the screen
        turtle.penup()
        turtle.goto(-self.canvas_width + 20, self.canvas_height - 40)
        turtle.pendown()
        turtle.color((0, 0, 0))
        turtle.write(f"Level: {self.level}", font=("Arial", 16, "bold"))

    def __redraw(self):
        turtle.clear()
        self.my_paddle.clear()
        self.__draw_border()
        self.__draw_level()
        self.my_paddle.draw()
        for i in range(len(self.ball_list)):
            self.ball_list[i].draw()
        turtle.update()
        heapq.heappush(self.pq,
                       my_event.Event(self.t + 1.0 / self.HZ, None, None,
                                      None))

    def __paddle_predict(self):
        for ball in self.ball_list:
            dtP = ball.time_to_hit_paddle(self.my_paddle)
            if dtP != float('inf'):
                heapq.heappush(self.pq,
                               my_event.Event(self.t + dtP, ball, None,
                                              self.my_paddle))

    # Update level and add more balls if necessary
    def check_level_up(self):
        # Check if all balls are at stage 4
        all_stage_4 = True
        for ball in self.ball_list:
            if ball.stage < 4:
                all_stage_4 = False
                break

        if all_stage_4:
            # If all balls are at stage 4, reset all balls to stage 0 and add a new ball
            print("All balls reached stage 4. Resetting all balls to stage 0 and adding a new ball.")
            for ball in self.ball_list:
                ball.stage = 0  # Reset stage for all balls

            if self.level < self.max_level:  #check level up
                self.level += 1
                self.stage_ball_count += 1
                print(
                    f"Level {self.level}: Checking if balls reach stage 4 to add a new ball.")
                print('here')
                self.add_new_ball()
                self.__predict(self.ball_list[-1])

                self.stage_ball_count = 1  # Start with 1 new ball

                print(f"Added a new ball: Level {self.level}.")

    def run(self):
        # Initialize priority queue with collision events and redraw event
        for i in range(len(self.ball_list)):
            self.__predict(self.ball_list[i])
        heapq.heappush(self.pq, my_event.Event(0, None, None, None))

        # Bind key press and release events
        self.screen.listen()
        self.screen.onkeypress(self.paddle_movement.start_move_left, "Left")
        self.screen.onkeypress(self.paddle_movement.start_move_right, "Right")
        self.screen.onkeypress(self.paddle_movement.start_move_up, "Up")
        self.screen.onkeypress(self.paddle_movement.start_move_down, "Down")

        self.screen.onkeyrelease(self.paddle_movement.stop_move_left, "Left")
        self.screen.onkeyrelease(self.paddle_movement.stop_move_right, "Right")
        self.screen.onkeyrelease(self.paddle_movement.stop_move_up, "Up")
        self.screen.onkeyrelease(self.paddle_movement.stop_move_down, "Down")

        self.screen.onkeypress(self.paddle_movement.blink_blade, "space")

        # Start the continuous paddle movement loop
        self.paddle_movement.move_continuous()

        while True:
            e = heapq.heappop(self.pq)
            if not e.is_valid():
                continue

            ball_a = e.a
            ball_b = e.b
            paddle_a = e.paddle

            # update positions, and then simulation clock
            for ball in self.ball_list:
                ball.move(e.time - self.t)
            self.t = e.time

            # Handle events
            if (ball_a is not None) and (ball_b is not None) and (
                    paddle_a is None):
                # Ball-ball collision
                ball_a.bounce_off(ball_b)
            elif (ball_a is not None) and (ball_b is None) and (
                    paddle_a is None):
                # Ball hits vertical wall
                ball_a.bounce_off_vertical_wall()
            elif (ball_a is None) and (ball_b is not None) and (
                    paddle_a is None):
                # Ball hits horizontal wall
                ball_b.bounce_off_horizontal_wall()
            elif (ball_a is None) and (ball_b is None) and (paddle_a is None):
                # Redraw event
                self.__redraw()
            elif (ball_a is not None) and (ball_b is None) and (
                    paddle_a is not None):
                # Ball hits paddle
                ball_a.bounce_off_paddle(paddle_a)

            # Check if the level should be increased
            self.check_level_up()

            # Recalculate future events
            self.__predict(ball_a)
            self.__predict(ball_b)

            # Regularly update paddle predictions
            self.__paddle_predict()


# num_balls = int(input("Number of balls to simulate: "))
num_balls = 1
my_simulator = BouncingSimulator(num_balls)
my_simulator.run()
