from gl import *
from glconstants import *
import array
import os.path
from Buffer import *

class Program:
    uniforms = {}
    ubo = None
    current = None
    def __init__(self, vsfname, fsfname):
        vs = self.compile(vsfname, GL_VERTEX_SHADER)
        fs = self.compile(fsfname, GL_FRAGMENT_SHADER)
        self.Prog = glCreateProgram()
        glAttachShader(self.Prog,vs)
        glAttachShader(self.Prog,fs)
        glLinkProgram(self.Prog)
        self.getLog(self.Prog, "Linking " + vsfname + " and " + "fsfname", glGetProgramInfoLog)
        tmp = array.array("I", [0])
        glGetProgramiv(self.Prog, GL_LINK_STATUS, tmp)
        if tmp[0] == 0:
            raise RuntimeError("Cannot Link")
        if Program.ubo == None:
            Program.setupUniforms(self.Prog)


    @staticmethod
    def setupUniforms(prog):
        tmp = array.array("I", [0])
        glGetProgramiv(prog, GL_ACTIVE_UNIFORMS, tmp)
        numuniforms = tmp[0]
        uniformsToQuery = array.array("I", range(numuniforms))
        offsets = array.array("I", [0] * numuniforms)
        sizes = array.array("I", [0] * numuniforms)
        types = array.array("I", [0] * numuniforms)
        glGetActiveUniformsiv(prog, numuniforms, uniformsToQuery, GL_UNIFORM_OFFSET, offsets)
        glGetActiveUniformsiv(prog, numuniforms, uniformsToQuery, GL_UNIFORM_SIZE, sizes)
        glGetActiveUniformsiv(prog, numuniforms, uniformsToQuery, GL_UNIFORM_TYPE, types)
        sizeForType = {GL_FLOAT_VEC4: 4*4,
                       GL_FLOAT_VEC3: 3 * 4,
                       GL_FLOAT_VEC2: 2 * 4,
                       GL_FLOAT: 1 * 4,
                       GL_INT: 1 * 4,
                       GL_FLOAT_MAT4: 4*16,
                       GL_FLOAT_MAT3: 3 * 16,
                       GL_FLOAT_MAT2: 2 * 16}
        nameBytes = bytearray(256)
        Program.totalUniformBytes = 0
        for i in range(numuniforms):
            glGetActiveUniformName(prog, i,len(nameBytes), tmp, nameBytes)
            nameLen = tmp[0]
            name = nameBytes[:nameLen].decode()
            if offsets[i] != 0xffffffff:
                assert sizes[i] == 1
                numBytes = sizeForType[types[i]]
                Program.uniforms[name] = (offsets[i], numBytes, types[i])
                end = offsets[i] + numBytes
                if end > Program.totalUniformBytes:
                    Program.totalUniformBytes = end
        Program.uboBackingMemory = create_string_buffer(Program.totalUniformBytes)
        Program.uboBackingAddress = addressof(Program.uboBackingMemory)
        Program.ubo = Buffer(initialData = None, size=Program.totalUniformBytes,usage=GL_DYNAMIC_DRAW)
        Program.ubo.bindBase(GL_UNIFORM_BUFFER, 0)

    @staticmethod
    def setUniform(name, value):
        offset, numBytes, typ = Program.uniforms[name]
        if typ == GL_FLOAT:
            value = array.array("f", [value])
        elif typ == GL_INT:
            value = array.array("I", [value])
        b = value.tobytes()
        if len(b) != numBytes:
            raise RuntimeError("Type mismatch when setting uniform '" + name+"': Got "+str(type(value)))
        dst = c_void_p(Program.uboBackingAddress + offset)
        memmove(dst, b, numBytes)

    @staticmethod
    def updateUniforms():
        glBufferSubData(GL_UNIFORM_BUFFER, 0, Program.totalUniformBytes, Program.uboBackingMemory)

    def compile(self, fname, typ):
        s = glCreateShader(typ)
        shaderdata = open(os.path.join("shaders", fname)).read()
        uniformdata = open(os.path.join("shaders", "uniforms.txt")).read()
        src = ["#version 430\n",
               "layout(std140, row_major) uniform Uniforms{\n",
               "#line 1\n", uniformdata, "};\n",
               "#line 1\n", shaderdata]
        glShaderSource(s, len(src), src, None)
        glCompileShader(s)
        self.getLog(s, "compiling " + fname, glGetShaderInfoLog)
        tmp = array.array("I", [0])
        glGetShaderiv(s, GL_COMPILE_STATUS, tmp)
        if tmp[0] == 0:
            raise RuntimeError("Could not Compile " + fname)
        return s

    def getLog(self, s, desc, f):
        blob = bytearray(5000)
        tmp = array.array("I", [0])
        f(s, len(blob), tmp, blob)
        length = tmp[0]
        if length == 0:
            return
        st = blob[:length]
        st = st.decode()
        print(desc)
        print(st)

    def use(self):
        glUseProgram(self.Prog)
        Program.current = self

    def draw(self):
        if self.dirty:
            self.renderTexture()

        oldprog = Program.current
        Text.prog.use()
        glBindVertexArray(self.vao)
        Program.setUniform("textQuadSizeInPixels", self.textQuadSize)
        Program.setUniform("textPosInPixels", self.pos)
        Program.updateUniforms()
        self.tex.bind(0)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)
        glBindVertexArray(0)
        if oldprog:
            oldprog.use()
