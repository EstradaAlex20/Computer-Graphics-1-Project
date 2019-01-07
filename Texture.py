from Program import *
import io
import png
import zipfile
import os.path


class Texture:
    def __init__(self, typ):
        self.type = typ
        self.tex = None
    def bind(self,unit):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(self.type,self.tex)
    def unbind(self,unit):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(self.type,0)

class TextureCube(Texture):
    def __init__(self,size):
        Texture.__init__(self, GL_TEXTURE_CUBE_MAP)
        self.size = size

class ImageTextureCube(TextureCube):
    def __init__(self, namepattern):
        super().__init__(None)
        tmp = array.array("I", [0])
        glGenTextures(1,tmp)
        self.tex = tmp[0]
        self.bind(0)
        self.loadImages(namepattern)

    def loadImages(self, namepattern):
        for i in range(6):
            fname = os.path.join("assets", namepattern % i)
            membuf = io.BytesIO()
            pw, ph, fmt, pix = png.decode(open(fname,"rb").read())
            if pw != ph:
                raise RuntimeError("Cubemap must be square: "+fname)
            if i == 0:
                self.size = pw
            elif self.size != pw:
                raise RuntimeError("Cubmap sides: Wrong size: " + fname)
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGBA8,
                         self.size, self.size, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, pix)

        glGenerateMipmap(GL_TEXTURE_CUBE_MAP)


class Texture2DArray(Texture):
    def __init__(self,w,h,slices):
        Texture.__init__(self, GL_TEXTURE_2D_ARRAY)
        self.w = w
        self.h = h
        self.slices = slices


class DataTexture2DArray(Texture2DArray):
    def __init__(self, w, h, slices, pix):
        Texture2DArray.__init__(self,w,h,slices)
        tmp = array.array("I", [0])
        glGenTextures(1,tmp)
        self.tex = tmp[0]
        self.bind(0)
        glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_RGBA, w,h,slices, 0, GL_RGBA, GL_UNSIGNED_BYTE, pix)
        self.unbind(0)

    def setData(self,w,h,slices,pix):
        self.bind(0)
        if w == self.w and h == self.h and slices == self.slices:
            glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0, 0, 0, 0,w,h,slices, GL_RGBA, GL_UNSIGNED_BYTE, pix)
        else:
            glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_RGBA,w,h,slices, 0, GL_RGBA, GL_UNSIGNED_BYTE, pix)
            self.w = w
            self.h = h
            self.slices = slices
        glGenerateMipmap(GL_TEXTURE_2D_ARRAY)
        self.unbind(0)


class ImageTexture2DArray(DataTexture2DArray):
    def __init__(self, *files):
        membuf = io.BytesIO()
        w=None
        h=None
        slices=0
        for fname in files:
            if fname.endswith(".png") or fname.endswith(".jpg"):
                fname = os.path.join("assets", fname)
                tmp = open(fname, "rb").read()
                pw, ph, fmt, pix = png.decode(tmp)
                pix = png.flipY(pw, ph, pix)
                if w == None:
                    w = pw
                    h=ph
                else:
                    if w != pw or h != ph:
                        raise RuntimeError("Size mismatch")
                slices+= 1
                membuf.write(pix)

            elif fname.endswith(".ora") or fname.endswith(".zip"):
                z = zipfile.ZipFile(fname)
                for n in sorted(z.namelist()):
                    if n.endswith(".png") or n.endswith(".jpg"):
                        tmp = z.open(n).read()
                        pw, ph, fmt, pix = png.decode(tmp)
                        pix = png.flipY(pw, ph, pix)
                        if w == None:
                            w = pw
                            h = ph
                    else:
                        if w != pw or h != ph:
                            raise RuntimeError("Size mismatch")
                    slices += 1
                    membuf.write(pix)
            else:
                raise RuntimeError("Cannot read file " + fname)
        DataTexture2DArray.__init__(self,w,h,slices,membuf.getbuffer())