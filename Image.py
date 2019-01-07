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
from sdl2.sdlmixer import *
import os.path
from math3d import *
from Bullet import *
from Texture import *
from Sampler import *
from Ship import *
from Enemy import *

class Image():
    def __init__(self,scale, *files):
        self.tex = None
        self.samp = None
        self.vao = None
        self.scale = scale

    def drawStuff(self, background=False):
        Samp = Sampler()
        if background:
            Points = [-2, -1, 4, -1, 4, 1, -2, 1]
        else:
            Points = [-1, -1, 1, -1, 1, 1, -1, 1]
        Indicies = [0, 1, 2, 0, 2, 3]
        for i in range(len(Points)):
            Points[i] = Points[i] * self.scale
        Array = array.array("f", Points)
        ArrayBuffer = Buffer(Array)
        IndicieArray = array.array("I", Indicies)
        IndicieBuffer = Buffer(IndicieArray)
        TextureBuffer = Buffer(array.array("f", [0, 0, 1, 0, 1, 1, 0, 1]))
        tmp = array.array("I", [0])
        glGenVertexArrays(1, tmp)
        vao = tmp[0]
        glBindVertexArray(vao)
        ArrayBuffer.bind(GL_ARRAY_BUFFER)
        IndicieBuffer.bind(GL_ELEMENT_ARRAY_BUFFER)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 2 * 4, 0)
        TextureBuffer.bind(GL_ARRAY_BUFFER)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 2 * 4, 0)
        glBindVertexArray(0)
        self.samp = Samp
        self.vao = vao