import random
from Program import *
from math3d import *
import math
from Mesh import *

class Enemy:
    def __init__(self, radius):
        self.radius = radius
        self.x = 512*3.5 / 512
        self.y = random.uniform(-1,1)
        self.z =  10
        self.vao = None
        self.tex = None
        self.samp = None
        self.speed = 0.0009
        self.state = "ALIVE"
        self.deathTimer = 1000
        self.pos = vec3(self.x, self.y, 0)
        self.angle = 1
        self.worldMatrix = mat4.identity() * translation3(vec3(self.x, self.y, self.z))
        self.scale = 1

    def update(self, elapsed):

        self.x -= self.speed * elapsed
        self.worldMatrix = mat4.identity() * translation3(vec3(self.x, self.y, self.z))
        if self.state == "DYING":
            self.y -= 0.005
            self.scale -= 0.005
            #self.worldMatrix = mat4.identity()
            #self.worldMatrix *= translation3(vec3(self.x, self.y, self.z))
            self.worldMatrix *= rotation3(vec3(0, 0, 1), math.radians(self.angle))
            self.worldMatrix *= mat4(self.scale,0,0,0,
                                     0,self.scale,0,0,
                                     0,0,self.scale,0,
                                     0,0,0,1)

            #self.worldMatrix *= rotation3(vec3(0, 0, 1), math.radians(self.angle))
            #self.M *= mat3(1,0,0,0,1,0,self.x,self.y,1)
            self.deathTimer -= elapsed
        if self.deathTimer <= 0:
            self.state = "DEAD"

    def draw(self):
        self.angle += 10
        #M = mat3(math.cos(math.radians(self.angle)),math.sin(math.radians(self.angle)),0,-math.sin(math.radians(self.angle)),math.cos(math.radians(self.angle)),0,0,0,1)
        #M *= mat3(1,0,0,0,1,0,self.x,self.y,1)
        Program.setUniform("worldMatrix", self.worldMatrix)
        Program.setUniform("enemyAlpha", self.deathTimer/1000)
        Program.updateUniforms()
        #glBindVertexArray(vao)


class StraightEnemy(Enemy):
    mesh = None
    def __init__(self, radius=0.1):
        if StraightEnemy.mesh == None:
            StraightEnemy.mesh = Mesh("ship2b.obj.mesh")
        super().__init__(radius)

    def update(self, elapsed):
        super().update(elapsed)

    def draw(self):
        Program.setUniform("enemyAlpha", self.deathTimer/1000)
        Program.updateUniforms()
        StraightEnemy.mesh.draw(self.worldMatrix)
        #self.vao = vao
        #self.tex = tex
        #super().draw(vao, tex)


class HappyEnemy(Enemy):
    mesh = None
    def __init__(self, radius=0.1):
        if HappyEnemy.mesh == None:
            HappyEnemy.mesh = Mesh("jellyfish.obj.mesh")
        super().__init__(radius)
        self.waveSpeed = random.randint(5,15)

    def update(self, elapsed):
        self.y -= math.sin(self.x * self.waveSpeed) * self.speed * elapsed
        super().update(elapsed)

    def draw(self):
        Program.setUniform("enemyAlpha", self.deathTimer/1000)
        Program.updateUniforms()
        HappyEnemy.mesh.draw(self.worldMatrix)
        #self.vao = vao
        #self.tex = tex
        #super().draw(vao, tex)



