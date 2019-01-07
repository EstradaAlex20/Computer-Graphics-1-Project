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
from Image import *
from Program import *
from sdl2.sdlttf import *


class Text:
    prog = None
    def __init__(self, fontname, size):
        if Text.prog == None:
            Text.prog = Program("TextVertexShader.txt", "TextFragmentShader.txt")

        self.txt = "temp"
        self.samp = Sampler()
        self.font = TTF_OpenFont(os.path.join("assets",fontname).encode(), size)
        open(os.path.join("assets", fontname))
        vbuff = Buffer(array.array("f", [0, 0, 1, 0, 1, 1, 0, 1]))
        ibuff = Buffer(array.array("I", [0, 1, 2, 0, 2, 3]))
        tmp = array.array("I", [0])
        glGenVertexArrays(1, tmp)
        self.vao = tmp[0]
        glBindVertexArray(self.vao)
        ibuff.bind(GL_ELEMENT_ARRAY_BUFFER)
        vbuff.bind(GL_ARRAY_BUFFER)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 2 * 4, 0)
        glBindVertexArray(0)
        self.tex = DataTexture2DArray(1,1,1,array.array("B",[0,0,0,0]))
        self.textQuadSize = vec2(0, 0)
        self.pos = vec2(0, 0)
        self.dirty = False
        surf1p = TTF_RenderUTF8_Blended(self.font, self.txt.encode(), SDL_Color(255, 255, 255, 255))
        surf2p = SDL_ConvertSurfaceFormat(surf1p, SDL_PIXELFORMAT_ABGR8888, 0)
        w = surf2p.contents.w
        h = surf2p.contents.h
        pitch = surf2p.contents.pitch
        if pitch != w * 4:
            print("Uh Oh!", pitch, w)
        pix = surf2p.contents.pixels
        B = string_at(pix, pitch * h)
        self.tex.setData(w, h, 1, B)
        SDL_FreeSurface(surf2p)
        SDL_FreeSurface(surf1p)
        self.textQuadSize = vec2(w, h)
        self.dirty = False

        Program.setUniform("textPosInPixels", self.pos)
        Program.setUniform("textQuadSizeInPixels", self.textQuadSize)
        Program.updateUniforms()


    def setText(self,pos,st):
        self.pos = pos
        self.txt = st
        self.dirty = True
        surf1p = TTF_RenderUTF8_Blended(self.font, self.txt.encode(), SDL_Color(255, 255, 255, 255))
        surf2p = SDL_ConvertSurfaceFormat(surf1p, SDL_PIXELFORMAT_ABGR8888, 0)
        w = surf2p.contents.w
        h = surf2p.contents.h
        pitch = surf2p.contents.pitch
        if pitch != w * 4:
            print("Uh Oh!", pitch, w)
        pix = surf2p.contents.pixels
        B = string_at(pix, pitch * h)
        self.tex.setData(w, h, 1, B)
        SDL_FreeSurface(surf2p)
        SDL_FreeSurface(surf1p)
        self.textQuadSize = vec2(w, h)
        Program.setUniform("textPosInPixels", self.pos)
        Program.setUniform("textQuadSizeInPixels", self.textQuadSize)
        Program.updateUniforms()
        self.dirty = False




