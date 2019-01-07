from math3d import *
from Program import *
import math

class Camera:
    def __init__(self, coi, eye, up):
        self.lookAt(coi, eye, up)
        self.horzAngle = math.radians(45)
        self.vertAngle = math.radians(45)
        self.hither = 0.1
        self.yon = 1000
        self.updateProjectionMatrix()
        #print(self.projMatrix)

    def lookAt(self, coi, up, eye):
        self.eye = eye.xyz
        self.coi = coi.xyz
        self.look = normalize(coi.xyz - self.eye)
        self.right = normalize(cross(self.look, up))
        self.up = cross(self.right, self.look)
        self.updateViewMatrix()

    def updateViewMatrix(self):
        self.viewMatrix = mat4(
            self.right.x, self.up.x, -self.look.x, 0,
            self.right.y, self.up.y, -self.look.y, 0,
            self.right.z, self.up.z, -self.look.z, 0,
            -dot(self.eye, self.right), -dot(self.eye, self.up), dot(self.eye, self.look), 1
        )


    def updateProjectionMatrix(self):
        self.projMatrix = mat4(
            1/math.tan(self.horzAngle),0,0,0,
            0,1/math.tan(self.vertAngle),0,0,
            0,0,1 + (2*self.yon) / (self.hither-self.yon),-1,
            0,0,(2*self.hither*self.yon)/(self.hither - self.yon),0
        )

    def setUniforms(self):
        #assuming shader does p * M and not M * p
        Program.setUniform("viewMatrix", self.viewMatrix)
        Program.setUniform("projMatrix", self.projMatrix)
        Program.setUniform("eyePos", self.eye.xyz)


    def tilt(self, amt):
        M = rotation2(amt)
        self.right = self.right * M
        self.up = self.up * M
        self.updateViewMatrix()

    def pan(self, dx, dy):
        self.coi.x += dx
        self.coi.y += dy
        self.updateViewMatrix()

    def walk(self, amt):
        self.strafe(0,0,amt)

    def strafe(self, dx, dy, dz):
        self.eye += dx * self.right + dy * self.up + dz * self.look
        self.updateViewMatrix()


    def turn(self, amt):
        pass
        #M = axisRotation((0,1,0), amt)
        #self.right = self.right * M
        #self.look = self.look * M
        #self.up = self.up * M

    def roll(self, amt):
        pass

    def pitch(self, amt):
        pass