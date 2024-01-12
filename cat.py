import random, pygame
import time, math

class Cat:
    def __init__(self):
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.MAX_x = 1024
        self.MAX_y = 1024
        self.size = 0
        self.mode = "idle"
        self.doing = "none"
        self.idle_list = ["none","none2", "lay", "lay2", "lay3", "lay4", "behind"]
        self.go_list = ["walkslow", "walk", "walk", "run", "run"]
        self.food_found = False
        self.front = False
        self.back = False
        self.flip = False
        self.slide_end = False
        self.dragging = False
        self.tx = 0
        self.ty = 0
        self.jty = -5
        self.dx = 0
        self.dy = 0
        self.do_end = True
        self.act_change = True
        self.need_act = 100
        self.imgcropx = 0
        self.imgcropy = 0
        self.imgdx = 64
        self.imgdy = 64
    
    def acting(self):
        n = random.random()
        if self.dragging:
            self.mode = "idle"
            self.doing = "none"
            self.need_act = 1
        else:
            n = random.random()
            self.tx = max(0, min(self.tx, self.MAX_x - 100))
            self.ty = max(0, min(self.ty, self.MAX_y - 100))
            
            if self.need_act < 1:
                if self.do_end:
                    n = 1
                    self.need_act = random.randint(5, 60)
            else:
                self.need_act -= 1
            
            
            if self.mode == "idle":
                if n > 0.99:
                    self.need_act = random.randint(5, 60)
                    if random.random() > 0.94:
                        self.doing = random.choice(self.idle_list)
                        self.act_change = True
                        self.do_end = False
                    else:
                        self.mode = "move"
                        self.doing = "none"
                else:
                    if self.do_end:
                        if random.random() > 0.99:
                            self.doing = random.choice(self.idle_list)
                            self.act_change = True
                            self.do_end = False
                        elif random.random() > 0.95:
                            self.mode = "move"
                            self.doing = "none"

            elif self.mode == "move":
                if self.doing == "none":
                    self.slide_end = False
                    self.do_end = False
                    self.act_change = True
                    if random.random() > 0.5:
                        self.tx = self.x + random.randint(-200, 200)
                    else:
                        self.ty = self.y + random.randint(-200, 200)

                    self.tx = max(0, min(self.tx, self.MAX_x - 100))
                    self.ty = max(0, min(self.ty, self.MAX_y - 100))

                    if self.y - self.ty <= 0 and abs(self.x - self.tx) < 20:
                        self.front = True
                    elif self.y - self.ty > 0 and abs(self.x - self.tx) < 20:
                        self.back = True
                    else:
                        self.flip = self.x > self.tx

                    self.doing = random.choice(self.go_list)
                    if self.doing != "slide":
                        angle = math.atan2(self.ty - self.y, self.tx - self.x)
                        self.dx = int(4 * math.cos(angle))
                        self.dy = int(4 * math.sin(angle))

                elif self.doing == "run":
                    angle = math.atan2(self.ty - self.y, self.tx - self.x)
                    self.dx = int(4 * math.cos(angle))
                    self.dy = int(4 * math.sin(angle))
                    self.x += self.dx * 3
                    self.y += self.dy * 3
                # Walk 동작 처리
                elif self.doing == "walk":
                    angle = math.atan2(self.ty - self.y, self.tx - self.x)
                    self.dx = int(6 * math.cos(angle))
                    self.dy = int(6 * math.sin(angle))
                    self.x += self.dx*2
                    self.y += self.dy*2

                # Walkslow 동작 처리
                elif self.doing == "walkslow":
                    angle = math.atan2(self.ty - self.y, self.tx - self.x)
                    self.dx = int(6 * math.cos(angle))
                    self.dy = int(6 * math.sin(angle))
                    self.x += self.dx
                    self.y += self.dy

                # 도착 여부 체크
                if abs(self.tx - self.x) < 10 and abs(self.ty - self.y) < 10:
                    self.x = self.tx
                    self.y = self.ty
                    self.front = False
                    self.back = False
                    self.flip = False
                    self.mode = "idle"
                    self.do_end = True
                    self.doing = random.choice(self.idle_list)
                    self.slide_end = True


    def set_frame(self, xx, yy, tx):
        if self.act_change:
            self.do_end = False
            self.imgcropx = xx
            self.imgcropy = yy
            self.act_change = False
        else:
            self.imgcropx += 1
            if self.imgcropx > tx:
                if self.mode == "move":
                    self.imgcropx = xx
                else:
                    self.do_end = True
                    self.imgcropx = xx
    def update_frame(self):
        if self.mode == "idle":
            # idle 상태에 따른 setFrame 호출
            idle_actions = {
                "none": (3, 4, 3),
                "none2": (3, 6, 3),
                "lay": (0, 4, 2),
                "lay2": (0, 5, 2),
                "lay3": (0, 6, 2),
                "lay4": (0, 7, 2),
                "behind": (6, 5, 8),
            }
            if self.doing in idle_actions:
                self.set_frame(*idle_actions[self.doing])
        elif self.mode == "move":
            # move 상태에 따른 setFrame 호출
            if self.doing == "run":
                if self.back:
                    self.set_frame(6, 3, 8)
                elif self.front:
                    self.set_frame(6, 0, 8)
                else:
                    self.set_frame(6, 2, 8)
            else:
                if self.back:
                    self.set_frame(0, 3, 2)
                elif self.front:
                    self.set_frame(0, 0, 2)
                else:
                    self.set_frame(0, 2, 2)


