from gl import *
from glconstants import *
import array

class Buffer:
    def __init__(self, initialData, usage=GL_STATIC_DRAW, size=None):
        tmp = array.array("I", [0])
        glGenBuffers(1, tmp)
        self.buffID = tmp[0]
        glBindBuffer(GL_ARRAY_BUFFER, self.buffID)
        if initialData == None:
            glBufferData(GL_ARRAY_BUFFER, size, None, usage)
        else:
            if type(initialData) == array.array:
                tmp = initialData.tobytes()
            else:
                tmp = initialData
            glBufferData(GL_ARRAY_BUFFER, len(tmp), tmp, usage)

        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def bind(self, where):
        glBindBuffer(where, self.buffID)

    def bindBase(self, bindingPoint, index):
        glBindBufferBase(bindingPoint, index, self.buffID)

