# напиши здесь код создания и управления картой
 
# напиши здесь код основного окна игры
from direct.showbase.ShowBase import ShowBase
from hero import *
import pickle
 
 
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()    #создаем карту
        #self.pos = -20,40,-15
        #self.block = self.land.addBlock(self.pos)
        base.camLens.setFov(90)
        x,y = self.land.loadLand("land.txt")
        self.hero = Hero((x//2,y//2,2), self.land)
 
 
class Mapmanager():
    def __init__(self):
        self.colors = [(0.5, 0.3, 0.0, 1),
                       (0.2, 0.2, 0.3, 1),
                       (0.5, 0.5, 0.2, 1),
                       (0.0, 0.6, 0.0, 1)]
 
    def addBlock(self, pos):
        self.block = loader.loadModel('block.egg')
        self.texture = loader.loadTexture('block.png')
        self.block.setTexture(self.texture)
        self.land = render.attachNewNode("Land")
        self.block.reparentTo(self.land)
        self.block.setScale(1)
        self.block.setPos(pos)
 
        self.color = self.getColor(pos[2])
        self.block.setColor(self.color)
 
        self.block.setTag("at", str(pos))
 
    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()
 
    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]
 
    def loadLand(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            y = 0
            for line in file:
                x = 0
                line = line.split()
                for el in line:
                    z = int(el)
                    for z0 in range(z+1):
                        self.addBlock((x,y,z0))
                    x += 1
                y += 1
        return x, y
 
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        print(blocks)
        if blocks:
            return False
        else:
            #print(blocks, 1)
            return True
 
    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))
 
    def findHighestEmpty(self, pos):
        x, y, z = pos
 
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)
 
    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)
                print(pos)
 
 
    def loadMap(self):
        #self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for i in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)
 
game = Game()
game.run()
