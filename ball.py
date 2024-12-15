import random
import math
import turtle

class Ball:
    def __init__(self, size, x, y, vx, vy, color, id):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = 100 * size ** 2
        self.count = 0  # Count the number of bounces
        self.id = id
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        self.stage = 1  # Start at stage 1

        # Maximum allowed speed (cap speed)
        self.max_speed = 10

        # Initialize color and speed based on initial stage
        self.update_stage()

    def update_stage(self):
        """Update the speed and color based on the current stage"""
        if self.stage == 1:
            self.color = (255, 255, 0)  # YELLOW
            self.vx = 1.5
            self.vy = 1.5
        elif self.stage == 2:
            self.color = (236, 83, 0)  # ORANGE
            self.vx = 2
            self.vy = 2
        elif self.stage == 3:
            self.color = (255, 0, 0)  # Red
            self.vx = 4
            self.vy = 4


    def draw(self):
        """Draw the ball on the screen"""
        turtle.penup()
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.goto(self.x, self.y - self.size)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()

    def bounce_off_vertical_wall(self):
        """Bounce off a vertical wall and increment bounce count"""
        self.vx = -self.vx
        self.count += 1
        self.size =random.uniform(0.01,0.06) * self.canvas_width
        if self.count >= 5:
            self.stage += 1
            self.count = 0  # Reset bounce count after advancing stage
            self.update_stage()  # Update color and speed based on new stage

        print(
            f"Ball {self.id} bounced off vertical wall. Current stage: {self.stage}, Current count: {self.count}")
    def bounce_off_horizontal_wall(self):
        """Bounce off a horizontal wall and increment bounce count"""
        self.vy = -self.vy
        self.count += 1
        if self.count >= 5:
            self.stage += 1
            self.count = 0  # Reset bounce count after advancing stage
            self.update_stage()  # Update color and speed based on new stage
        print(
            f"Ball {self.id} bounced off horizontal wall. Current stage: {self.stage}, Current count: {self.count}")

    def bounce_off(self, that):
        """Bounce off another ball and increment bounce count"""
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy  # dv dot dr
        dist = self.size + that.size   # Distance between particle centers at collision

        # Magnitude of normal force
        magnitude = 2 * self.mass * that.mass * dvdr / ((self.mass + that.mass) * dist)

        # Normal force, and in x and y directions
        fx = magnitude * dx / dist
        fy = magnitude * dy / dist

        # Update velocities according to normal force
        self.vx += fx / self.mass
        self.vy += fy / self.mass
        that.vx -= fx / that.mass
        that.vy -= fy / that.mass

        # Update collision counts
        self.count += 1
        that.count += 1

        if self.count >= 5:
            self.stage += 1
            self.count = 0  # Reset bounce count after advancing stage
            self.update_stage()  # Update color and speed based on new stage

    def distance(self, that):
        """Calculate the distance between this ball and another ball"""
        return math.sqrt((that.x - self.x) ** 2 + (that.y - self.y) ** 2)

    def move(self, dt):
        """Move the ball according to its velocity"""
        self.x += self.vx * dt
        self.y += self.vy * dt

    # Time-to-hit methods
    def time_to_hit(self, that):
        if self is that:
            return math.inf
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy
        if dvdr > 0:
            return math.inf
        dvdv = dvx * dvx + dvy * dvy
        if dvdv == 0:
            return math.inf
        drdr = dx * dx + dy * dy
        sigma = self.size + that.size
        d = (dvdr * dvdr) - dvdv * (drdr - sigma * sigma)
        if d < 0:
            return math.inf
        t = -(dvdr + math.sqrt(d)) / dvdv

        if t <= 0:
            return math.inf

        return t

    def time_to_hit_vertical_wall(self):
        if self.vx > 0:
            return (self.canvas_width - self.x - self.size) / self.vx
        elif self.vx < 0:
            return (self.canvas_width + self.x - self.size) / (-self.vx)
        else:
            return math.inf

    def time_to_hit_horizontal_wall(self):
        if self.vy > 0:
            return (self.canvas_height - self.y - self.size) / self.vy
        elif self.vy < 0:
            return (self.canvas_height + self.y - self.size) / (-self.vy)
        else:
            return math.inf

    def time_to_hit_paddle(self, paddle):
        if (self.vy > 0) and ((self.y + self.size) > (paddle.location[1] - paddle.height/2)):
            return math.inf
        if (self.vy < 0) and ((self.y - self.size) < (paddle.location[1] + paddle.height/2)):
            return math.inf

        dt = (math.sqrt((paddle.location[1] - self.y)**2) - self.size - paddle.height/2) / abs(self.vy)
        paddle_left_edge = paddle.location[0] - paddle.width/2
        paddle_right_edge = paddle.location[0] + paddle.width/2
        if paddle_left_edge - self.size <= self.x + (self.vx*dt) <= paddle_right_edge + self.size:
            return dt
        else:
            return math.inf

    def bounce_off_paddle(self,paddle):
        self.vy = -self.vy
        self.vx = -self.vx
        print("################CHECK###############")
        paddle.flash_red()
        self.count += 1
        if self.count >= 5:
            self.stage += 1
            self.count = 0  # Reset bounce count after advancing stage
            self.update_stage()  # Update color and speed based on new stage

    def __str__(self):
        return f"Ball {self.id}: x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy}, stage={self.stage}, color={self.color}"

