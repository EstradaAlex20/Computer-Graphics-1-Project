from math3d import *
import math
from Camera import *
import random

class PowerUp(object):
    def __init__(self):
        self.world_x = random.uniform(0,2.5)
        self.world_y = random.uniform(-1,1)
        self.worldMatrix = mat3.identity() * translation2(vec2(self.world_x, self.world_y))
        self.count = 0
        self.state = "ALIVE"
        self.deathtimer = 5000

    def update(self, elapsed_ms):
        self.count += elapsed_ms
        if self.state == "DYING":
            #self.worldMatrix *= rotation2(0.05)
            if self.worldMatrix[0][0] > 0:
                self.worldMatrix[0][0] -= 0.005
            if self.worldMatrix[1][1] > 0:
                self.worldMatrix[1][1] -= 0.005
            self.deathtimer -= elapsed_ms
        else:
            self.worldMatrix[0][0] += 0.05*math.sin(math.radians(self.count))
            self.worldMatrix[1][1] += 0.05 * math.sin(math.radians(self.count))
        #self.worldMatrix += scaling2(vec2(math.sin(math.radians(self.count)),math.sin(math.radians(self.count))))
        if self.deathtimer < 0:
            self.state="DEAD"

    def viewCoords(self, camera):
        p = vec3(0,0,1)
        p *= self.worldMatrix
        p *= camera.viewMatrix
        return vec2(p[0],p[1])

class Star(object):
    def __init__(self):
        self.x = random.uniform(-1,3)
        self.y = random.uniform(-1,1)
        self.z = 500
        self.worldMatrix = mat4.identity() * translation3(vec3(self.x, self.y, self.z))