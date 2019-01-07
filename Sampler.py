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

class Sampler:
    def __init__(self):
        tmp = array.array("I", [0])
        glGenSamplers(1, tmp)
        self.samp = tmp[0]
        glSamplerParameteri(self.samp,GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glSamplerParameteri(self.samp,GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glSamplerParameteri(self.samp,GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glSamplerParameteri(self.samp, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def bind(self, unit):
        glBindSampler(unit, self.samp)
