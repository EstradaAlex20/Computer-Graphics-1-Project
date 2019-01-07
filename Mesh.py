from ctypes import *
from sdl2 import *
from sdl2.keycode import *
from gl import *
from glconstants import *
import array
from Buffer import *
from Program import *
import random
import math
import traceback
import array
import os
from sdl2.sdlmixer import *
import os.path
from math3d import *
from Texture import *
from Sampler import *
from obj2mesh import *


class Mesh:
    def __init__(self, fname):
        self.materials = []
        self.world_x = 2.5
        self.world_y = 0
        self.world_z = -1
        self.dx = 0.0005
        self.dy = 0.0003
        self.worldMatrix = mat4.identity() * translation3(vec3(self.world_x, self.world_y, self.world_z))
        fname = os.path.join("assets", fname)
        with open(fname, "rb") as fp:
            line = fp.readline()
            if line != b"mesh 0\n":
                raise RuntimeError("bad mesh format: " + fname)
            line = fp.readline()
            if not line.startswith(b"num_materials"):
                raise RuntimeError("bad mesh format: " + fname)
            line = line.decode()
            lst = line.split()
            nm = int(lst[1])
            for i in range(nm):
                self.readAMaterial(fp)
            pbuff = self.readBlob(fp, "position")
            tbuff = self.readBlob(fp, "texcoord")
            nbuff = self.readBlob(fp, "normal")
            ibuff = self.readBlob(fp, "Indicies")
            line = fp.readline()
            assert line == b"end\n"
            self.setup(pbuff, tbuff, nbuff, ibuff)


    def readAMaterial(self, fp):
        line = fp.readline().decode()
        line = fp.readline().decode()
        assert line.startswith("kd")
        lst = line.split()
        lst = [float(q) for q in lst[1:4]]
        kd = vec3(*lst)
        line = fp.readline().decode()
        assert line.startswith("ks")
        lst = line.split()
        lst = [float(q) for q in lst[1:4]]
        ks = vec3(*lst)
        line = fp.readline().decode()
        assert line.startswith("ns")
        tmp = line.split()
        tmp = float(tmp[1])
        ns = tmp
        line = fp.readline().decode()
        if line.startswith("map_kd"):
            lst = line.split(" ", 1)
            mapkd = lst[1].strip()
            line = fp.readline().decode()
        else:
            mapkd = None

        assert line.startswith("first")
        lst = line.split(" ")
        first = int(lst[3])
        count = int(lst[4])
        #line = fp.readline().decode()
        #assert line.startswith("position")
        #lst = line.split(" ")
        #position = int(lst[1])

        M = Material()
        M.kd = kd
        if mapkd == None:
            mapkd = ("white.png")
        M.map_kd = mapkd
        M.first = first
        M.count = count
        M.tex = ImageTexture2DArray(mapkd)
        M.ns = ns
        M.ks = ks
        self.materials.append(M)




    def readBlob(self, fp, name):
        line = fp.readline().decode()
        assert line.startswith(name)
        lst = line.split()
        numbytes = int(lst[1])
        blob = fp.read(numbytes)
        fp.readline()
        B = Buffer(blob)
        return B

    def setup(self, pbuff, tbuff, nbuff, ibuff):
        tmp = array.array("I", [0])
        glGenVertexArrays(1,tmp)
        self.vao = tmp[0]
        glBindVertexArray(self.vao)
        ibuff.bind(GL_ELEMENT_ARRAY_BUFFER)
        pbuff.bind(GL_ARRAY_BUFFER)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT, False, 3*4, 0)
        tbuff.bind(GL_ARRAY_BUFFER)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,2,GL_FLOAT, False, 2*4, 0)
        nbuff.bind(GL_ARRAY_BUFFER)
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, False, 3 * 4, 0)
        glBindVertexArray(0)

    def draw(self, worldMatrix):
        glBindVertexArray(self.vao)
        for m in self.materials:
            m.tex.bind(0)
            Program.setUniform("diffuse", m.kd)
            Program.setUniform("worldMatrix", worldMatrix)
            Program.setUniform("specular", m.ks)
            Program.setUniform("shininess", m.ns)
            Program.updateUniforms()
            glDrawElements(GL_TRIANGLES, m.count, GL_UNSIGNED_INT, m.first)
        Program.setUniform("diffuse", vec3(1,1,1))

    def update(self, elapsedMS):
        self.world_x += self.dx * elapsedMS
        self.world_y += self.dy * elapsedMS
        if self.world_x > 3 or self.world_x < 2:
            self.dx *= -1

        if self.world_y > 1 or self.world_y < -1:
            self.dy *= -1

        self.worldMatrix = mat3.identity() * translation2(vec2(self.world_x, self.world_y))


