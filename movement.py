class PaddleMovement:
    def __init__(self, simulator):
        self.simulator = simulator
        self.simulator.is_running = True
        self.simulator.left_key_pressed = False
        self.simulator.right_key_pressed = False
        self.simulator.up_key_pressed = False
        self.simulator.down_key_pressed = False

        self.blink_cooldown = 3000  # 3 วินาที
        self.blink_ready = True  # สถานะการบลิงค์พร้อมใช้งาน

    def move_left(self):
        if (self.simulator.my_paddle.location[0] - self.simulator.my_paddle.width / 2 - 10) > -self.simulator.canvas_width:
            self.simulator.my_paddle.set_location(
                [self.simulator.my_paddle.location[0] - 10, self.simulator.my_paddle.location[1]])

    def move_right(self):
        if (self.simulator.my_paddle.location[0] + self.simulator.my_paddle.width / 2 + 10) < self.simulator.canvas_width:
            self.simulator.my_paddle.set_location(
                [self.simulator.my_paddle.location[0] + 10, self.simulator.my_paddle.location[1]])

    def move_up(self):
        if (self.simulator.my_paddle.location[1] + self.simulator.my_paddle.height / 2 + 10) < self.simulator.canvas_height:
            self.simulator.my_paddle.set_location(
                [self.simulator.my_paddle.location[0], self.simulator.my_paddle.location[1] + 10])

    def move_down(self):
        if (self.simulator.my_paddle.location[1] - self.simulator.my_paddle.height / 2 - 10) > -self.simulator.canvas_height:
            self.simulator.my_paddle.set_location(
                [self.simulator.my_paddle.location[0], self.simulator.my_paddle.location[1] - 10])

    def move_continuous(self):
        if self.simulator.is_running:
            if self.simulator.left_key_pressed:
                self.move_left()
            if self.simulator.right_key_pressed:
                self.move_right()
            if self.simulator.up_key_pressed:
                self.move_up()
            if self.simulator.down_key_pressed:
                self.move_down()
            self.simulator.screen.ontimer(self.move_continuous, 20)

    def start_move_left(self):
        self.simulator.left_key_pressed = True

    def start_move_right(self):
        self.simulator.right_key_pressed = True

    def start_move_up(self):
        self.simulator.up_key_pressed = True

    def start_move_down(self):
        self.simulator.down_key_pressed = True

    def stop_move_left(self):
        self.simulator.left_key_pressed = False

    def stop_move_right(self):
        self.simulator.right_key_pressed = False

    def stop_move_up(self):
        self.simulator.up_key_pressed = False

    def stop_move_down(self):
        self.simulator.down_key_pressed = False

    def blink_blade(self):
        if not self.blink_ready:
            return  # ถ้ายังไม่พร้อมบลิงค์ ให้หยุดทำงาน

        self.blink_ready = False  # เปลี่ยนสถานะเป็น "ไม่พร้อม"
        self.simulator.my_paddle.color = (0, 0, 0)  # เปลี่ยนสีเป็นสีดำ (แสดงว่ายังไม่พร้อม)

        blink_distance = 100
        new_x = self.simulator.my_paddle.location[0]
        new_y = self.simulator.my_paddle.location[1]

        # คำนวณตำแหน่งใหม่
        if self.simulator.left_key_pressed:
            new_x -= blink_distance
        if self.simulator.right_key_pressed:
            new_x += blink_distance
        if self.simulator.up_key_pressed:
            new_y += blink_distance
        if self.simulator.down_key_pressed:
            new_y -= blink_distance

        # ตรวจสอบขอบเขต
        new_x = max(-self.simulator.canvas_width + self.simulator.my_paddle.width / 2,
                    min(self.simulator.canvas_width - self.simulator.my_paddle.width / 2, new_x))
        new_y = max(-self.simulator.canvas_height + self.simulator.my_paddle.height / 2,
                    min(self.simulator.canvas_height - self.simulator.my_paddle.height / 2, new_y))

        # อัปเดตตำแหน่งใหม่
        self.simulator.my_paddle.set_location([new_x, new_y])

        # ตั้งเวลาให้กลับมาพร้อมใช้งานหลังคูลดาวน์เสร็จ
        self.simulator.screen.ontimer(self.reset_blink, self.blink_cooldown)

    def reset_blink(self):
        self.blink_ready = True  # บลิงค์พร้อมใช้งานอีกครั้ง
        self.simulator.my_paddle.color = (128, 128, 128)  # เปลี่ยนสีกลับเป็นสีเทา (พร้อมใช้งาน)
