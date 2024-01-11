import random, pygame
import time, math

class Pet:
    def __init__(self):
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.MAX_x = 1024
        self.MAX_y = 1024
        self.size = 0
        self.mode = "idle"
        self.doing = "standing"
        self.idle_list = ["none", "none2", "lay", "sit", "swing",
                          "standing", "sitting", "dancing", "behind"]
        self.go_list = ["walkslow", "walk", "walk", "slide", "slide"]
        self.is_jump = False
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
            
            if n > 1:
                self.jty = 4
                self.is_jump = True
                self.act_change = True
            
            if self.is_jump:
                if self.jty>-5:
                    self.y-=5 * self.jty
                    self.jty -= 1
                else:
                    self.is_Jump = False
                    self.act_change = True
            
            if self.mode == "idle":
                if n > 0.99:
                    self.need_act = random.randint(5, 60)
                    if random.random() > 0.9:
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
                        elif random.random() > 0.9:
                            self.mode = "move"
                            self.doing = "none"

            elif self.mode == "move":
                if self.doing == "none":
                    self.slide_end = False
                    self.do_end = False
                    self.act_change = True
                    if random.random() > 0.5:
                        self.tx = self.x + random.randint(-100, 100)
                        self.ty = self.y + random.randint(-50, 50)
                    else:
                        self.tx = self.x + random.randint(-150, 150)
                        self.ty = self.y + random.randint(-150, 150)

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
                elif self.doing == "slide":
                    self.x += (self.tx - self.x) // 8
                    self.y += (self.ty - self.y) // 8

                # Walk 동작 처리
                elif self.doing == "walk":
                    angle = math.atan2(self.ty - self.y, self.tx - self.x)
                    self.dx = int(4 * math.cos(angle))
                    self.dy = int(4 * math.sin(angle))
                    self.x += self.dx
                    self.y += self.dy

                # Walkslow 동작 처리
                elif self.doing == "walkslow":
                    angle = math.atan2(self.ty - self.y, self.tx - self.x)
                    self.dx = int(4 * math.cos(angle))
                    self.dy = int(4 * math.sin(angle))
                    self.x += self.dx // 2
                    self.y += self.dy // 2

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
                    if self.doing == "slide":
                        if not self.slide_end:
                            self.imgcropx = tx
                    else:
                        self.imgcropx = xx
                else:
                    self.do_end = True
                    self.imgcropx = xx
    def update_frame(self):
        if not self.dragging:
            if self.is_jump:
                self.set_frame(0, 9, 8)
            else:
                if self.mode == "idle":
                    # idle 상태에 따른 setFrame 호출
                    idle_actions = {
                        "none": (0, 8, 0),
                        "none2": (0, 8, 0),
                        "lay": (9, 0, 9),
                        "sit": (7, 8, 7),
                        "swing": (0, 3, 7),
                        "standing": (0, 8, 6),
                        "sitting": (7, 8, 14),
                        "dancing": (0, 6, 5),
                        "behind": (0, 7, 9),
                    }
                    if self.doing in idle_actions:
                        self.set_frame(*idle_actions[self.doing])
                elif self.mode == "move":
                    # move 상태에 따른 setFrame 호출
                    if self.doing == "slide":
                        self.set_frame(0, 1, 2)
                    else:
                        if self.back:
                            self.set_frame(0, 5, 5)
                        elif self.front:
                            self.set_frame(6, 5, 10)
                        else:
                            move_actions = {
                                "walk": (0, 0, 8),
                                "walkslow": (0, 4, 10),
                            }
                            if self.doing in move_actions:
                                self.set_frame(*move_actions[self.doing])
        else:
            # dragging 상태일 때 setFrame 호출
            self.set_frame(10, 0, 14)