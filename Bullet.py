import random
from math3d import *
from Mesh import *

class Bullet:
    mesh = None
    def __init__(self, ship):
        if Bullet.mesh == None:
            Bullet.mesh = Mesh("bullet.obj.mesh")
        self.lifetime=1500
        self.pos = ship.pos
        self.right = ship.right
        self.up = ship.up
        self.facing = ship.facing
        self.speed = 0.00005
        self.distance = 0
        self.worldView = ship.worldView

    def update(self, elapsed_ms, ship):
        self.lifetime -= elapsed_ms
        self.pos -= self.facing * 0.05
        temp = mat4(self.right.x, self.right.y, self.right.z, 0,
                    self.up.x, self.up.y, self.up.z, 0,
                    self.facing.x, self.facing.y, self.facing.z, 0,
                    0,0,0,1) * translation3(self.pos)
        self.worldView = temp


    def draw(self):
        Bullet.mesh.draw(self.worldView)
