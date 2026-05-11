import pyxel
import random

class LuckyCats:
    def __init__(self, game):
        self.game = game
        self.bodycolor = 0
        self.eyes = 0
        self.hat = 0
        self.wearing = 0
        self.generate()
        self.hit = 0

        """ self.bodycolor = {
            "white": 0,
            "brown": 1,
            "purple": 2,
            "orange": 3,
            "black": 4,
            "cow": 5,
            "tri": 6,
        }
        self.eyes = {
            "normal": 0,
            "blue": 1,
            "yellow": 2,
            "yellowblack": 3,
            "oddeye": 4,
            "heart": 5,
            "vr": 6,
            "sunglasses": 7,
            "pitsviper": 8,
            "solanasunglasses": 9,
        }
        self.hat = {
            "none": 0,
            "solanacap": 1,
            "strawhat": 2,
            "tophat": 3,
            "flower": 4,
            "angelring": 5,
            "piratehat": 6,
            "crown": 7,
        }
        self.wearing = {
            "none": 0,
            "coin": 1,
            "koban": 2,
            "plain": 3,
            "bitcoin": 4,
            "solanacoin": 5,
            "redsuit": 6,
            "blacksuit": 7,
            "bluesuit": 8,
            "heart": 9,
        } """
    def generate(self):
        self.bodycolor = random.randint(0,6)
        self.eyes = random.randint(0,9)
        self.hat = random.randint(0,7)
        self.wearing = random.randint(0,9)

    def start(self):
        pass

    def update(self):
        pass

    def draw_back(self, x, y):
        pyxel.blt(x,y,0,0,136,24,24,colkey=0)

    def draw_face(self, x, y):
        #body
        pyxel.blt(x,y,1,0,0+(24*self.bodycolor),24,24,colkey=0)
        #eyes
        pyxel.blt(x,y+8,1,24,64+(8*self.eyes),24,8,colkey=0)
        #hat
        pyxel.blt(x,y,1,24,0+(8*self.hat),24,8,colkey=0)
        #wearing
        pyxel.blt(x,y+16,1,48,0+(8*self.wearing),24,8,colkey=0)

