class Paddle:
    def __init__(self, width, height, color, my_turtle):
        self.width = width
        self.height = height
        self.location = [0, 0]
        self.color = color
        self.original_color = color
        self.my_turtle = my_turtle
        self.my_turtle.penup()
        self.my_turtle.setheading(0)
        self.my_turtle.hideturtle()


    def set_location(self, location):
        self.location = location
        self.my_turtle.goto(self.location[0], self.location[1])

    def draw(self):
        margin = 2.5  # ความกว้างของขอบ

        # วาดขอบ (สีขอบ)
        border_color = (0,0,0)  # สีของขอบ
        self.my_turtle.color(border_color)
        self.my_turtle.penup()
        self.my_turtle.goto(self.location[0] - self.width / 2,
                            self.location[1] - self.height / 2)  # มุมซ้ายล่าง
        self.my_turtle.pendown()
        self.my_turtle.begin_fill()
        for _ in range(2):
            self.my_turtle.forward(self.width)
            self.my_turtle.left(90)
            self.my_turtle.forward(self.height)
            self.my_turtle.left(90)
        self.my_turtle.end_fill()
        self.my_turtle.penup()

        # วาด paddle จริง (พื้นที่ภายใน)
        self.my_turtle.color(self.color)
        inner_width = self.width - 2 * margin
        inner_height = self.height - 2 * margin
        self.my_turtle.goto(
            self.location[0] - inner_width / 2,
            self.location[1] - inner_height / 2
        )  # มุมซ้ายล่างของ paddle จริง
        self.my_turtle.pendown()
        self.my_turtle.begin_fill()
        for _ in range(2):
            self.my_turtle.forward(inner_width)
            self.my_turtle.left(90)
            self.my_turtle.forward(inner_height)
            self.my_turtle.left(90)
        self.my_turtle.end_fill()
        self.my_turtle.penup()

        # กลับไปที่ตำแหน่งศูนย์กลางของ paddle
        self.my_turtle.goto(self.location[0], self.location[1])

    def clear(self):
        self.my_turtle.clear()

    def __str__(self):
        return "paddle"
