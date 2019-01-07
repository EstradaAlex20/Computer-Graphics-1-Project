from math3d import *
from Mesh import *
class Ship:
    mesh = None
    def __init__(self):
        if Ship.mesh == None:
            Ship.mesh = Mesh("ship1c.obj.mesh")
        self.x = 0
        self.y = 0
        self.z = 0
        self.pos = vec4(self.x,self.y,self.z,0)
        self.right = vec4(1,0,0,0)
        self.up = vec4(0,1,0,0)
        self.facing = vec4(0,0,1,0)
        self.angle = 0
        self.worldView = mat4.identity()
        self.worldView = self.worldView * translation3(vec3(self.x, self.y, self.z))

    def update(self, elapsed_ms):
        self.pos -= self.facing * 0.005
        temp = mat4(self.right.x, self.right.y, self.right.z, 0,
                    self.up.x, self.up.y, self.up.z, 0,
                    self.facing.x, self.facing.y, self.facing.z, 0,
                    0,0,0,1) * translation3(self.pos)
        self.worldView = temp



    def draw(self):
        Ship.mesh.draw(self.worldView)

    def turn(self, amt):
        M = axisRotation(self.up, amt)
        self.facing *= M
        self.right *= M

    def pitch(self, amt):
        M = axisRotation(self.right, amt)
        self.facing *= M
        self.up *= M

    def rotate(self, amt):
        M = axisRotation(self.facing, amt)
        self.right *= M
        self.up *= M