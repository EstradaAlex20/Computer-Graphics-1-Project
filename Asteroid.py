from math3d import *
from Mesh import *
import random

class Asteroid:
    mesh = None
    def __init__(self, pos):
        if Asteroid.mesh == None:
            Asteroid.mesh = Mesh("asteroid.obj.mesh")
        self.pos = pos
        self.right = vec4(1,0,0,0)
        self.up = vec4(0,1,0,0)
        self.facing = vec4(0,0,1,0)
        self.rotateVec = random.choice([self.up, self.facing, self.right])
        self.angle = 0.005
        self.translationVec = vec3(random.randint(-8,8),random.randint(-8,8),random.randint(-8,8))
        self.worldMatrix = mat4.identity()

    def update(self, elapsed_ms):
        self.worldMatrix = mat4.identity()  * scaling3(vec3(5,5,5)) * rotation3(self.rotateVec, self.angle) * translation3(self.translationVec)
        self.angle += 0.005

    def draw(self):
        Asteroid.mesh.draw(self.worldMatrix)
