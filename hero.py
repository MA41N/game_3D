key_switch_camera = 'c'  # камера привязана к герою или нет
key_switch_mode = 'z'  # можно проходить сквозь препятствия или нет

key_forward = 's'  # шаг вперёд (куда смотрит камера)
key_back = 'w'  # шаг назад
key_left = 'd'  # шаг влево (вбок от камеры)
key_right = 'a'  # шаг вправо
key_up = 'space'  # шаг вверх
key_down = 'g'  # шаг вниз

key_turn_left = 'q'  # поворот камеры направо (а мира - налево)
key_turn_right = 'e'  # поворот камеры налево (а мира - направо)

key_build = 'b'  # построить блок перед собой
key_destroy = 'v'  # разрушить блок перед собой


class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True  # режим прохождения сквозь всё
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setH(180)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
 
 
    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True
 
 
    def cameraUp(self):
        pos = self.hero.getPos()
 
        base.mouseInterfaceNode.setPos((pos[0]-9,pos[1]-5,pos[2]-6))
        base.mouseInterfaceNode.setH(180)
        base.camera.reparentTo(self.hero)
 
        base.enableMouse()
        self.cameraOn = False
 
 
    def accept_events(self):
        base.accept('c', self.changeView)
 
        base.accept('q', self.turn_left)
        base.accept('q'+ '-repeat', self.turn_left)
        base.accept('e', self.turn_right)
        base.accept('e' + '-repeat', self.turn_right)
 
        base.accept('w', self.forward)
        base.accept('w' + '-repeat', self.forward)
        base.accept('a', self.left)
        base.accept('a' + '-repeat', self.left)
        base.accept('d', self.right)
        base.accept('d' + '-repeat', self.right)
        base.accept('s', self.back)
        base.accept('s' + '-repeat', self.back)
 
        base.accept('space', self.up)
        base.accept('space'+'-repeat', self.up)
 
        base.accept('v', self.down)
        base.accept('v' + '-repeat', self.down)
 
        base.accept('z', self.changeMode)
 
        base.accept('p', self.build)
        base.accept('o', self.destroy)
 
        base.accept('k', self.land.saveMap)
        base.accept('l', self.land.loadMap)
 
 
    def changeMode(self):
        if self.mode == True:
            self.mode = False
        else:
            self.mode = True
 
 
    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
            #self.mode = False
        else:
            self.cameraBind()
            #self.mode = True
 
 
    def turn_left(self):
        a = self.hero.getH()
        a += 5
        self.hero.setH(a % 360)
 
 
    def turn_right(self):
        a = self.hero.getH()
        a -= 5
        self.hero.setH(a % 360)
 
 
    def just_move(self, angle):
        pos = self.look_at(angle)
        print(pos)
        self.hero.setPos(pos)
 
 
    def try_move(self, angle):
        pos = self.look_at(angle)
        print(pos)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            print(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            print(pos)
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
 
 
    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())
 
        dx, dy = self.check_dir(angle)
 
        return from_x + dx, from_y + dy, from_z
 
    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return 0, -1
        elif angle > 20 and angle <= 65:
            return 1, -1
        elif angle > 65 and angle <= 110:
            return 1, 0
        elif angle > 110 and angle <= 155:
            return 1, 1
        elif angle > 155 and angle <= 200:
            return 0, 1
        elif angle > 200 and angle <= 245:
            return -1, 1
        elif angle > 245 and angle <= 290:
            return -1, 0
        elif angle > 290 and angle <= 335:
            return -1, -1
        elif angle > 335 and angle <= 360:
            return 0, -1
 
 
    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)
 
    def forward(self):
        angle = (self.hero.getH() + 0) % 360
        print(angle)
        self.move_to(angle)
 
 
    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)
 
 
    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)
 
 
    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)
 
 
    def up(self):
        self.hero.setZ(self.hero.getZ() + 1)
 
 
 
    def down(self):
        self.hero.setZ(self.hero.getZ() - 1)
 
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)
 
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)