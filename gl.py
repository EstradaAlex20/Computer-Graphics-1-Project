#Data from gl.xml, which has this copyright:

#Copyright (c) 2013-2016 The Khronos Group Inc.
#
#Permission is hereby granted, free of charge, to any person obtaining a
#copy of this software and/or associated documentation files (the
#"Materials"), to deal in the Materials without restriction, including
#without limitation the rights to use, copy, modify, merge, publish,
#distribute, sublicense, and/or sell copies of the Materials, and to
#permit persons to whom the Materials are furnished to do so, subject to
#the following conditions:
#
#The above copyright notice and this permission notice shall be included
#in all copies or substantial portions of the Materials.
#
#THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.
#
#------------------------------------------------------------------------
#
#This file, gl.xml, is the OpenGL and OpenGL API Registry. The older
#".spec" file format has been retired and will no longer be updated with
#new extensions and API versions. The canonical version of the registry,
#together with documentation, schema, and Python generator scripts used
#to generate C header files for OpenGL and OpenGL ES, can always be found
#in the Khronos Registry at
#        http://www.opengl.org/registry/
#    

import sys
from ctypes import *
import array

def __pyglMakeCallback(fname):
    def tmp(*args):
        raise RuntimeError("The function "+fname+" is not implemented")
    return tmp
        

#http://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function
def __pyglGetFuncAddress(funcname):
    if sys.platform.lower().find("win32") != -1:
        if "kernel32" not in __pyglGetFuncAddress.__dict__:

            __pyglGetFuncAddress.kernel32 = windll.kernel32

            __pyglGetFuncAddress.LoadLibraryA = __pyglGetFuncAddress.kernel32.LoadLibraryA
            __pyglGetFuncAddress.LoadLibraryA.argtypes=[c_char_p]
            __pyglGetFuncAddress.LoadLibraryA.restype = c_void_p


            __pyglGetFuncAddress.GetProcAddress = __pyglGetFuncAddress.kernel32.GetProcAddress
            __pyglGetFuncAddress.GetProcAddress.argtypes = [c_void_p,c_char_p]
            __pyglGetFuncAddress.GetProcAddress.restype = c_void_p

            __pyglGetFuncAddress.opengl32 = __pyglGetFuncAddress.LoadLibraryA(b"opengl32.dll")
            tmp = __pyglGetFuncAddress.GetProcAddress(__pyglGetFuncAddress.opengl32,b"wglGetProcAddress")
            __pyglGetFuncAddress.wglGetProcAddress = WINFUNCTYPE(c_void_p,c_char_p)(tmp)    

        x = __pyglGetFuncAddress.wglGetProcAddress(funcname.encode())
        if not x or x == None or x == 0 or x == 1 or x == 2 or x == 3 or x == -1 or x == 0xffffffff or x == 0xffffffffffffffff:
            x = __pyglGetFuncAddress.GetProcAddress(__pyglGetFuncAddress.opengl32,funcname.encode())
    else:
        if "dlopen" not in __pyglGetFuncAddress.__dict__:
            __pyglGetFuncAddress.dlopen = cdll.LoadLibrary("libdl.so").dlopen
            __pyglGetFuncAddress.dlopen.argtypes = [c_char_p,c_int]
            __pyglGetFuncAddress.dlopen.restype = c_void_p
            #2 = RTLD_NOW
            __pyglGetFuncAddress.libgl = __pyglGetFuncAddress.dlopen(b"libGL.so",2)
            __pyglGetFuncAddress.dlsym = cdll.LoadLibrary("libdl.so").dlsym
            __pyglGetFuncAddress.dlsym.argtypes = [c_void_p,c_char_p]
            __pyglGetFuncAddress.dlsym.restype = c_void_p
        x = __pyglGetFuncAddress.dlsym(__pyglGetFuncAddress.libgl,funcname.encode())
    #endif
    return x
            
if sys.platform.lower().find('win32') != -1:
    __PYGL_FUNC_TYPE = WINFUNCTYPE
else:
    __PYGL_FUNC_TYPE = CFUNCTYPE
      
      
def __pyglGetAsConstVoidPointer(v):
    if v == None:
        a= c_void_p(None)
    elif isinstance(v,bytes):
        a= c_char_p(v)
    elif isinstance(v,bytearray):
        a= (c_uint8*len(v)).from_buffer(v)
    elif isinstance(v,array.array):
        a= c_void_p(v.buffer_info()[0])
    elif isinstance(v, c_void_p):
        a = v
    elif isinstance(v, memoryview):
        a = v.tobytes()
    else:
        a = byref(v) #raise TypeError("Invalid type:"+str(type(v)))
    return a  
    
    
# <command>
#            <proto>void <name>glActiveShaderProgram</name></proto>
#            <param><ptype>GLuint</ptype> <name>pipeline</name></param>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#        </command>
#        
__glActiveShaderProgram_impl=None
def glActiveShaderProgram (pipeline, program):
    global __glActiveShaderProgram_impl
    if not __glActiveShaderProgram_impl:
        fptr = __pyglGetFuncAddress('glActiveShaderProgram')
        if not fptr:
            raise RuntimeError('The function glActiveShaderProgram is not available')
        __glActiveShaderProgram_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glActiveShaderProgram = __glActiveShaderProgram_impl
    return glActiveShaderProgram(pipeline, program)
# <command>
#            <proto>void <name>glActiveTexture</name></proto>
#            <param group="TextureUnit"><ptype>GLenum</ptype> <name>texture</name></param>
#            <glx opcode="197" type="render" />
#        </command>
#        
__glActiveTexture_impl=None
def glActiveTexture (texture):
    global __glActiveTexture_impl
    if not __glActiveTexture_impl:
        fptr = __pyglGetFuncAddress('glActiveTexture')
        if not fptr:
            raise RuntimeError('The function glActiveTexture is not available')
        __glActiveTexture_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glActiveTexture = __glActiveTexture_impl
    return glActiveTexture(texture)
# <command>
#            <proto>void <name>glAttachShader</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>shader</name></param>
#        </command>
#        
__glAttachShader_impl=None
def glAttachShader (program, shader):
    global __glAttachShader_impl
    if not __glAttachShader_impl:
        fptr = __pyglGetFuncAddress('glAttachShader')
        if not fptr:
            raise RuntimeError('The function glAttachShader is not available')
        __glAttachShader_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glAttachShader = __glAttachShader_impl
    return glAttachShader(program, shader)
# <command>
#            <proto>void <name>glBeginConditionalRender</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param group="TypeEnum"><ptype>GLenum</ptype> <name>mode</name></param>
#        </command>
#        
__glBeginConditionalRender_impl=None
def glBeginConditionalRender (id, mode):
    global __glBeginConditionalRender_impl
    if not __glBeginConditionalRender_impl:
        fptr = __pyglGetFuncAddress('glBeginConditionalRender')
        if not fptr:
            raise RuntimeError('The function glBeginConditionalRender is not available')
        __glBeginConditionalRender_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBeginConditionalRender = __glBeginConditionalRender_impl
    return glBeginConditionalRender(id, mode)
# <command>
#            <proto>void <name>glBeginQuery</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <glx opcode="231" type="render" />
#        </command>
#        
__glBeginQuery_impl=None
def glBeginQuery (target, id):
    global __glBeginQuery_impl
    if not __glBeginQuery_impl:
        fptr = __pyglGetFuncAddress('glBeginQuery')
        if not fptr:
            raise RuntimeError('The function glBeginQuery is not available')
        __glBeginQuery_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBeginQuery = __glBeginQuery_impl
    return glBeginQuery(target, id)
# <command>
#            <proto>void <name>glBeginQueryIndexed</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#        </command>
#        
__glBeginQueryIndexed_impl=None
def glBeginQueryIndexed (target, index, id):
    global __glBeginQueryIndexed_impl
    if not __glBeginQueryIndexed_impl:
        fptr = __pyglGetFuncAddress('glBeginQueryIndexed')
        if not fptr:
            raise RuntimeError('The function glBeginQueryIndexed is not available')
        __glBeginQueryIndexed_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glBeginQueryIndexed = __glBeginQueryIndexed_impl
    return glBeginQueryIndexed(target, index, id)
# <command>
#            <proto>void <name>glBeginTransformFeedback</name></proto>
#            <param><ptype>GLenum</ptype> <name>primitiveMode</name></param>
#        </command>
#        
__glBeginTransformFeedback_impl=None
def glBeginTransformFeedback (primitiveMode):
    global __glBeginTransformFeedback_impl
    if not __glBeginTransformFeedback_impl:
        fptr = __pyglGetFuncAddress('glBeginTransformFeedback')
        if not fptr:
            raise RuntimeError('The function glBeginTransformFeedback is not available')
        __glBeginTransformFeedback_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glBeginTransformFeedback = __glBeginTransformFeedback_impl
    return glBeginTransformFeedback(primitiveMode)
# <command>
#            <proto>void <name>glBindAttribLocation</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param>const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glBindAttribLocation_impl=None
def glBindAttribLocation (program, index, name):
    global __glBindAttribLocation_impl
    if not __glBindAttribLocation_impl:
        fptr = __pyglGetFuncAddress('glBindAttribLocation')
        if not fptr:
            raise RuntimeError('The function glBindAttribLocation is not available')
        __glBindAttribLocation_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glBindAttribLocation = (lambda program,index,name:__glBindAttribLocation_impl(program,index,c_char_p( name .encode() )))
    return glBindAttribLocation(program, index, name)
# <command>
#            <proto>void <name>glBindBuffer</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#        </command>
#        
__glBindBuffer_impl=None
def glBindBuffer (target, buffer):
    global __glBindBuffer_impl
    if not __glBindBuffer_impl:
        fptr = __pyglGetFuncAddress('glBindBuffer')
        if not fptr:
            raise RuntimeError('The function glBindBuffer is not available')
        __glBindBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBindBuffer = __glBindBuffer_impl
    return glBindBuffer(target, buffer)
# <command>
#            <proto>void <name>glBindBufferBase</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#        </command>
#        
__glBindBufferBase_impl=None
def glBindBufferBase (target, index, buffer):
    global __glBindBufferBase_impl
    if not __glBindBufferBase_impl:
        fptr = __pyglGetFuncAddress('glBindBufferBase')
        if not fptr:
            raise RuntimeError('The function glBindBufferBase is not available')
        __glBindBufferBase_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glBindBufferBase = __glBindBufferBase_impl
    return glBindBufferBase(target, index, buffer)
# <command>
#            <proto>void <name>glBindBufferRange</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#        </command>
#        
__glBindBufferRange_impl=None
def glBindBufferRange (target, index, buffer, offset, size):
    global __glBindBufferRange_impl
    if not __glBindBufferRange_impl:
        fptr = __pyglGetFuncAddress('glBindBufferRange')
        if not fptr:
            raise RuntimeError('The function glBindBufferRange is not available')
        __glBindBufferRange_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_size_t, c_void_p)(fptr)
    glBindBufferRange = __glBindBufferRange_impl
    return glBindBufferRange(target, index, buffer, offset, size)
# <command>
#            <proto>void <name>glBindBuffersBase</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>buffers</name></param>
#        </command>
#        
__glBindBuffersBase_impl=None
def glBindBuffersBase (target, first, count, buffers):
    global __glBindBuffersBase_impl
    if not __glBindBuffersBase_impl:
        fptr = __pyglGetFuncAddress('glBindBuffersBase')
        if not fptr:
            raise RuntimeError('The function glBindBuffersBase is not available')
        __glBindBuffersBase_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p)(fptr)
    glBindBuffersBase = (lambda target,first,count,buffers:__glBindBuffersBase_impl(target,first,count,__pyglGetAsConstVoidPointer( buffers )))
    return glBindBuffersBase(target, first, count, buffers)
# <command>
#            <proto>void <name>glBindBuffersRange</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>buffers</name></param>
#            <param len="count">const <ptype>GLintptr</ptype> *<name>offsets</name></param>
#            <param len="count">const <ptype>GLsizeiptr</ptype> *<name>sizes</name></param>
#        </command>
#        
__glBindBuffersRange_impl=None
def glBindBuffersRange (target, first, count, buffers, offsets, sizes):
    global __glBindBuffersRange_impl
    if not __glBindBuffersRange_impl:
        fptr = __pyglGetFuncAddress('glBindBuffersRange')
        if not fptr:
            raise RuntimeError('The function glBindBuffersRange is not available')
        __glBindBuffersRange_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p, c_void_p, c_void_p)(fptr)
    glBindBuffersRange = (lambda target,first,count,buffers,offsets,sizes:__glBindBuffersRange_impl(target,first,count,__pyglGetAsConstVoidPointer( buffers ),__pyglGetAsConstVoidPointer( offsets ),__pyglGetAsConstVoidPointer( sizes )))
    return glBindBuffersRange(target, first, count, buffers, offsets, sizes)
# <command>
#            <proto>void <name>glBindFragDataLocation</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>color</name></param>
#            <param len="COMPSIZE(name)">const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glBindFragDataLocation_impl=None
def glBindFragDataLocation (program, color, name):
    global __glBindFragDataLocation_impl
    if not __glBindFragDataLocation_impl:
        fptr = __pyglGetFuncAddress('glBindFragDataLocation')
        if not fptr:
            raise RuntimeError('The function glBindFragDataLocation is not available')
        __glBindFragDataLocation_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glBindFragDataLocation = (lambda program,color,name:__glBindFragDataLocation_impl(program,color,c_char_p( name .encode() )))
    return glBindFragDataLocation(program, color, name)
# <command>
#            <proto>void <name>glBindFragDataLocationIndexed</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>colorNumber</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param>const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glBindFragDataLocationIndexed_impl=None
def glBindFragDataLocationIndexed (program, colorNumber, index, name):
    global __glBindFragDataLocationIndexed_impl
    if not __glBindFragDataLocationIndexed_impl:
        fptr = __pyglGetFuncAddress('glBindFragDataLocationIndexed')
        if not fptr:
            raise RuntimeError('The function glBindFragDataLocationIndexed is not available')
        __glBindFragDataLocationIndexed_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glBindFragDataLocationIndexed = (lambda program,colorNumber,index,name:__glBindFragDataLocationIndexed_impl(program,colorNumber,index,c_char_p( name .encode() )))
    return glBindFragDataLocationIndexed(program, colorNumber, index, name)
# <command>
#            <proto>void <name>glBindFramebuffer</name></proto>
#            <param group="FramebufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <glx opcode="236" type="render" />
#        </command>
#        
__glBindFramebuffer_impl=None
def glBindFramebuffer (target, framebuffer):
    global __glBindFramebuffer_impl
    if not __glBindFramebuffer_impl:
        fptr = __pyglGetFuncAddress('glBindFramebuffer')
        if not fptr:
            raise RuntimeError('The function glBindFramebuffer is not available')
        __glBindFramebuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBindFramebuffer = __glBindFramebuffer_impl
    return glBindFramebuffer(target, framebuffer)
# <command>
#            <proto>void <name>glBindImageTexture</name></proto>
#            <param><ptype>GLuint</ptype> <name>unit</name></param>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>layered</name></param>
#            <param><ptype>GLint</ptype> <name>layer</name></param>
#            <param><ptype>GLenum</ptype> <name>access</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#        </command>
#        
__glBindImageTexture_impl=None
def glBindImageTexture (unit, texture, level, layered, layer, access, format):
    global __glBindImageTexture_impl
    if not __glBindImageTexture_impl:
        fptr = __pyglGetFuncAddress('glBindImageTexture')
        if not fptr:
            raise RuntimeError('The function glBindImageTexture is not available')
        __glBindImageTexture_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_char, c_int, c_uint, c_uint)(fptr)
    glBindImageTexture = __glBindImageTexture_impl
    return glBindImageTexture(unit, texture, level, layered, layer, access, format)
# <command>
#            <proto>void <name>glBindImageTextures</name></proto>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>textures</name></param>
#        </command>
#        
__glBindImageTextures_impl=None
def glBindImageTextures (first, count, textures):
    global __glBindImageTextures_impl
    if not __glBindImageTextures_impl:
        fptr = __pyglGetFuncAddress('glBindImageTextures')
        if not fptr:
            raise RuntimeError('The function glBindImageTextures is not available')
        __glBindImageTextures_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glBindImageTextures = (lambda first,count,textures:__glBindImageTextures_impl(first,count,__pyglGetAsConstVoidPointer( textures )))
    return glBindImageTextures(first, count, textures)
# <command>
#            <proto>void <name>glBindProgramPipeline</name></proto>
#            <param><ptype>GLuint</ptype> <name>pipeline</name></param>
#        </command>
#        
__glBindProgramPipeline_impl=None
def glBindProgramPipeline (pipeline):
    global __glBindProgramPipeline_impl
    if not __glBindProgramPipeline_impl:
        fptr = __pyglGetFuncAddress('glBindProgramPipeline')
        if not fptr:
            raise RuntimeError('The function glBindProgramPipeline is not available')
        __glBindProgramPipeline_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glBindProgramPipeline = __glBindProgramPipeline_impl
    return glBindProgramPipeline(pipeline)
# <command>
#            <proto>void <name>glBindRenderbuffer</name></proto>
#            <param group="RenderbufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>renderbuffer</name></param>
#            <glx opcode="235" type="render" />
#        </command>
#        
__glBindRenderbuffer_impl=None
def glBindRenderbuffer (target, renderbuffer):
    global __glBindRenderbuffer_impl
    if not __glBindRenderbuffer_impl:
        fptr = __pyglGetFuncAddress('glBindRenderbuffer')
        if not fptr:
            raise RuntimeError('The function glBindRenderbuffer is not available')
        __glBindRenderbuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBindRenderbuffer = __glBindRenderbuffer_impl
    return glBindRenderbuffer(target, renderbuffer)
# <command>
#            <proto>void <name>glBindSampler</name></proto>
#            <param><ptype>GLuint</ptype> <name>unit</name></param>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#        </command>
#        
__glBindSampler_impl=None
def glBindSampler (unit, sampler):
    global __glBindSampler_impl
    if not __glBindSampler_impl:
        fptr = __pyglGetFuncAddress('glBindSampler')
        if not fptr:
            raise RuntimeError('The function glBindSampler is not available')
        __glBindSampler_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBindSampler = __glBindSampler_impl
    return glBindSampler(unit, sampler)
# <command>
#            <proto>void <name>glBindSamplers</name></proto>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>samplers</name></param>
#        </command>
#        
__glBindSamplers_impl=None
def glBindSamplers (first, count, samplers):
    global __glBindSamplers_impl
    if not __glBindSamplers_impl:
        fptr = __pyglGetFuncAddress('glBindSamplers')
        if not fptr:
            raise RuntimeError('The function glBindSamplers is not available')
        __glBindSamplers_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glBindSamplers = (lambda first,count,samplers:__glBindSamplers_impl(first,count,__pyglGetAsConstVoidPointer( samplers )))
    return glBindSamplers(first, count, samplers)
# <command>
#            <proto>void <name>glBindTexture</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="Texture"><ptype>GLuint</ptype> <name>texture</name></param>
#            <glx opcode="4117" type="render" />
#        </command>
#        
__glBindTexture_impl=None
def glBindTexture (target, texture):
    global __glBindTexture_impl
    if not __glBindTexture_impl:
        fptr = __pyglGetFuncAddress('glBindTexture')
        if not fptr:
            raise RuntimeError('The function glBindTexture is not available')
        __glBindTexture_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBindTexture = __glBindTexture_impl
    return glBindTexture(target, texture)
# <command>
#            <proto>void <name>glBindTextureUnit</name></proto>
#            <param><ptype>GLuint</ptype> <name>unit</name></param>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#        </command>
#        
__glBindTextureUnit_impl=None
def glBindTextureUnit (unit, texture):
    global __glBindTextureUnit_impl
    if not __glBindTextureUnit_impl:
        fptr = __pyglGetFuncAddress('glBindTextureUnit')
        if not fptr:
            raise RuntimeError('The function glBindTextureUnit is not available')
        __glBindTextureUnit_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBindTextureUnit = __glBindTextureUnit_impl
    return glBindTextureUnit(unit, texture)
# <command>
#            <proto>void <name>glBindTextures</name></proto>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>textures</name></param>
#        </command>
#        
__glBindTextures_impl=None
def glBindTextures (first, count, textures):
    global __glBindTextures_impl
    if not __glBindTextures_impl:
        fptr = __pyglGetFuncAddress('glBindTextures')
        if not fptr:
            raise RuntimeError('The function glBindTextures is not available')
        __glBindTextures_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glBindTextures = (lambda first,count,textures:__glBindTextures_impl(first,count,__pyglGetAsConstVoidPointer( textures )))
    return glBindTextures(first, count, textures)
# <command>
#            <proto>void <name>glBindTransformFeedback</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#        </command>
#        
__glBindTransformFeedback_impl=None
def glBindTransformFeedback (target, id):
    global __glBindTransformFeedback_impl
    if not __glBindTransformFeedback_impl:
        fptr = __pyglGetFuncAddress('glBindTransformFeedback')
        if not fptr:
            raise RuntimeError('The function glBindTransformFeedback is not available')
        __glBindTransformFeedback_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBindTransformFeedback = __glBindTransformFeedback_impl
    return glBindTransformFeedback(target, id)
# <command>
#            <proto>void <name>glBindVertexArray</name></proto>
#            <param><ptype>GLuint</ptype> <name>array</name></param>
#            <glx opcode="350" type="render" />
#        </command>
#        
__glBindVertexArray_impl=None
def glBindVertexArray (array):
    global __glBindVertexArray_impl
    if not __glBindVertexArray_impl:
        fptr = __pyglGetFuncAddress('glBindVertexArray')
        if not fptr:
            raise RuntimeError('The function glBindVertexArray is not available')
        __glBindVertexArray_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glBindVertexArray = __glBindVertexArray_impl
    return glBindVertexArray(array)
# <command>
#            <proto>void <name>glBindVertexBuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>bindingindex</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param><ptype>GLsizei</ptype> <name>stride</name></param>
#        </command>
#        
__glBindVertexBuffer_impl=None
def glBindVertexBuffer (bindingindex, buffer, offset, stride):
    global __glBindVertexBuffer_impl
    if not __glBindVertexBuffer_impl:
        fptr = __pyglGetFuncAddress('glBindVertexBuffer')
        if not fptr:
            raise RuntimeError('The function glBindVertexBuffer is not available')
        __glBindVertexBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_size_t, c_int)(fptr)
    glBindVertexBuffer = __glBindVertexBuffer_impl
    return glBindVertexBuffer(bindingindex, buffer, offset, stride)
# <command>
#            <proto>void <name>glBindVertexBuffers</name></proto>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>buffers</name></param>
#            <param len="count">const <ptype>GLintptr</ptype> *<name>offsets</name></param>
#            <param len="count">const <ptype>GLsizei</ptype> *<name>strides</name></param>
#        </command>
#        
__glBindVertexBuffers_impl=None
def glBindVertexBuffers (first, count, buffers, offsets, strides):
    global __glBindVertexBuffers_impl
    if not __glBindVertexBuffers_impl:
        fptr = __pyglGetFuncAddress('glBindVertexBuffers')
        if not fptr:
            raise RuntimeError('The function glBindVertexBuffers is not available')
        __glBindVertexBuffers_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_void_p, c_void_p)(fptr)
    glBindVertexBuffers = (lambda first,count,buffers,offsets,strides:__glBindVertexBuffers_impl(first,count,__pyglGetAsConstVoidPointer( buffers ),__pyglGetAsConstVoidPointer( offsets ),__pyglGetAsConstVoidPointer( strides )))
    return glBindVertexBuffers(first, count, buffers, offsets, strides)
# <command>
#            <proto>void <name>glBlendColor</name></proto>
#            <param group="ColorF"><ptype>GLfloat</ptype> <name>red</name></param>
#            <param group="ColorF"><ptype>GLfloat</ptype> <name>green</name></param>
#            <param group="ColorF"><ptype>GLfloat</ptype> <name>blue</name></param>
#            <param group="ColorF"><ptype>GLfloat</ptype> <name>alpha</name></param>
#            <glx opcode="4096" type="render" />
#        </command>
#        
__glBlendColor_impl=None
def glBlendColor (red, green, blue, alpha):
    global __glBlendColor_impl
    if not __glBlendColor_impl:
        fptr = __pyglGetFuncAddress('glBlendColor')
        if not fptr:
            raise RuntimeError('The function glBlendColor is not available')
        __glBlendColor_impl = __PYGL_FUNC_TYPE( None ,c_float, c_float, c_float, c_float)(fptr)
    glBlendColor = __glBlendColor_impl
    return glBlendColor(red, green, blue, alpha)
# <command>
#            <proto>void <name>glBlendEquation</name></proto>
#            <param group="BlendEquationMode"><ptype>GLenum</ptype> <name>mode</name></param>
#            <glx opcode="4097" type="render" />
#        </command>
#        
__glBlendEquation_impl=None
def glBlendEquation (mode):
    global __glBlendEquation_impl
    if not __glBlendEquation_impl:
        fptr = __pyglGetFuncAddress('glBlendEquation')
        if not fptr:
            raise RuntimeError('The function glBlendEquation is not available')
        __glBlendEquation_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glBlendEquation = __glBlendEquation_impl
    return glBlendEquation(mode)
# <command>
#            <proto>void <name>glBlendEquationSeparate</name></proto>
#            <param group="BlendEquationModeEXT"><ptype>GLenum</ptype> <name>modeRGB</name></param>
#            <param group="BlendEquationModeEXT"><ptype>GLenum</ptype> <name>modeAlpha</name></param>
#            <glx opcode="4228" type="render" />
#        </command>
#        
__glBlendEquationSeparate_impl=None
def glBlendEquationSeparate (modeRGB, modeAlpha):
    global __glBlendEquationSeparate_impl
    if not __glBlendEquationSeparate_impl:
        fptr = __pyglGetFuncAddress('glBlendEquationSeparate')
        if not fptr:
            raise RuntimeError('The function glBlendEquationSeparate is not available')
        __glBlendEquationSeparate_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBlendEquationSeparate = __glBlendEquationSeparate_impl
    return glBlendEquationSeparate(modeRGB, modeAlpha)
# <command>
#            <proto>void <name>glBlendEquationSeparatei</name></proto>
#            <param><ptype>GLuint</ptype> <name>buf</name></param>
#            <param><ptype>GLenum</ptype> <name>modeRGB</name></param>
#            <param><ptype>GLenum</ptype> <name>modeAlpha</name></param>
#        </command>
#        
__glBlendEquationSeparatei_impl=None
def glBlendEquationSeparatei (buf, modeRGB, modeAlpha):
    global __glBlendEquationSeparatei_impl
    if not __glBlendEquationSeparatei_impl:
        fptr = __pyglGetFuncAddress('glBlendEquationSeparatei')
        if not fptr:
            raise RuntimeError('The function glBlendEquationSeparatei is not available')
        __glBlendEquationSeparatei_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glBlendEquationSeparatei = __glBlendEquationSeparatei_impl
    return glBlendEquationSeparatei(buf, modeRGB, modeAlpha)
# <command>
#            <proto>void <name>glBlendEquationi</name></proto>
#            <param><ptype>GLuint</ptype> <name>buf</name></param>
#            <param><ptype>GLenum</ptype> <name>mode</name></param>
#        </command>
#        
__glBlendEquationi_impl=None
def glBlendEquationi (buf, mode):
    global __glBlendEquationi_impl
    if not __glBlendEquationi_impl:
        fptr = __pyglGetFuncAddress('glBlendEquationi')
        if not fptr:
            raise RuntimeError('The function glBlendEquationi is not available')
        __glBlendEquationi_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBlendEquationi = __glBlendEquationi_impl
    return glBlendEquationi(buf, mode)
# <command>
#            <proto>void <name>glBlendFunc</name></proto>
#            <param group="BlendingFactorSrc"><ptype>GLenum</ptype> <name>sfactor</name></param>
#            <param group="BlendingFactorDest"><ptype>GLenum</ptype> <name>dfactor</name></param>
#            <glx opcode="160" type="render" />
#        </command>
#        
__glBlendFunc_impl=None
def glBlendFunc (sfactor, dfactor):
    global __glBlendFunc_impl
    if not __glBlendFunc_impl:
        fptr = __pyglGetFuncAddress('glBlendFunc')
        if not fptr:
            raise RuntimeError('The function glBlendFunc is not available')
        __glBlendFunc_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glBlendFunc = __glBlendFunc_impl
    return glBlendFunc(sfactor, dfactor)
# <command>
#            <proto>void <name>glBlendFuncSeparate</name></proto>
#            <param group="BlendFuncSeparateParameterEXT"><ptype>GLenum</ptype> <name>sfactorRGB</name></param>
#            <param group="BlendFuncSeparateParameterEXT"><ptype>GLenum</ptype> <name>dfactorRGB</name></param>
#            <param group="BlendFuncSeparateParameterEXT"><ptype>GLenum</ptype> <name>sfactorAlpha</name></param>
#            <param group="BlendFuncSeparateParameterEXT"><ptype>GLenum</ptype> <name>dfactorAlpha</name></param>
#            <glx opcode="4134" type="render" />
#        </command>
#        
__glBlendFuncSeparate_impl=None
def glBlendFuncSeparate (sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha):
    global __glBlendFuncSeparate_impl
    if not __glBlendFuncSeparate_impl:
        fptr = __pyglGetFuncAddress('glBlendFuncSeparate')
        if not fptr:
            raise RuntimeError('The function glBlendFuncSeparate is not available')
        __glBlendFuncSeparate_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint)(fptr)
    glBlendFuncSeparate = __glBlendFuncSeparate_impl
    return glBlendFuncSeparate(sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha)
# <command>
#            <proto>void <name>glBlendFuncSeparatei</name></proto>
#            <param><ptype>GLuint</ptype> <name>buf</name></param>
#            <param><ptype>GLenum</ptype> <name>srcRGB</name></param>
#            <param><ptype>GLenum</ptype> <name>dstRGB</name></param>
#            <param><ptype>GLenum</ptype> <name>srcAlpha</name></param>
#            <param><ptype>GLenum</ptype> <name>dstAlpha</name></param>
#        </command>
#        
__glBlendFuncSeparatei_impl=None
def glBlendFuncSeparatei (buf, srcRGB, dstRGB, srcAlpha, dstAlpha):
    global __glBlendFuncSeparatei_impl
    if not __glBlendFuncSeparatei_impl:
        fptr = __pyglGetFuncAddress('glBlendFuncSeparatei')
        if not fptr:
            raise RuntimeError('The function glBlendFuncSeparatei is not available')
        __glBlendFuncSeparatei_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_uint)(fptr)
    glBlendFuncSeparatei = __glBlendFuncSeparatei_impl
    return glBlendFuncSeparatei(buf, srcRGB, dstRGB, srcAlpha, dstAlpha)
# <command>
#            <proto>void <name>glBlendFunci</name></proto>
#            <param><ptype>GLuint</ptype> <name>buf</name></param>
#            <param><ptype>GLenum</ptype> <name>src</name></param>
#            <param><ptype>GLenum</ptype> <name>dst</name></param>
#        </command>
#        
__glBlendFunci_impl=None
def glBlendFunci (buf, src, dst):
    global __glBlendFunci_impl
    if not __glBlendFunci_impl:
        fptr = __pyglGetFuncAddress('glBlendFunci')
        if not fptr:
            raise RuntimeError('The function glBlendFunci is not available')
        __glBlendFunci_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glBlendFunci = __glBlendFunci_impl
    return glBlendFunci(buf, src, dst)
# <command>
#            <proto>void <name>glBlitFramebuffer</name></proto>
#            <param><ptype>GLint</ptype> <name>srcX0</name></param>
#            <param><ptype>GLint</ptype> <name>srcY0</name></param>
#            <param><ptype>GLint</ptype> <name>srcX1</name></param>
#            <param><ptype>GLint</ptype> <name>srcY1</name></param>
#            <param><ptype>GLint</ptype> <name>dstX0</name></param>
#            <param><ptype>GLint</ptype> <name>dstY0</name></param>
#            <param><ptype>GLint</ptype> <name>dstX1</name></param>
#            <param><ptype>GLint</ptype> <name>dstY1</name></param>
#            <param group="ClearBufferMask"><ptype>GLbitfield</ptype> <name>mask</name></param>
#            <param><ptype>GLenum</ptype> <name>filter</name></param>
#            <glx opcode="4330" type="render" />
#        </command>
#        
__glBlitFramebuffer_impl=None
def glBlitFramebuffer (srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, dstX1, dstY1, mask, filter):
    global __glBlitFramebuffer_impl
    if not __glBlitFramebuffer_impl:
        fptr = __pyglGetFuncAddress('glBlitFramebuffer')
        if not fptr:
            raise RuntimeError('The function glBlitFramebuffer is not available')
        __glBlitFramebuffer_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint)(fptr)
    glBlitFramebuffer = __glBlitFramebuffer_impl
    return glBlitFramebuffer(srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, dstX1, dstY1, mask, filter)
# <command>
#            <proto>void <name>glBlitNamedFramebuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>readFramebuffer</name></param>
#            <param><ptype>GLuint</ptype> <name>drawFramebuffer</name></param>
#            <param><ptype>GLint</ptype> <name>srcX0</name></param>
#            <param><ptype>GLint</ptype> <name>srcY0</name></param>
#            <param><ptype>GLint</ptype> <name>srcX1</name></param>
#            <param><ptype>GLint</ptype> <name>srcY1</name></param>
#            <param><ptype>GLint</ptype> <name>dstX0</name></param>
#            <param><ptype>GLint</ptype> <name>dstY0</name></param>
#            <param><ptype>GLint</ptype> <name>dstX1</name></param>
#            <param><ptype>GLint</ptype> <name>dstY1</name></param>
#            <param><ptype>GLbitfield</ptype> <name>mask</name></param>
#            <param><ptype>GLenum</ptype> <name>filter</name></param>
#        </command>
#        
__glBlitNamedFramebuffer_impl=None
def glBlitNamedFramebuffer (readFramebuffer, drawFramebuffer, srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, dstX1, dstY1, mask, filter):
    global __glBlitNamedFramebuffer_impl
    if not __glBlitNamedFramebuffer_impl:
        fptr = __pyglGetFuncAddress('glBlitNamedFramebuffer')
        if not fptr:
            raise RuntimeError('The function glBlitNamedFramebuffer is not available')
        __glBlitNamedFramebuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint)(fptr)
    glBlitNamedFramebuffer = __glBlitNamedFramebuffer_impl
    return glBlitNamedFramebuffer(readFramebuffer, drawFramebuffer, srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, dstX1, dstY1, mask, filter)
# <command>
#            <proto>void <name>glBufferData</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param len="size">const void *<name>data</name></param>
#            <param group="BufferUsageARB"><ptype>GLenum</ptype> <name>usage</name></param>
#        </command>
#        
__glBufferData_impl=None
def glBufferData (target, size, data, usage):
    global __glBufferData_impl
    if not __glBufferData_impl:
        fptr = __pyglGetFuncAddress('glBufferData')
        if not fptr:
            raise RuntimeError('The function glBufferData is not available')
        __glBufferData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p, c_void_p, c_uint)(fptr)
    glBufferData = (lambda target,size,data,usage:__glBufferData_impl(target,size,__pyglGetAsConstVoidPointer( data ),usage))
    return glBufferData(target, size, data, usage)
# <command>
#            <proto>void <name>glBufferStorage</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param len="size">const void *<name>data</name></param>
#            <param><ptype>GLbitfield</ptype> <name>flags</name></param>
#        </command>
#        
__glBufferStorage_impl=None
def glBufferStorage (target, size, data, flags):
    global __glBufferStorage_impl
    if not __glBufferStorage_impl:
        fptr = __pyglGetFuncAddress('glBufferStorage')
        if not fptr:
            raise RuntimeError('The function glBufferStorage is not available')
        __glBufferStorage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p, c_void_p, c_uint)(fptr)
    glBufferStorage = (lambda target,size,data,flags:__glBufferStorage_impl(target,size,__pyglGetAsConstVoidPointer( data ),flags))
    return glBufferStorage(target, size, data, flags)
# <command>
#            <proto>void <name>glBufferSubData</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param len="size">const void *<name>data</name></param>
#        </command>
#        
__glBufferSubData_impl=None
def glBufferSubData (target, offset, size, data):
    global __glBufferSubData_impl
    if not __glBufferSubData_impl:
        fptr = __pyglGetFuncAddress('glBufferSubData')
        if not fptr:
            raise RuntimeError('The function glBufferSubData is not available')
        __glBufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_size_t, c_void_p, c_void_p)(fptr)
    glBufferSubData = (lambda target,offset,size,data:__glBufferSubData_impl(target,offset,size,__pyglGetAsConstVoidPointer( data )))
    return glBufferSubData(target, offset, size, data)
# <command>
#            <proto><ptype>GLenum</ptype> <name>glCheckFramebufferStatus</name></proto>
#            <param group="FramebufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <glx opcode="1427" type="vendor" />
#        </command>
#        
__glCheckFramebufferStatus_impl=None
def glCheckFramebufferStatus (target):
    global __glCheckFramebufferStatus_impl
    if not __glCheckFramebufferStatus_impl:
        fptr = __pyglGetFuncAddress('glCheckFramebufferStatus')
        if not fptr:
            raise RuntimeError('The function glCheckFramebufferStatus is not available')
        __glCheckFramebufferStatus_impl = __PYGL_FUNC_TYPE( c_uint ,c_uint)(fptr)
    glCheckFramebufferStatus = __glCheckFramebufferStatus_impl
    return glCheckFramebufferStatus(target)
# <command>
#            <proto><ptype>GLenum</ptype> <name>glCheckNamedFramebufferStatus</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#        </command>
#        
__glCheckNamedFramebufferStatus_impl=None
def glCheckNamedFramebufferStatus (framebuffer, target):
    global __glCheckNamedFramebufferStatus_impl
    if not __glCheckNamedFramebufferStatus_impl:
        fptr = __pyglGetFuncAddress('glCheckNamedFramebufferStatus')
        if not fptr:
            raise RuntimeError('The function glCheckNamedFramebufferStatus is not available')
        __glCheckNamedFramebufferStatus_impl = __PYGL_FUNC_TYPE( c_uint ,c_uint, c_uint)(fptr)
    glCheckNamedFramebufferStatus = __glCheckNamedFramebufferStatus_impl
    return glCheckNamedFramebufferStatus(framebuffer, target)
# <command>
#            <proto>void <name>glClampColor</name></proto>
#            <param group="ClampColorTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="ClampColorModeARB"><ptype>GLenum</ptype> <name>clamp</name></param>
#            <glx opcode="234" type="render" />
#        </command>
#        
__glClampColor_impl=None
def glClampColor (target, clamp):
    global __glClampColor_impl
    if not __glClampColor_impl:
        fptr = __pyglGetFuncAddress('glClampColor')
        if not fptr:
            raise RuntimeError('The function glClampColor is not available')
        __glClampColor_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glClampColor = __glClampColor_impl
    return glClampColor(target, clamp)
# <command>
#            <proto>void <name>glClear</name></proto>
#            <param group="ClearBufferMask"><ptype>GLbitfield</ptype> <name>mask</name></param>
#            <glx opcode="127" type="render" />
#        </command>
#        
__glClear_impl=None
def glClear (mask):
    global __glClear_impl
    if not __glClear_impl:
        fptr = __pyglGetFuncAddress('glClear')
        if not fptr:
            raise RuntimeError('The function glClear is not available')
        __glClear_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glClear = __glClear_impl
    return glClear(mask)
# <command>
#            <proto>void <name>glClearBufferData</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type)">const void *<name>data</name></param>
#        </command>
#        
__glClearBufferData_impl=None
def glClearBufferData (target, internalformat, format, type, data):
    global __glClearBufferData_impl
    if not __glClearBufferData_impl:
        fptr = __pyglGetFuncAddress('glClearBufferData')
        if not fptr:
            raise RuntimeError('The function glClearBufferData is not available')
        __glClearBufferData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_void_p)(fptr)
    glClearBufferData = (lambda target,internalformat,format,type,data:__glClearBufferData_impl(target,internalformat,format,type,__pyglGetAsConstVoidPointer( data )))
    return glClearBufferData(target, internalformat, format, type, data)
# <command>
#            <proto>void <name>glClearBufferSubData</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type)">const void *<name>data</name></param>
#        </command>
#        
__glClearBufferSubData_impl=None
def glClearBufferSubData (target, internalformat, offset, size, format, type, data):
    global __glClearBufferSubData_impl
    if not __glClearBufferSubData_impl:
        fptr = __pyglGetFuncAddress('glClearBufferSubData')
        if not fptr:
            raise RuntimeError('The function glClearBufferSubData is not available')
        __glClearBufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_size_t, c_void_p, c_uint, c_uint, c_void_p)(fptr)
    glClearBufferSubData = (lambda target,internalformat,offset,size,format,type,data:__glClearBufferSubData_impl(target,internalformat,offset,size,format,type,__pyglGetAsConstVoidPointer( data )))
    return glClearBufferSubData(target, internalformat, offset, size, format, type, data)
# <command>
#            <proto>void <name>glClearBufferfi</name></proto>
#            <param><ptype>GLenum</ptype> <name>buffer</name></param>
#            <param group="DrawBufferName"><ptype>GLint</ptype> <name>drawbuffer</name></param>
#            <param><ptype>GLfloat</ptype> <name>depth</name></param>
#            <param><ptype>GLint</ptype> <name>stencil</name></param>
#        </command>
#        
__glClearBufferfi_impl=None
def glClearBufferfi (buffer, drawbuffer, depth, stencil):
    global __glClearBufferfi_impl
    if not __glClearBufferfi_impl:
        fptr = __pyglGetFuncAddress('glClearBufferfi')
        if not fptr:
            raise RuntimeError('The function glClearBufferfi is not available')
        __glClearBufferfi_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_float, c_int)(fptr)
    glClearBufferfi = __glClearBufferfi_impl
    return glClearBufferfi(buffer, drawbuffer, depth, stencil)
# <command>
#            <proto>void <name>glClearBufferfv</name></proto>
#            <param><ptype>GLenum</ptype> <name>buffer</name></param>
#            <param group="DrawBufferName"><ptype>GLint</ptype> <name>drawbuffer</name></param>
#            <param len="COMPSIZE(buffer)">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glClearBufferfv_impl=None
def glClearBufferfv (buffer, drawbuffer, value):
    global __glClearBufferfv_impl
    if not __glClearBufferfv_impl:
        fptr = __pyglGetFuncAddress('glClearBufferfv')
        if not fptr:
            raise RuntimeError('The function glClearBufferfv is not available')
        __glClearBufferfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glClearBufferfv = (lambda buffer,drawbuffer,value:__glClearBufferfv_impl(buffer,drawbuffer,__pyglGetAsConstVoidPointer( value )))
    return glClearBufferfv(buffer, drawbuffer, value)
# <command>
#            <proto>void <name>glClearBufferiv</name></proto>
#            <param><ptype>GLenum</ptype> <name>buffer</name></param>
#            <param group="DrawBufferName"><ptype>GLint</ptype> <name>drawbuffer</name></param>
#            <param len="COMPSIZE(buffer)">const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glClearBufferiv_impl=None
def glClearBufferiv (buffer, drawbuffer, value):
    global __glClearBufferiv_impl
    if not __glClearBufferiv_impl:
        fptr = __pyglGetFuncAddress('glClearBufferiv')
        if not fptr:
            raise RuntimeError('The function glClearBufferiv is not available')
        __glClearBufferiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glClearBufferiv = (lambda buffer,drawbuffer,value:__glClearBufferiv_impl(buffer,drawbuffer,__pyglGetAsConstVoidPointer( value )))
    return glClearBufferiv(buffer, drawbuffer, value)
# <command>
#            <proto>void <name>glClearBufferuiv</name></proto>
#            <param><ptype>GLenum</ptype> <name>buffer</name></param>
#            <param group="DrawBufferName"><ptype>GLint</ptype> <name>drawbuffer</name></param>
#            <param len="COMPSIZE(buffer)">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glClearBufferuiv_impl=None
def glClearBufferuiv (buffer, drawbuffer, value):
    global __glClearBufferuiv_impl
    if not __glClearBufferuiv_impl:
        fptr = __pyglGetFuncAddress('glClearBufferuiv')
        if not fptr:
            raise RuntimeError('The function glClearBufferuiv is not available')
        __glClearBufferuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glClearBufferuiv = (lambda buffer,drawbuffer,value:__glClearBufferuiv_impl(buffer,drawbuffer,__pyglGetAsConstVoidPointer( value )))
    return glClearBufferuiv(buffer, drawbuffer, value)
# <command>
#            <proto>void <name>glClearColor</name></proto>
#            <param group="ColorF"><ptype>GLfloat</ptype> <name>red</name></param>
#            <param group="ColorF"><ptype>GLfloat</ptype> <name>green</name></param>
#            <param group="ColorF"><ptype>GLfloat</ptype> <name>blue</name></param>
#            <param group="ColorF"><ptype>GLfloat</ptype> <name>alpha</name></param>
#            <glx opcode="130" type="render" />
#        </command>
#        
__glClearColor_impl=None
def glClearColor (red, green, blue, alpha):
    global __glClearColor_impl
    if not __glClearColor_impl:
        fptr = __pyglGetFuncAddress('glClearColor')
        if not fptr:
            raise RuntimeError('The function glClearColor is not available')
        __glClearColor_impl = __PYGL_FUNC_TYPE( None ,c_float, c_float, c_float, c_float)(fptr)
    glClearColor = __glClearColor_impl
    return glClearColor(red, green, blue, alpha)
# <command>
#            <proto>void <name>glClearDepth</name></proto>
#            <param><ptype>GLdouble</ptype> <name>depth</name></param>
#            <glx opcode="132" type="render" />
#        </command>
#        
__glClearDepth_impl=None
def glClearDepth (depth):
    global __glClearDepth_impl
    if not __glClearDepth_impl:
        fptr = __pyglGetFuncAddress('glClearDepth')
        if not fptr:
            raise RuntimeError('The function glClearDepth is not available')
        __glClearDepth_impl = __PYGL_FUNC_TYPE( None ,c_double)(fptr)
    glClearDepth = __glClearDepth_impl
    return glClearDepth(depth)
# <command>
#            <proto>void <name>glClearDepthf</name></proto>
#            <param><ptype>GLfloat</ptype> <name>d</name></param>
#        </command>
#        
__glClearDepthf_impl=None
def glClearDepthf (d):
    global __glClearDepthf_impl
    if not __glClearDepthf_impl:
        fptr = __pyglGetFuncAddress('glClearDepthf')
        if not fptr:
            raise RuntimeError('The function glClearDepthf is not available')
        __glClearDepthf_impl = __PYGL_FUNC_TYPE( None ,c_float)(fptr)
    glClearDepthf = __glClearDepthf_impl
    return glClearDepthf(d)
# <command>
#            <proto>void <name>glClearNamedBufferData</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param>const void *<name>data</name></param>
#        </command>
#        
__glClearNamedBufferData_impl=None
def glClearNamedBufferData (buffer, internalformat, format, type, data):
    global __glClearNamedBufferData_impl
    if not __glClearNamedBufferData_impl:
        fptr = __pyglGetFuncAddress('glClearNamedBufferData')
        if not fptr:
            raise RuntimeError('The function glClearNamedBufferData is not available')
        __glClearNamedBufferData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_void_p)(fptr)
    glClearNamedBufferData = (lambda buffer,internalformat,format,type,data:__glClearNamedBufferData_impl(buffer,internalformat,format,type,__pyglGetAsConstVoidPointer( data )))
    return glClearNamedBufferData(buffer, internalformat, format, type, data)
# <command>
#            <proto>void <name>glClearNamedBufferSubData</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param>const void *<name>data</name></param>
#        </command>
#        
__glClearNamedBufferSubData_impl=None
def glClearNamedBufferSubData (buffer, internalformat, offset, size, format, type, data):
    global __glClearNamedBufferSubData_impl
    if not __glClearNamedBufferSubData_impl:
        fptr = __pyglGetFuncAddress('glClearNamedBufferSubData')
        if not fptr:
            raise RuntimeError('The function glClearNamedBufferSubData is not available')
        __glClearNamedBufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_size_t, c_void_p, c_uint, c_uint, c_void_p)(fptr)
    glClearNamedBufferSubData = (lambda buffer,internalformat,offset,size,format,type,data:__glClearNamedBufferSubData_impl(buffer,internalformat,offset,size,format,type,__pyglGetAsConstVoidPointer( data )))
    return glClearNamedBufferSubData(buffer, internalformat, offset, size, format, type, data)
# <command>
#            <proto>void <name>glClearNamedFramebufferfi</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>buffer</name></param>
#            <param><ptype>GLint</ptype> <name>drawbuffer</name></param>
#            <param><ptype>GLfloat</ptype> <name>depth</name></param>
#            <param><ptype>GLint</ptype> <name>stencil</name></param>
#        </command>
#        
__glClearNamedFramebufferfi_impl=None
def glClearNamedFramebufferfi (framebuffer, buffer, drawbuffer, depth, stencil):
    global __glClearNamedFramebufferfi_impl
    if not __glClearNamedFramebufferfi_impl:
        fptr = __pyglGetFuncAddress('glClearNamedFramebufferfi')
        if not fptr:
            raise RuntimeError('The function glClearNamedFramebufferfi is not available')
        __glClearNamedFramebufferfi_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_float, c_int)(fptr)
    glClearNamedFramebufferfi = __glClearNamedFramebufferfi_impl
    return glClearNamedFramebufferfi(framebuffer, buffer, drawbuffer, depth, stencil)
# <command>
#            <proto>void <name>glClearNamedFramebufferfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>buffer</name></param>
#            <param><ptype>GLint</ptype> <name>drawbuffer</name></param>
#            <param>const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glClearNamedFramebufferfv_impl=None
def glClearNamedFramebufferfv (framebuffer, buffer, drawbuffer, value):
    global __glClearNamedFramebufferfv_impl
    if not __glClearNamedFramebufferfv_impl:
        fptr = __pyglGetFuncAddress('glClearNamedFramebufferfv')
        if not fptr:
            raise RuntimeError('The function glClearNamedFramebufferfv is not available')
        __glClearNamedFramebufferfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p)(fptr)
    glClearNamedFramebufferfv = (lambda framebuffer,buffer,drawbuffer,value:__glClearNamedFramebufferfv_impl(framebuffer,buffer,drawbuffer,__pyglGetAsConstVoidPointer( value )))
    return glClearNamedFramebufferfv(framebuffer, buffer, drawbuffer, value)
# <command>
#            <proto>void <name>glClearNamedFramebufferiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>buffer</name></param>
#            <param><ptype>GLint</ptype> <name>drawbuffer</name></param>
#            <param>const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glClearNamedFramebufferiv_impl=None
def glClearNamedFramebufferiv (framebuffer, buffer, drawbuffer, value):
    global __glClearNamedFramebufferiv_impl
    if not __glClearNamedFramebufferiv_impl:
        fptr = __pyglGetFuncAddress('glClearNamedFramebufferiv')
        if not fptr:
            raise RuntimeError('The function glClearNamedFramebufferiv is not available')
        __glClearNamedFramebufferiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p)(fptr)
    glClearNamedFramebufferiv = (lambda framebuffer,buffer,drawbuffer,value:__glClearNamedFramebufferiv_impl(framebuffer,buffer,drawbuffer,__pyglGetAsConstVoidPointer( value )))
    return glClearNamedFramebufferiv(framebuffer, buffer, drawbuffer, value)
# <command>
#            <proto>void <name>glClearNamedFramebufferuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>buffer</name></param>
#            <param><ptype>GLint</ptype> <name>drawbuffer</name></param>
#            <param>const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glClearNamedFramebufferuiv_impl=None
def glClearNamedFramebufferuiv (framebuffer, buffer, drawbuffer, value):
    global __glClearNamedFramebufferuiv_impl
    if not __glClearNamedFramebufferuiv_impl:
        fptr = __pyglGetFuncAddress('glClearNamedFramebufferuiv')
        if not fptr:
            raise RuntimeError('The function glClearNamedFramebufferuiv is not available')
        __glClearNamedFramebufferuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p)(fptr)
    glClearNamedFramebufferuiv = (lambda framebuffer,buffer,drawbuffer,value:__glClearNamedFramebufferuiv_impl(framebuffer,buffer,drawbuffer,__pyglGetAsConstVoidPointer( value )))
    return glClearNamedFramebufferuiv(framebuffer, buffer, drawbuffer, value)
# <command>
#            <proto>void <name>glClearStencil</name></proto>
#            <param group="StencilValue"><ptype>GLint</ptype> <name>s</name></param>
#            <glx opcode="131" type="render" />
#        </command>
#        
__glClearStencil_impl=None
def glClearStencil (s):
    global __glClearStencil_impl
    if not __glClearStencil_impl:
        fptr = __pyglGetFuncAddress('glClearStencil')
        if not fptr:
            raise RuntimeError('The function glClearStencil is not available')
        __glClearStencil_impl = __PYGL_FUNC_TYPE( None ,c_int)(fptr)
    glClearStencil = __glClearStencil_impl
    return glClearStencil(s)
# <command>
#            <proto>void <name>glClearTexImage</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type)">const void *<name>data</name></param>
#        </command>
#        
__glClearTexImage_impl=None
def glClearTexImage (texture, level, format, type, data):
    global __glClearTexImage_impl
    if not __glClearTexImage_impl:
        fptr = __pyglGetFuncAddress('glClearTexImage')
        if not fptr:
            raise RuntimeError('The function glClearTexImage is not available')
        __glClearTexImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_uint, c_void_p)(fptr)
    glClearTexImage = (lambda texture,level,format,type,data:__glClearTexImage_impl(texture,level,format,type,__pyglGetAsConstVoidPointer( data )))
    return glClearTexImage(texture, level, format, type, data)
# <command>
#            <proto>void <name>glClearTexSubImage</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type)">const void *<name>data</name></param>
#        </command>
#        
__glClearTexSubImage_impl=None
def glClearTexSubImage (texture, level, xoffset, yoffset, zoffset, width, height, depth, format, type, data):
    global __glClearTexSubImage_impl
    if not __glClearTexSubImage_impl:
        fptr = __pyglGetFuncAddress('glClearTexSubImage')
        if not fptr:
            raise RuntimeError('The function glClearTexSubImage is not available')
        __glClearTexSubImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glClearTexSubImage = (lambda texture,level,xoffset,yoffset,zoffset,width,height,depth,format,type,data:__glClearTexSubImage_impl(texture,level,xoffset,yoffset,zoffset,width,height,depth,format,type,__pyglGetAsConstVoidPointer( data )))
    return glClearTexSubImage(texture, level, xoffset, yoffset, zoffset, width, height, depth, format, type, data)
# <command>
#            <proto><ptype>GLenum</ptype> <name>glClientWaitSync</name></proto>
#            <param group="sync"><ptype>GLsync</ptype> <name>sync</name></param>
#            <param><ptype>GLbitfield</ptype> <name>flags</name></param>
#            <param><ptype>GLuint64</ptype> <name>timeout</name></param>
#        </command>
#        
__glClientWaitSync_impl=None
def glClientWaitSync (sync, flags, timeout):
    global __glClientWaitSync_impl
    if not __glClientWaitSync_impl:
        fptr = __pyglGetFuncAddress('glClientWaitSync')
        if not fptr:
            raise RuntimeError('The function glClientWaitSync is not available')
        __glClientWaitSync_impl = __PYGL_FUNC_TYPE( c_uint ,c_void_p, c_uint, c_ulonglong)(fptr)
    glClientWaitSync = __glClientWaitSync_impl
    return glClientWaitSync(sync, flags, timeout)
# <command>
#            <proto>void <name>glClipControl</name></proto>
#            <param><ptype>GLenum</ptype> <name>origin</name></param>
#            <param><ptype>GLenum</ptype> <name>depth</name></param>
#        </command>
#        
__glClipControl_impl=None
def glClipControl (origin, depth):
    global __glClipControl_impl
    if not __glClipControl_impl:
        fptr = __pyglGetFuncAddress('glClipControl')
        if not fptr:
            raise RuntimeError('The function glClipControl is not available')
        __glClipControl_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glClipControl = __glClipControl_impl
    return glClipControl(origin, depth)
# <command>
#            <proto>void <name>glColorMask</name></proto>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>red</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>green</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>blue</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>alpha</name></param>
#            <glx opcode="134" type="render" />
#        </command>
#        
__glColorMask_impl=None
def glColorMask (red, green, blue, alpha):
    global __glColorMask_impl
    if not __glColorMask_impl:
        fptr = __pyglGetFuncAddress('glColorMask')
        if not fptr:
            raise RuntimeError('The function glColorMask is not available')
        __glColorMask_impl = __PYGL_FUNC_TYPE( None ,c_char, c_char, c_char, c_char)(fptr)
    glColorMask = __glColorMask_impl
    return glColorMask(red, green, blue, alpha)
# <command>
#            <proto>void <name>glColorMaski</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>r</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>g</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>b</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>a</name></param>
#        </command>
#        
__glColorMaski_impl=None
def glColorMaski (index, r, g, b, a):
    global __glColorMaski_impl
    if not __glColorMaski_impl:
        fptr = __pyglGetFuncAddress('glColorMaski')
        if not fptr:
            raise RuntimeError('The function glColorMaski is not available')
        __glColorMaski_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_char, c_char, c_char, c_char)(fptr)
    glColorMaski = __glColorMaski_impl
    return glColorMaski(index, r, g, b, a)
# <command>
#            <proto>void <name>glCompileShader</name></proto>
#            <param><ptype>GLuint</ptype> <name>shader</name></param>
#        </command>
#        
__glCompileShader_impl=None
def glCompileShader (shader):
    global __glCompileShader_impl
    if not __glCompileShader_impl:
        fptr = __pyglGetFuncAddress('glCompileShader')
        if not fptr:
            raise RuntimeError('The function glCompileShader is not available')
        __glCompileShader_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glCompileShader = __glCompileShader_impl
    return glCompileShader(shader)
# <command>
#            <proto>void <name>glCompressedTexImage1D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="PixelInternalFormat"><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>border</name></param>
#            <param><ptype>GLsizei</ptype> <name>imageSize</name></param>
#            <param group="CompressedTextureARB" len="imageSize">const void *<name>data</name></param>
#            <glx opcode="214" type="render" />
#            <glx comment="PBO protocol" name="glCompressedTexImage1DPBO" opcode="314" type="render" />
#        </command>
#        
__glCompressedTexImage1D_impl=None
def glCompressedTexImage1D (target, level, internalformat, width, border, imageSize, data):
    global __glCompressedTexImage1D_impl
    if not __glCompressedTexImage1D_impl:
        fptr = __pyglGetFuncAddress('glCompressedTexImage1D')
        if not fptr:
            raise RuntimeError('The function glCompressedTexImage1D is not available')
        __glCompressedTexImage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int, c_int, c_void_p)(fptr)
    glCompressedTexImage1D = (lambda target,level,internalformat,width,border,imageSize,data:__glCompressedTexImage1D_impl(target,level,internalformat,width,border,imageSize,__pyglGetAsConstVoidPointer( data )))
    return glCompressedTexImage1D(target, level, internalformat, width, border, imageSize, data)
# <command>
#            <proto>void <name>glCompressedTexImage2D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="PixelInternalFormat"><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>border</name></param>
#            <param><ptype>GLsizei</ptype> <name>imageSize</name></param>
#            <param group="CompressedTextureARB" len="imageSize">const void *<name>data</name></param>
#            <glx opcode="215" type="render" />
#            <glx comment="PBO protocol" name="glCompressedTexImage2DPBO" opcode="315" type="render" />
#        </command>
#        
__glCompressedTexImage2D_impl=None
def glCompressedTexImage2D (target, level, internalformat, width, height, border, imageSize, data):
    global __glCompressedTexImage2D_impl
    if not __glCompressedTexImage2D_impl:
        fptr = __pyglGetFuncAddress('glCompressedTexImage2D')
        if not fptr:
            raise RuntimeError('The function glCompressedTexImage2D is not available')
        __glCompressedTexImage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int, c_int, c_int, c_void_p)(fptr)
    glCompressedTexImage2D = (lambda target,level,internalformat,width,height,border,imageSize,data:__glCompressedTexImage2D_impl(target,level,internalformat,width,height,border,imageSize,__pyglGetAsConstVoidPointer( data )))
    return glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, data)
# <command>
#            <proto>void <name>glCompressedTexImage3D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="PixelInternalFormat"><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>border</name></param>
#            <param><ptype>GLsizei</ptype> <name>imageSize</name></param>
#            <param group="CompressedTextureARB" len="imageSize">const void *<name>data</name></param>
#            <glx opcode="216" type="render" />
#            <glx comment="PBO protocol" name="glCompressedTexImage3DPBO" opcode="316" type="render" />
#        </command>
#        
__glCompressedTexImage3D_impl=None
def glCompressedTexImage3D (target, level, internalformat, width, height, depth, border, imageSize, data):
    global __glCompressedTexImage3D_impl
    if not __glCompressedTexImage3D_impl:
        fptr = __pyglGetFuncAddress('glCompressedTexImage3D')
        if not fptr:
            raise RuntimeError('The function glCompressedTexImage3D is not available')
        __glCompressedTexImage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int, c_int, c_int, c_int, c_void_p)(fptr)
    glCompressedTexImage3D = (lambda target,level,internalformat,width,height,depth,border,imageSize,data:__glCompressedTexImage3D_impl(target,level,internalformat,width,height,depth,border,imageSize,__pyglGetAsConstVoidPointer( data )))
    return glCompressedTexImage3D(target, level, internalformat, width, height, depth, border, imageSize, data)
# <command>
#            <proto>void <name>glCompressedTexSubImage1D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLsizei</ptype> <name>imageSize</name></param>
#            <param group="CompressedTextureARB" len="imageSize">const void *<name>data</name></param>
#            <glx opcode="217" type="render" />
#            <glx comment="PBO protocol" name="glCompressedTexSubImage1DPBO" opcode="317" type="render" />
#        </command>
#        
__glCompressedTexSubImage1D_impl=None
def glCompressedTexSubImage1D (target, level, xoffset, width, format, imageSize, data):
    global __glCompressedTexSubImage1D_impl
    if not __glCompressedTexSubImage1D_impl:
        fptr = __pyglGetFuncAddress('glCompressedTexSubImage1D')
        if not fptr:
            raise RuntimeError('The function glCompressedTexSubImage1D is not available')
        __glCompressedTexSubImage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_uint, c_int, c_void_p)(fptr)
    glCompressedTexSubImage1D = (lambda target,level,xoffset,width,format,imageSize,data:__glCompressedTexSubImage1D_impl(target,level,xoffset,width,format,imageSize,__pyglGetAsConstVoidPointer( data )))
    return glCompressedTexSubImage1D(target, level, xoffset, width, format, imageSize, data)
# <command>
#            <proto>void <name>glCompressedTexSubImage2D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLsizei</ptype> <name>imageSize</name></param>
#            <param group="CompressedTextureARB" len="imageSize">const void *<name>data</name></param>
#            <glx opcode="218" type="render" />
#            <glx comment="PBO protocol" name="glCompressedTexSubImage2DPBO" opcode="318" type="render" />
#        </command>
#        
__glCompressedTexSubImage2D_impl=None
def glCompressedTexSubImage2D (target, level, xoffset, yoffset, width, height, format, imageSize, data):
    global __glCompressedTexSubImage2D_impl
    if not __glCompressedTexSubImage2D_impl:
        fptr = __pyglGetFuncAddress('glCompressedTexSubImage2D')
        if not fptr:
            raise RuntimeError('The function glCompressedTexSubImage2D is not available')
        __glCompressedTexSubImage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_uint, c_int, c_void_p)(fptr)
    glCompressedTexSubImage2D = (lambda target,level,xoffset,yoffset,width,height,format,imageSize,data:__glCompressedTexSubImage2D_impl(target,level,xoffset,yoffset,width,height,format,imageSize,__pyglGetAsConstVoidPointer( data )))
    return glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, data)
# <command>
#            <proto>void <name>glCompressedTexSubImage3D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLsizei</ptype> <name>imageSize</name></param>
#            <param group="CompressedTextureARB" len="imageSize">const void *<name>data</name></param>
#            <glx opcode="219" type="render" />
#            <glx comment="PBO protocol" name="glCompressedTexSubImage3DPBO" opcode="319" type="render" />
#        </command>
#        
__glCompressedTexSubImage3D_impl=None
def glCompressedTexSubImage3D (target, level, xoffset, yoffset, zoffset, width, height, depth, format, imageSize, data):
    global __glCompressedTexSubImage3D_impl
    if not __glCompressedTexSubImage3D_impl:
        fptr = __pyglGetFuncAddress('glCompressedTexSubImage3D')
        if not fptr:
            raise RuntimeError('The function glCompressedTexSubImage3D is not available')
        __glCompressedTexSubImage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_int, c_void_p)(fptr)
    glCompressedTexSubImage3D = (lambda target,level,xoffset,yoffset,zoffset,width,height,depth,format,imageSize,data:__glCompressedTexSubImage3D_impl(target,level,xoffset,yoffset,zoffset,width,height,depth,format,imageSize,__pyglGetAsConstVoidPointer( data )))
    return glCompressedTexSubImage3D(target, level, xoffset, yoffset, zoffset, width, height, depth, format, imageSize, data)
# <command>
#            <proto>void <name>glCompressedTextureSubImage1D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLsizei</ptype> <name>imageSize</name></param>
#            <param>const void *<name>data</name></param>
#        </command>
#        
__glCompressedTextureSubImage1D_impl=None
def glCompressedTextureSubImage1D (texture, level, xoffset, width, format, imageSize, data):
    global __glCompressedTextureSubImage1D_impl
    if not __glCompressedTextureSubImage1D_impl:
        fptr = __pyglGetFuncAddress('glCompressedTextureSubImage1D')
        if not fptr:
            raise RuntimeError('The function glCompressedTextureSubImage1D is not available')
        __glCompressedTextureSubImage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_uint, c_int, c_void_p)(fptr)
    glCompressedTextureSubImage1D = (lambda texture,level,xoffset,width,format,imageSize,data:__glCompressedTextureSubImage1D_impl(texture,level,xoffset,width,format,imageSize,__pyglGetAsConstVoidPointer( data )))
    return glCompressedTextureSubImage1D(texture, level, xoffset, width, format, imageSize, data)
# <command>
#            <proto>void <name>glCompressedTextureSubImage2D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLsizei</ptype> <name>imageSize</name></param>
#            <param>const void *<name>data</name></param>
#        </command>
#        
__glCompressedTextureSubImage2D_impl=None
def glCompressedTextureSubImage2D (texture, level, xoffset, yoffset, width, height, format, imageSize, data):
    global __glCompressedTextureSubImage2D_impl
    if not __glCompressedTextureSubImage2D_impl:
        fptr = __pyglGetFuncAddress('glCompressedTextureSubImage2D')
        if not fptr:
            raise RuntimeError('The function glCompressedTextureSubImage2D is not available')
        __glCompressedTextureSubImage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_uint, c_int, c_void_p)(fptr)
    glCompressedTextureSubImage2D = (lambda texture,level,xoffset,yoffset,width,height,format,imageSize,data:__glCompressedTextureSubImage2D_impl(texture,level,xoffset,yoffset,width,height,format,imageSize,__pyglGetAsConstVoidPointer( data )))
    return glCompressedTextureSubImage2D(texture, level, xoffset, yoffset, width, height, format, imageSize, data)
# <command>
#            <proto>void <name>glCompressedTextureSubImage3D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLsizei</ptype> <name>imageSize</name></param>
#            <param>const void *<name>data</name></param>
#        </command>
#        
__glCompressedTextureSubImage3D_impl=None
def glCompressedTextureSubImage3D (texture, level, xoffset, yoffset, zoffset, width, height, depth, format, imageSize, data):
    global __glCompressedTextureSubImage3D_impl
    if not __glCompressedTextureSubImage3D_impl:
        fptr = __pyglGetFuncAddress('glCompressedTextureSubImage3D')
        if not fptr:
            raise RuntimeError('The function glCompressedTextureSubImage3D is not available')
        __glCompressedTextureSubImage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_int, c_void_p)(fptr)
    glCompressedTextureSubImage3D = (lambda texture,level,xoffset,yoffset,zoffset,width,height,depth,format,imageSize,data:__glCompressedTextureSubImage3D_impl(texture,level,xoffset,yoffset,zoffset,width,height,depth,format,imageSize,__pyglGetAsConstVoidPointer( data )))
    return glCompressedTextureSubImage3D(texture, level, xoffset, yoffset, zoffset, width, height, depth, format, imageSize, data)
# <command>
#            <proto>void <name>glCopyBufferSubData</name></proto>
#            <param><ptype>GLenum</ptype> <name>readTarget</name></param>
#            <param><ptype>GLenum</ptype> <name>writeTarget</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>readOffset</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>writeOffset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#        </command>
#        
__glCopyBufferSubData_impl=None
def glCopyBufferSubData (readTarget, writeTarget, readOffset, writeOffset, size):
    global __glCopyBufferSubData_impl
    if not __glCopyBufferSubData_impl:
        fptr = __pyglGetFuncAddress('glCopyBufferSubData')
        if not fptr:
            raise RuntimeError('The function glCopyBufferSubData is not available')
        __glCopyBufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_size_t, c_size_t, c_void_p)(fptr)
    glCopyBufferSubData = __glCopyBufferSubData_impl
    return glCopyBufferSubData(readTarget, writeTarget, readOffset, writeOffset, size)
# <command>
#            <proto>void <name>glCopyImageSubData</name></proto>
#            <param><ptype>GLuint</ptype> <name>srcName</name></param>
#            <param><ptype>GLenum</ptype> <name>srcTarget</name></param>
#            <param><ptype>GLint</ptype> <name>srcLevel</name></param>
#            <param><ptype>GLint</ptype> <name>srcX</name></param>
#            <param><ptype>GLint</ptype> <name>srcY</name></param>
#            <param><ptype>GLint</ptype> <name>srcZ</name></param>
#            <param><ptype>GLuint</ptype> <name>dstName</name></param>
#            <param><ptype>GLenum</ptype> <name>dstTarget</name></param>
#            <param><ptype>GLint</ptype> <name>dstLevel</name></param>
#            <param><ptype>GLint</ptype> <name>dstX</name></param>
#            <param><ptype>GLint</ptype> <name>dstY</name></param>
#            <param><ptype>GLint</ptype> <name>dstZ</name></param>
#            <param><ptype>GLsizei</ptype> <name>srcWidth</name></param>
#            <param><ptype>GLsizei</ptype> <name>srcHeight</name></param>
#            <param><ptype>GLsizei</ptype> <name>srcDepth</name></param>
#        </command>
#        
__glCopyImageSubData_impl=None
def glCopyImageSubData (srcName, srcTarget, srcLevel, srcX, srcY, srcZ, dstName, dstTarget, dstLevel, dstX, dstY, dstZ, srcWidth, srcHeight, srcDepth):
    global __glCopyImageSubData_impl
    if not __glCopyImageSubData_impl:
        fptr = __pyglGetFuncAddress('glCopyImageSubData')
        if not fptr:
            raise RuntimeError('The function glCopyImageSubData is not available')
        __glCopyImageSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_int, c_int, c_int, c_uint, c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int)(fptr)
    glCopyImageSubData = __glCopyImageSubData_impl
    return glCopyImageSubData(srcName, srcTarget, srcLevel, srcX, srcY, srcZ, dstName, dstTarget, dstLevel, dstX, dstY, dstZ, srcWidth, srcHeight, srcDepth)
# <command>
#            <proto>void <name>glCopyNamedBufferSubData</name></proto>
#            <param><ptype>GLuint</ptype> <name>readBuffer</name></param>
#            <param><ptype>GLuint</ptype> <name>writeBuffer</name></param>
#            <param><ptype>GLintptr</ptype> <name>readOffset</name></param>
#            <param><ptype>GLintptr</ptype> <name>writeOffset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#        </command>
#        
__glCopyNamedBufferSubData_impl=None
def glCopyNamedBufferSubData (readBuffer, writeBuffer, readOffset, writeOffset, size):
    global __glCopyNamedBufferSubData_impl
    if not __glCopyNamedBufferSubData_impl:
        fptr = __pyglGetFuncAddress('glCopyNamedBufferSubData')
        if not fptr:
            raise RuntimeError('The function glCopyNamedBufferSubData is not available')
        __glCopyNamedBufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_size_t, c_size_t, c_void_p)(fptr)
    glCopyNamedBufferSubData = __glCopyNamedBufferSubData_impl
    return glCopyNamedBufferSubData(readBuffer, writeBuffer, readOffset, writeOffset, size)
# <command>
#            <proto>void <name>glCopyTexImage1D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="PixelInternalFormat"><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>x</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>border</name></param>
#            <glx opcode="4119" type="render" />
#        </command>
#        
__glCopyTexImage1D_impl=None
def glCopyTexImage1D (target, level, internalformat, x, y, width, border):
    global __glCopyTexImage1D_impl
    if not __glCopyTexImage1D_impl:
        fptr = __pyglGetFuncAddress('glCopyTexImage1D')
        if not fptr:
            raise RuntimeError('The function glCopyTexImage1D is not available')
        __glCopyTexImage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int, c_int, c_int)(fptr)
    glCopyTexImage1D = __glCopyTexImage1D_impl
    return glCopyTexImage1D(target, level, internalformat, x, y, width, border)
# <command>
#            <proto>void <name>glCopyTexImage2D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="PixelInternalFormat"><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>x</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>border</name></param>
#            <glx opcode="4120" type="render" />
#        </command>
#        
__glCopyTexImage2D_impl=None
def glCopyTexImage2D (target, level, internalformat, x, y, width, height, border):
    global __glCopyTexImage2D_impl
    if not __glCopyTexImage2D_impl:
        fptr = __pyglGetFuncAddress('glCopyTexImage2D')
        if not fptr:
            raise RuntimeError('The function glCopyTexImage2D is not available')
        __glCopyTexImage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int, c_int, c_int, c_int)(fptr)
    glCopyTexImage2D = __glCopyTexImage2D_impl
    return glCopyTexImage2D(target, level, internalformat, x, y, width, height, border)
# <command>
#            <proto>void <name>glCopyTexSubImage1D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>x</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <glx opcode="4121" type="render" />
#        </command>
#        
__glCopyTexSubImage1D_impl=None
def glCopyTexSubImage1D (target, level, xoffset, x, y, width):
    global __glCopyTexSubImage1D_impl
    if not __glCopyTexSubImage1D_impl:
        fptr = __pyglGetFuncAddress('glCopyTexSubImage1D')
        if not fptr:
            raise RuntimeError('The function glCopyTexSubImage1D is not available')
        __glCopyTexSubImage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int)(fptr)
    glCopyTexSubImage1D = __glCopyTexSubImage1D_impl
    return glCopyTexSubImage1D(target, level, xoffset, x, y, width)
# <command>
#            <proto>void <name>glCopyTexSubImage2D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>x</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <glx opcode="4122" type="render" />
#        </command>
#        
__glCopyTexSubImage2D_impl=None
def glCopyTexSubImage2D (target, level, xoffset, yoffset, x, y, width, height):
    global __glCopyTexSubImage2D_impl
    if not __glCopyTexSubImage2D_impl:
        fptr = __pyglGetFuncAddress('glCopyTexSubImage2D')
        if not fptr:
            raise RuntimeError('The function glCopyTexSubImage2D is not available')
        __glCopyTexSubImage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int)(fptr)
    glCopyTexSubImage2D = __glCopyTexSubImage2D_impl
    return glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height)
# <command>
#            <proto>void <name>glCopyTexSubImage3D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>x</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <glx opcode="4123" type="render" />
#        </command>
#        
__glCopyTexSubImage3D_impl=None
def glCopyTexSubImage3D (target, level, xoffset, yoffset, zoffset, x, y, width, height):
    global __glCopyTexSubImage3D_impl
    if not __glCopyTexSubImage3D_impl:
        fptr = __pyglGetFuncAddress('glCopyTexSubImage3D')
        if not fptr:
            raise RuntimeError('The function glCopyTexSubImage3D is not available')
        __glCopyTexSubImage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int)(fptr)
    glCopyTexSubImage3D = __glCopyTexSubImage3D_impl
    return glCopyTexSubImage3D(target, level, xoffset, yoffset, zoffset, x, y, width, height)
# <command>
#            <proto>void <name>glCopyTextureSubImage1D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <param><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#        </command>
#        
__glCopyTextureSubImage1D_impl=None
def glCopyTextureSubImage1D (texture, level, xoffset, x, y, width):
    global __glCopyTextureSubImage1D_impl
    if not __glCopyTextureSubImage1D_impl:
        fptr = __pyglGetFuncAddress('glCopyTextureSubImage1D')
        if not fptr:
            raise RuntimeError('The function glCopyTextureSubImage1D is not available')
        __glCopyTextureSubImage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int)(fptr)
    glCopyTextureSubImage1D = __glCopyTextureSubImage1D_impl
    return glCopyTextureSubImage1D(texture, level, xoffset, x, y, width)
# <command>
#            <proto>void <name>glCopyTextureSubImage2D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <param><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#        </command>
#        
__glCopyTextureSubImage2D_impl=None
def glCopyTextureSubImage2D (texture, level, xoffset, yoffset, x, y, width, height):
    global __glCopyTextureSubImage2D_impl
    if not __glCopyTextureSubImage2D_impl:
        fptr = __pyglGetFuncAddress('glCopyTextureSubImage2D')
        if not fptr:
            raise RuntimeError('The function glCopyTextureSubImage2D is not available')
        __glCopyTextureSubImage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int)(fptr)
    glCopyTextureSubImage2D = __glCopyTextureSubImage2D_impl
    return glCopyTextureSubImage2D(texture, level, xoffset, yoffset, x, y, width, height)
# <command>
#            <proto>void <name>glCopyTextureSubImage3D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <param><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#        </command>
#        
__glCopyTextureSubImage3D_impl=None
def glCopyTextureSubImage3D (texture, level, xoffset, yoffset, zoffset, x, y, width, height):
    global __glCopyTextureSubImage3D_impl
    if not __glCopyTextureSubImage3D_impl:
        fptr = __pyglGetFuncAddress('glCopyTextureSubImage3D')
        if not fptr:
            raise RuntimeError('The function glCopyTextureSubImage3D is not available')
        __glCopyTextureSubImage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int)(fptr)
    glCopyTextureSubImage3D = __glCopyTextureSubImage3D_impl
    return glCopyTextureSubImage3D(texture, level, xoffset, yoffset, zoffset, x, y, width, height)
# <command>
#            <proto>void <name>glCreateBuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param><ptype>GLuint</ptype> *<name>buffers</name></param>
#        </command>
#        
__glCreateBuffers_impl=None
def glCreateBuffers (n, buffers):
    global __glCreateBuffers_impl
    if not __glCreateBuffers_impl:
        fptr = __pyglGetFuncAddress('glCreateBuffers')
        if not fptr:
            raise RuntimeError('The function glCreateBuffers is not available')
        __glCreateBuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glCreateBuffers = (lambda n,buffers:__glCreateBuffers_impl(n,(c_uint8*len( buffers )).from_buffer( buffers )))
    return glCreateBuffers(n, buffers)
# <command>
#            <proto>void <name>glCreateFramebuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param><ptype>GLuint</ptype> *<name>framebuffers</name></param>
#        </command>
#        
__glCreateFramebuffers_impl=None
def glCreateFramebuffers (n, framebuffers):
    global __glCreateFramebuffers_impl
    if not __glCreateFramebuffers_impl:
        fptr = __pyglGetFuncAddress('glCreateFramebuffers')
        if not fptr:
            raise RuntimeError('The function glCreateFramebuffers is not available')
        __glCreateFramebuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glCreateFramebuffers = (lambda n,framebuffers:__glCreateFramebuffers_impl(n,(c_uint8*len( framebuffers )).from_buffer( framebuffers )))
    return glCreateFramebuffers(n, framebuffers)
# <command>
#            <proto><ptype>GLuint</ptype> <name>glCreateProgram</name></proto>
#        </command>
#        
__glCreateProgram_impl=None
def glCreateProgram ():
    global __glCreateProgram_impl
    if not __glCreateProgram_impl:
        fptr = __pyglGetFuncAddress('glCreateProgram')
        if not fptr:
            raise RuntimeError('The function glCreateProgram is not available')
        __glCreateProgram_impl = __PYGL_FUNC_TYPE( c_uint ,)(fptr)
    glCreateProgram = __glCreateProgram_impl
    return glCreateProgram()
# <command>
#            <proto>void <name>glCreateProgramPipelines</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param><ptype>GLuint</ptype> *<name>pipelines</name></param>
#        </command>
#        
__glCreateProgramPipelines_impl=None
def glCreateProgramPipelines (n, pipelines):
    global __glCreateProgramPipelines_impl
    if not __glCreateProgramPipelines_impl:
        fptr = __pyglGetFuncAddress('glCreateProgramPipelines')
        if not fptr:
            raise RuntimeError('The function glCreateProgramPipelines is not available')
        __glCreateProgramPipelines_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glCreateProgramPipelines = (lambda n,pipelines:__glCreateProgramPipelines_impl(n,(c_uint8*len( pipelines )).from_buffer( pipelines )))
    return glCreateProgramPipelines(n, pipelines)
# <command>
#            <proto>void <name>glCreateQueries</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param><ptype>GLuint</ptype> *<name>ids</name></param>
#        </command>
#        
__glCreateQueries_impl=None
def glCreateQueries (target, n, ids):
    global __glCreateQueries_impl
    if not __glCreateQueries_impl:
        fptr = __pyglGetFuncAddress('glCreateQueries')
        if not fptr:
            raise RuntimeError('The function glCreateQueries is not available')
        __glCreateQueries_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glCreateQueries = (lambda target,n,ids:__glCreateQueries_impl(target,n,(c_uint8*len( ids )).from_buffer( ids )))
    return glCreateQueries(target, n, ids)
# <command>
#            <proto>void <name>glCreateRenderbuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param><ptype>GLuint</ptype> *<name>renderbuffers</name></param>
#        </command>
#        
__glCreateRenderbuffers_impl=None
def glCreateRenderbuffers (n, renderbuffers):
    global __glCreateRenderbuffers_impl
    if not __glCreateRenderbuffers_impl:
        fptr = __pyglGetFuncAddress('glCreateRenderbuffers')
        if not fptr:
            raise RuntimeError('The function glCreateRenderbuffers is not available')
        __glCreateRenderbuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glCreateRenderbuffers = (lambda n,renderbuffers:__glCreateRenderbuffers_impl(n,(c_uint8*len( renderbuffers )).from_buffer( renderbuffers )))
    return glCreateRenderbuffers(n, renderbuffers)
# <command>
#            <proto>void <name>glCreateSamplers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param><ptype>GLuint</ptype> *<name>samplers</name></param>
#        </command>
#        
__glCreateSamplers_impl=None
def glCreateSamplers (n, samplers):
    global __glCreateSamplers_impl
    if not __glCreateSamplers_impl:
        fptr = __pyglGetFuncAddress('glCreateSamplers')
        if not fptr:
            raise RuntimeError('The function glCreateSamplers is not available')
        __glCreateSamplers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glCreateSamplers = (lambda n,samplers:__glCreateSamplers_impl(n,(c_uint8*len( samplers )).from_buffer( samplers )))
    return glCreateSamplers(n, samplers)
# <command>
#            <proto><ptype>GLuint</ptype> <name>glCreateShader</name></proto>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#        </command>
#        
__glCreateShader_impl=None
def glCreateShader (type):
    global __glCreateShader_impl
    if not __glCreateShader_impl:
        fptr = __pyglGetFuncAddress('glCreateShader')
        if not fptr:
            raise RuntimeError('The function glCreateShader is not available')
        __glCreateShader_impl = __PYGL_FUNC_TYPE( c_uint ,c_uint)(fptr)
    glCreateShader = __glCreateShader_impl
    return glCreateShader(type)
# <command>
#            <proto><ptype>GLuint</ptype> <name>glCreateShaderProgramv</name></proto>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLchar</ptype> *const*<name>strings</name></param>
#        </command>
#        
__glCreateShaderProgramv_impl=None
def glCreateShaderProgramv (type, count, strings):
    global __glCreateShaderProgramv_impl
    if not __glCreateShaderProgramv_impl:
        fptr = __pyglGetFuncAddress('glCreateShaderProgramv')
        if not fptr:
            raise RuntimeError('The function glCreateShaderProgramv is not available')
        __glCreateShaderProgramv_impl = __PYGL_FUNC_TYPE( c_uint ,c_uint, c_int, c_void_p)(fptr)
    glCreateShaderProgramv = (lambda type,count,strings:__glCreateShaderProgramv_impl(type,count,c_char_p( strings .encode() )))
    return glCreateShaderProgramv(type, count, strings)
# <command>
#            <proto>void <name>glCreateTextures</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param><ptype>GLuint</ptype> *<name>textures</name></param>
#        </command>
#        
__glCreateTextures_impl=None
def glCreateTextures (target, n, textures):
    global __glCreateTextures_impl
    if not __glCreateTextures_impl:
        fptr = __pyglGetFuncAddress('glCreateTextures')
        if not fptr:
            raise RuntimeError('The function glCreateTextures is not available')
        __glCreateTextures_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glCreateTextures = (lambda target,n,textures:__glCreateTextures_impl(target,n,(c_uint8*len( textures )).from_buffer( textures )))
    return glCreateTextures(target, n, textures)
# <command>
#            <proto>void <name>glCreateTransformFeedbacks</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param><ptype>GLuint</ptype> *<name>ids</name></param>
#        </command>
#        
__glCreateTransformFeedbacks_impl=None
def glCreateTransformFeedbacks (n, ids):
    global __glCreateTransformFeedbacks_impl
    if not __glCreateTransformFeedbacks_impl:
        fptr = __pyglGetFuncAddress('glCreateTransformFeedbacks')
        if not fptr:
            raise RuntimeError('The function glCreateTransformFeedbacks is not available')
        __glCreateTransformFeedbacks_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glCreateTransformFeedbacks = (lambda n,ids:__glCreateTransformFeedbacks_impl(n,(c_uint8*len( ids )).from_buffer( ids )))
    return glCreateTransformFeedbacks(n, ids)
# <command>
#            <proto>void <name>glCreateVertexArrays</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param><ptype>GLuint</ptype> *<name>arrays</name></param>
#        </command>
#        
__glCreateVertexArrays_impl=None
def glCreateVertexArrays (n, arrays):
    global __glCreateVertexArrays_impl
    if not __glCreateVertexArrays_impl:
        fptr = __pyglGetFuncAddress('glCreateVertexArrays')
        if not fptr:
            raise RuntimeError('The function glCreateVertexArrays is not available')
        __glCreateVertexArrays_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glCreateVertexArrays = (lambda n,arrays:__glCreateVertexArrays_impl(n,(c_uint8*len( arrays )).from_buffer( arrays )))
    return glCreateVertexArrays(n, arrays)
# <command>
#            <proto>void <name>glCullFace</name></proto>
#            <param group="CullFaceMode"><ptype>GLenum</ptype> <name>mode</name></param>
#            <glx opcode="79" type="render" />
#        </command>
#        
__glCullFace_impl=None
def glCullFace (mode):
    global __glCullFace_impl
    if not __glCullFace_impl:
        fptr = __pyglGetFuncAddress('glCullFace')
        if not fptr:
            raise RuntimeError('The function glCullFace is not available')
        __glCullFace_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glCullFace = __glCullFace_impl
    return glCullFace(mode)
# <command>
#            <proto>void <name>glDebugMessageControl</name></proto>
#            <param><ptype>GLenum</ptype> <name>source</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param><ptype>GLenum</ptype> <name>severity</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>ids</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>enabled</name></param>
#        </command>
#        
__glDebugMessageControl_impl=None
def glDebugMessageControl (source, type, severity, count, ids, enabled):
    global __glDebugMessageControl_impl
    if not __glDebugMessageControl_impl:
        fptr = __pyglGetFuncAddress('glDebugMessageControl')
        if not fptr:
            raise RuntimeError('The function glDebugMessageControl is not available')
        __glDebugMessageControl_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_void_p, c_char)(fptr)
    glDebugMessageControl = (lambda source,type,severity,count,ids,enabled:__glDebugMessageControl_impl(source,type,severity,count,__pyglGetAsConstVoidPointer( ids ),enabled))
    return glDebugMessageControl(source, type, severity, count, ids, enabled)
# <command>
#            <proto>void <name>glDebugMessageInsert</name></proto>
#            <param><ptype>GLenum</ptype> <name>source</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLenum</ptype> <name>severity</name></param>
#            <param><ptype>GLsizei</ptype> <name>length</name></param>
#            <param len="COMPSIZE(buf,length)">const <ptype>GLchar</ptype> *<name>buf</name></param>
#        </command>
#        
__glDebugMessageInsert_impl=None
def glDebugMessageInsert (source, type, id, severity, length, buf):
    global __glDebugMessageInsert_impl
    if not __glDebugMessageInsert_impl:
        fptr = __pyglGetFuncAddress('glDebugMessageInsert')
        if not fptr:
            raise RuntimeError('The function glDebugMessageInsert is not available')
        __glDebugMessageInsert_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_int, c_void_p)(fptr)
    glDebugMessageInsert = (lambda source,type,id,severity,length,buf:__glDebugMessageInsert_impl(source,type,id,severity,length,c_char_p( buf .encode() )))
    return glDebugMessageInsert(source, type, id, severity, length, buf)
# <command>
#            <proto>void <name>glDeleteBuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n">const <ptype>GLuint</ptype> *<name>buffers</name></param>
#        </command>
#        
__glDeleteBuffers_impl=None
def glDeleteBuffers (n, buffers):
    global __glDeleteBuffers_impl
    if not __glDeleteBuffers_impl:
        fptr = __pyglGetFuncAddress('glDeleteBuffers')
        if not fptr:
            raise RuntimeError('The function glDeleteBuffers is not available')
        __glDeleteBuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDeleteBuffers = (lambda n,buffers:__glDeleteBuffers_impl(n,__pyglGetAsConstVoidPointer( buffers )))
    return glDeleteBuffers(n, buffers)
# <command>
#            <proto>void <name>glDeleteFramebuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n">const <ptype>GLuint</ptype> *<name>framebuffers</name></param>
#            <glx opcode="4320" type="render" />
#        </command>
#        
__glDeleteFramebuffers_impl=None
def glDeleteFramebuffers (n, framebuffers):
    global __glDeleteFramebuffers_impl
    if not __glDeleteFramebuffers_impl:
        fptr = __pyglGetFuncAddress('glDeleteFramebuffers')
        if not fptr:
            raise RuntimeError('The function glDeleteFramebuffers is not available')
        __glDeleteFramebuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDeleteFramebuffers = (lambda n,framebuffers:__glDeleteFramebuffers_impl(n,__pyglGetAsConstVoidPointer( framebuffers )))
    return glDeleteFramebuffers(n, framebuffers)
# <command>
#            <proto>void <name>glDeleteProgram</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <glx opcode="202" type="single" />
#        </command>
#        
__glDeleteProgram_impl=None
def glDeleteProgram (program):
    global __glDeleteProgram_impl
    if not __glDeleteProgram_impl:
        fptr = __pyglGetFuncAddress('glDeleteProgram')
        if not fptr:
            raise RuntimeError('The function glDeleteProgram is not available')
        __glDeleteProgram_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glDeleteProgram = __glDeleteProgram_impl
    return glDeleteProgram(program)
# <command>
#            <proto>void <name>glDeleteProgramPipelines</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n">const <ptype>GLuint</ptype> *<name>pipelines</name></param>
#        </command>
#        
__glDeleteProgramPipelines_impl=None
def glDeleteProgramPipelines (n, pipelines):
    global __glDeleteProgramPipelines_impl
    if not __glDeleteProgramPipelines_impl:
        fptr = __pyglGetFuncAddress('glDeleteProgramPipelines')
        if not fptr:
            raise RuntimeError('The function glDeleteProgramPipelines is not available')
        __glDeleteProgramPipelines_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDeleteProgramPipelines = (lambda n,pipelines:__glDeleteProgramPipelines_impl(n,__pyglGetAsConstVoidPointer( pipelines )))
    return glDeleteProgramPipelines(n, pipelines)
# <command>
#            <proto>void <name>glDeleteQueries</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n">const <ptype>GLuint</ptype> *<name>ids</name></param>
#            <glx opcode="161" type="single" />
#        </command>
#        
__glDeleteQueries_impl=None
def glDeleteQueries (n, ids):
    global __glDeleteQueries_impl
    if not __glDeleteQueries_impl:
        fptr = __pyglGetFuncAddress('glDeleteQueries')
        if not fptr:
            raise RuntimeError('The function glDeleteQueries is not available')
        __glDeleteQueries_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDeleteQueries = (lambda n,ids:__glDeleteQueries_impl(n,__pyglGetAsConstVoidPointer( ids )))
    return glDeleteQueries(n, ids)
# <command>
#            <proto>void <name>glDeleteRenderbuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n">const <ptype>GLuint</ptype> *<name>renderbuffers</name></param>
#            <glx opcode="4317" type="render" />
#        </command>
#        
__glDeleteRenderbuffers_impl=None
def glDeleteRenderbuffers (n, renderbuffers):
    global __glDeleteRenderbuffers_impl
    if not __glDeleteRenderbuffers_impl:
        fptr = __pyglGetFuncAddress('glDeleteRenderbuffers')
        if not fptr:
            raise RuntimeError('The function glDeleteRenderbuffers is not available')
        __glDeleteRenderbuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDeleteRenderbuffers = (lambda n,renderbuffers:__glDeleteRenderbuffers_impl(n,__pyglGetAsConstVoidPointer( renderbuffers )))
    return glDeleteRenderbuffers(n, renderbuffers)
# <command>
#            <proto>void <name>glDeleteSamplers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>samplers</name></param>
#        </command>
#        
__glDeleteSamplers_impl=None
def glDeleteSamplers (count, samplers):
    global __glDeleteSamplers_impl
    if not __glDeleteSamplers_impl:
        fptr = __pyglGetFuncAddress('glDeleteSamplers')
        if not fptr:
            raise RuntimeError('The function glDeleteSamplers is not available')
        __glDeleteSamplers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDeleteSamplers = (lambda count,samplers:__glDeleteSamplers_impl(count,__pyglGetAsConstVoidPointer( samplers )))
    return glDeleteSamplers(count, samplers)
# <command>
#            <proto>void <name>glDeleteShader</name></proto>
#            <param><ptype>GLuint</ptype> <name>shader</name></param>
#            <glx opcode="195" type="single" />
#        </command>
#        
__glDeleteShader_impl=None
def glDeleteShader (shader):
    global __glDeleteShader_impl
    if not __glDeleteShader_impl:
        fptr = __pyglGetFuncAddress('glDeleteShader')
        if not fptr:
            raise RuntimeError('The function glDeleteShader is not available')
        __glDeleteShader_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glDeleteShader = __glDeleteShader_impl
    return glDeleteShader(shader)
# <command>
#            <proto>void <name>glDeleteSync</name></proto>
#            <param group="sync"><ptype>GLsync</ptype> <name>sync</name></param>
#        </command>
#        
__glDeleteSync_impl=None
def glDeleteSync (sync):
    global __glDeleteSync_impl
    if not __glDeleteSync_impl:
        fptr = __pyglGetFuncAddress('glDeleteSync')
        if not fptr:
            raise RuntimeError('The function glDeleteSync is not available')
        __glDeleteSync_impl = __PYGL_FUNC_TYPE( None ,c_void_p)(fptr)
    glDeleteSync = __glDeleteSync_impl
    return glDeleteSync(sync)
# <command>
#            <proto>void <name>glDeleteTextures</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param group="Texture" len="n">const <ptype>GLuint</ptype> *<name>textures</name></param>
#            <glx opcode="144" type="single" />
#        </command>
#        
__glDeleteTextures_impl=None
def glDeleteTextures (n, textures):
    global __glDeleteTextures_impl
    if not __glDeleteTextures_impl:
        fptr = __pyglGetFuncAddress('glDeleteTextures')
        if not fptr:
            raise RuntimeError('The function glDeleteTextures is not available')
        __glDeleteTextures_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDeleteTextures = (lambda n,textures:__glDeleteTextures_impl(n,__pyglGetAsConstVoidPointer( textures )))
    return glDeleteTextures(n, textures)
# <command>
#            <proto>void <name>glDeleteTransformFeedbacks</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n">const <ptype>GLuint</ptype> *<name>ids</name></param>
#        </command>
#        
__glDeleteTransformFeedbacks_impl=None
def glDeleteTransformFeedbacks (n, ids):
    global __glDeleteTransformFeedbacks_impl
    if not __glDeleteTransformFeedbacks_impl:
        fptr = __pyglGetFuncAddress('glDeleteTransformFeedbacks')
        if not fptr:
            raise RuntimeError('The function glDeleteTransformFeedbacks is not available')
        __glDeleteTransformFeedbacks_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDeleteTransformFeedbacks = (lambda n,ids:__glDeleteTransformFeedbacks_impl(n,__pyglGetAsConstVoidPointer( ids )))
    return glDeleteTransformFeedbacks(n, ids)
# <command>
#            <proto>void <name>glDeleteVertexArrays</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n">const <ptype>GLuint</ptype> *<name>arrays</name></param>
#            <glx opcode="351" type="render" />
#        </command>
#        
__glDeleteVertexArrays_impl=None
def glDeleteVertexArrays (n, arrays):
    global __glDeleteVertexArrays_impl
    if not __glDeleteVertexArrays_impl:
        fptr = __pyglGetFuncAddress('glDeleteVertexArrays')
        if not fptr:
            raise RuntimeError('The function glDeleteVertexArrays is not available')
        __glDeleteVertexArrays_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDeleteVertexArrays = (lambda n,arrays:__glDeleteVertexArrays_impl(n,__pyglGetAsConstVoidPointer( arrays )))
    return glDeleteVertexArrays(n, arrays)
# <command>
#            <proto>void <name>glDepthFunc</name></proto>
#            <param group="DepthFunction"><ptype>GLenum</ptype> <name>func</name></param>
#            <glx opcode="164" type="render" />
#        </command>
#        
__glDepthFunc_impl=None
def glDepthFunc (func):
    global __glDepthFunc_impl
    if not __glDepthFunc_impl:
        fptr = __pyglGetFuncAddress('glDepthFunc')
        if not fptr:
            raise RuntimeError('The function glDepthFunc is not available')
        __glDepthFunc_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glDepthFunc = __glDepthFunc_impl
    return glDepthFunc(func)
# <command>
#            <proto>void <name>glDepthMask</name></proto>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>flag</name></param>
#            <glx opcode="135" type="render" />
#        </command>
#        
__glDepthMask_impl=None
def glDepthMask (flag):
    global __glDepthMask_impl
    if not __glDepthMask_impl:
        fptr = __pyglGetFuncAddress('glDepthMask')
        if not fptr:
            raise RuntimeError('The function glDepthMask is not available')
        __glDepthMask_impl = __PYGL_FUNC_TYPE( None ,c_char)(fptr)
    glDepthMask = __glDepthMask_impl
    return glDepthMask(flag)
# <command>
#            <proto>void <name>glDepthRange</name></proto>
#            <param><ptype>GLdouble</ptype> <name>near</name></param>
#            <param><ptype>GLdouble</ptype> <name>far</name></param>
#            <glx opcode="174" type="render" />
#        </command>
#        
__glDepthRange_impl=None
def glDepthRange (near, far):
    global __glDepthRange_impl
    if not __glDepthRange_impl:
        fptr = __pyglGetFuncAddress('glDepthRange')
        if not fptr:
            raise RuntimeError('The function glDepthRange is not available')
        __glDepthRange_impl = __PYGL_FUNC_TYPE( None ,c_double, c_double)(fptr)
    glDepthRange = __glDepthRange_impl
    return glDepthRange(near, far)
# <command>
#            <proto>void <name>glDepthRangeArrayv</name></proto>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="COMPSIZE(count)">const <ptype>GLdouble</ptype> *<name>v</name></param>
#        </command>
#        
__glDepthRangeArrayv_impl=None
def glDepthRangeArrayv (first, count, v):
    global __glDepthRangeArrayv_impl
    if not __glDepthRangeArrayv_impl:
        fptr = __pyglGetFuncAddress('glDepthRangeArrayv')
        if not fptr:
            raise RuntimeError('The function glDepthRangeArrayv is not available')
        __glDepthRangeArrayv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glDepthRangeArrayv = (lambda first,count,v:__glDepthRangeArrayv_impl(first,count,__pyglGetAsConstVoidPointer( v )))
    return glDepthRangeArrayv(first, count, v)
# <command>
#            <proto>void <name>glDepthRangeIndexed</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLdouble</ptype> <name>n</name></param>
#            <param><ptype>GLdouble</ptype> <name>f</name></param>
#        </command>
#        
__glDepthRangeIndexed_impl=None
def glDepthRangeIndexed (index, n, f):
    global __glDepthRangeIndexed_impl
    if not __glDepthRangeIndexed_impl:
        fptr = __pyglGetFuncAddress('glDepthRangeIndexed')
        if not fptr:
            raise RuntimeError('The function glDepthRangeIndexed is not available')
        __glDepthRangeIndexed_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_double, c_double)(fptr)
    glDepthRangeIndexed = __glDepthRangeIndexed_impl
    return glDepthRangeIndexed(index, n, f)
# <command>
#            <proto>void <name>glDepthRangef</name></proto>
#            <param><ptype>GLfloat</ptype> <name>n</name></param>
#            <param><ptype>GLfloat</ptype> <name>f</name></param>
#        </command>
#        
__glDepthRangef_impl=None
def glDepthRangef (n, f):
    global __glDepthRangef_impl
    if not __glDepthRangef_impl:
        fptr = __pyglGetFuncAddress('glDepthRangef')
        if not fptr:
            raise RuntimeError('The function glDepthRangef is not available')
        __glDepthRangef_impl = __PYGL_FUNC_TYPE( None ,c_float, c_float)(fptr)
    glDepthRangef = __glDepthRangef_impl
    return glDepthRangef(n, f)
# <command>
#            <proto>void <name>glDetachShader</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>shader</name></param>
#        </command>
#        
__glDetachShader_impl=None
def glDetachShader (program, shader):
    global __glDetachShader_impl
    if not __glDetachShader_impl:
        fptr = __pyglGetFuncAddress('glDetachShader')
        if not fptr:
            raise RuntimeError('The function glDetachShader is not available')
        __glDetachShader_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glDetachShader = __glDetachShader_impl
    return glDetachShader(program, shader)
# <command>
#            <proto>void <name>glDisable</name></proto>
#            <param group="EnableCap"><ptype>GLenum</ptype> <name>cap</name></param>
#            <glx opcode="138" type="render" />
#        </command>
#        
__glDisable_impl=None
def glDisable (cap):
    global __glDisable_impl
    if not __glDisable_impl:
        fptr = __pyglGetFuncAddress('glDisable')
        if not fptr:
            raise RuntimeError('The function glDisable is not available')
        __glDisable_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glDisable = __glDisable_impl
    return glDisable(cap)
# <command>
#            <proto>void <name>glDisableVertexArrayAttrib</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glDisableVertexArrayAttrib_impl=None
def glDisableVertexArrayAttrib (vaobj, index):
    global __glDisableVertexArrayAttrib_impl
    if not __glDisableVertexArrayAttrib_impl:
        fptr = __pyglGetFuncAddress('glDisableVertexArrayAttrib')
        if not fptr:
            raise RuntimeError('The function glDisableVertexArrayAttrib is not available')
        __glDisableVertexArrayAttrib_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glDisableVertexArrayAttrib = __glDisableVertexArrayAttrib_impl
    return glDisableVertexArrayAttrib(vaobj, index)
# <command>
#            <proto>void <name>glDisableVertexAttribArray</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glDisableVertexAttribArray_impl=None
def glDisableVertexAttribArray (index):
    global __glDisableVertexAttribArray_impl
    if not __glDisableVertexAttribArray_impl:
        fptr = __pyglGetFuncAddress('glDisableVertexAttribArray')
        if not fptr:
            raise RuntimeError('The function glDisableVertexAttribArray is not available')
        __glDisableVertexAttribArray_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glDisableVertexAttribArray = __glDisableVertexAttribArray_impl
    return glDisableVertexAttribArray(index)
# <command>
#            <proto>void <name>glDisablei</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glDisablei_impl=None
def glDisablei (target, index):
    global __glDisablei_impl
    if not __glDisablei_impl:
        fptr = __pyglGetFuncAddress('glDisablei')
        if not fptr:
            raise RuntimeError('The function glDisablei is not available')
        __glDisablei_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glDisablei = __glDisablei_impl
    return glDisablei(target, index)
# <command>
#            <proto>void <name>glDispatchCompute</name></proto>
#            <param><ptype>GLuint</ptype> <name>num_groups_x</name></param>
#            <param><ptype>GLuint</ptype> <name>num_groups_y</name></param>
#            <param><ptype>GLuint</ptype> <name>num_groups_z</name></param>
#        </command>
#        
__glDispatchCompute_impl=None
def glDispatchCompute (num_groups_x, num_groups_y, num_groups_z):
    global __glDispatchCompute_impl
    if not __glDispatchCompute_impl:
        fptr = __pyglGetFuncAddress('glDispatchCompute')
        if not fptr:
            raise RuntimeError('The function glDispatchCompute is not available')
        __glDispatchCompute_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glDispatchCompute = __glDispatchCompute_impl
    return glDispatchCompute(num_groups_x, num_groups_y, num_groups_z)
# <command>
#            <proto>void <name>glDispatchComputeIndirect</name></proto>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>indirect</name></param>
#        </command>
#        
__glDispatchComputeIndirect_impl=None
def glDispatchComputeIndirect (indirect):
    global __glDispatchComputeIndirect_impl
    if not __glDispatchComputeIndirect_impl:
        fptr = __pyglGetFuncAddress('glDispatchComputeIndirect')
        if not fptr:
            raise RuntimeError('The function glDispatchComputeIndirect is not available')
        __glDispatchComputeIndirect_impl = __PYGL_FUNC_TYPE( None ,c_size_t)(fptr)
    glDispatchComputeIndirect = __glDispatchComputeIndirect_impl
    return glDispatchComputeIndirect(indirect)
# <command>
#            <proto>void <name>glDrawArrays</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <glx opcode="193" type="render" />
#        </command>
#        
__glDrawArrays_impl=None
def glDrawArrays (mode, first, count):
    global __glDrawArrays_impl
    if not __glDrawArrays_impl:
        fptr = __pyglGetFuncAddress('glDrawArrays')
        if not fptr:
            raise RuntimeError('The function glDrawArrays is not available')
        __glDrawArrays_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int)(fptr)
    glDrawArrays = __glDrawArrays_impl
    return glDrawArrays(mode, first, count)
# <command>
#            <proto>void <name>glDrawArraysIndirect</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param>const void *<name>indirect</name></param>
#        </command>
#        
__glDrawArraysIndirect_impl=None
def glDrawArraysIndirect (mode, indirect):
    global __glDrawArraysIndirect_impl
    if not __glDrawArraysIndirect_impl:
        fptr = __pyglGetFuncAddress('glDrawArraysIndirect')
        if not fptr:
            raise RuntimeError('The function glDrawArraysIndirect is not available')
        __glDrawArraysIndirect_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glDrawArraysIndirect = (lambda mode,indirect:__glDrawArraysIndirect_impl(mode,__pyglGetAsConstVoidPointer( indirect )))
    return glDrawArraysIndirect(mode, indirect)
# <command>
#            <proto>void <name>glDrawArraysInstanced</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param><ptype>GLsizei</ptype> <name>instancecount</name></param>
#        </command>
#        
__glDrawArraysInstanced_impl=None
def glDrawArraysInstanced (mode, first, count, instancecount):
    global __glDrawArraysInstanced_impl
    if not __glDrawArraysInstanced_impl:
        fptr = __pyglGetFuncAddress('glDrawArraysInstanced')
        if not fptr:
            raise RuntimeError('The function glDrawArraysInstanced is not available')
        __glDrawArraysInstanced_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int)(fptr)
    glDrawArraysInstanced = __glDrawArraysInstanced_impl
    return glDrawArraysInstanced(mode, first, count, instancecount)
# <command>
#            <proto>void <name>glDrawArraysInstancedBaseInstance</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param><ptype>GLsizei</ptype> <name>instancecount</name></param>
#            <param><ptype>GLuint</ptype> <name>baseinstance</name></param>
#        </command>
#        
__glDrawArraysInstancedBaseInstance_impl=None
def glDrawArraysInstancedBaseInstance (mode, first, count, instancecount, baseinstance):
    global __glDrawArraysInstancedBaseInstance_impl
    if not __glDrawArraysInstancedBaseInstance_impl:
        fptr = __pyglGetFuncAddress('glDrawArraysInstancedBaseInstance')
        if not fptr:
            raise RuntimeError('The function glDrawArraysInstancedBaseInstance is not available')
        __glDrawArraysInstancedBaseInstance_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_uint)(fptr)
    glDrawArraysInstancedBaseInstance = __glDrawArraysInstancedBaseInstance_impl
    return glDrawArraysInstancedBaseInstance(mode, first, count, instancecount, baseinstance)
# <command>
#            <proto>void <name>glDrawBuffer</name></proto>
#            <param group="DrawBufferMode"><ptype>GLenum</ptype> <name>buf</name></param>
#            <glx opcode="126" type="render" />
#        </command>
#        
__glDrawBuffer_impl=None
def glDrawBuffer (buf):
    global __glDrawBuffer_impl
    if not __glDrawBuffer_impl:
        fptr = __pyglGetFuncAddress('glDrawBuffer')
        if not fptr:
            raise RuntimeError('The function glDrawBuffer is not available')
        __glDrawBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glDrawBuffer = __glDrawBuffer_impl
    return glDrawBuffer(buf)
# <command>
#            <proto>void <name>glDrawBuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param group="DrawBufferModeATI" len="n">const <ptype>GLenum</ptype> *<name>bufs</name></param>
#            <glx opcode="233" type="render" />
#        </command>
#        
__glDrawBuffers_impl=None
def glDrawBuffers (n, bufs):
    global __glDrawBuffers_impl
    if not __glDrawBuffers_impl:
        fptr = __pyglGetFuncAddress('glDrawBuffers')
        if not fptr:
            raise RuntimeError('The function glDrawBuffers is not available')
        __glDrawBuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glDrawBuffers = (lambda n,bufs:__glDrawBuffers_impl(n,__pyglGetAsConstVoidPointer( bufs )))
    return glDrawBuffers(n, bufs)
# <command>
#            <proto>void <name>glDrawElements</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="DrawElementsType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(count,type)">const void *<name>indices</name></param>
#        </command>
#        
__glDrawElements_impl=None
def glDrawElements (mode, count, type, indices):
    global __glDrawElements_impl
    if not __glDrawElements_impl:
        fptr = __pyglGetFuncAddress('glDrawElements')
        if not fptr:
            raise RuntimeError('The function glDrawElements is not available')
        __glDrawElements_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p)(fptr)
    glDrawElements = __glDrawElements_impl
    return glDrawElements(mode, count, type, indices)
# <command>
#            <proto>void <name>glDrawElementsBaseVertex</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="DrawElementsType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(count,type)">const void *<name>indices</name></param>
#            <param><ptype>GLint</ptype> <name>basevertex</name></param>
#        </command>
#        
__glDrawElementsBaseVertex_impl=None
def glDrawElementsBaseVertex (mode, count, type, indices, basevertex):
    global __glDrawElementsBaseVertex_impl
    if not __glDrawElementsBaseVertex_impl:
        fptr = __pyglGetFuncAddress('glDrawElementsBaseVertex')
        if not fptr:
            raise RuntimeError('The function glDrawElementsBaseVertex is not available')
        __glDrawElementsBaseVertex_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p, c_int)(fptr)
    glDrawElementsBaseVertex = (lambda mode,count,type,indices,basevertex:__glDrawElementsBaseVertex_impl(mode,count,type,__pyglGetAsConstVoidPointer( indices ),basevertex))
    return glDrawElementsBaseVertex(mode, count, type, indices, basevertex)
# <command>
#            <proto>void <name>glDrawElementsIndirect</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param>const void *<name>indirect</name></param>
#        </command>
#        
__glDrawElementsIndirect_impl=None
def glDrawElementsIndirect (mode, type, indirect):
    global __glDrawElementsIndirect_impl
    if not __glDrawElementsIndirect_impl:
        fptr = __pyglGetFuncAddress('glDrawElementsIndirect')
        if not fptr:
            raise RuntimeError('The function glDrawElementsIndirect is not available')
        __glDrawElementsIndirect_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glDrawElementsIndirect = (lambda mode,type,indirect:__glDrawElementsIndirect_impl(mode,type,__pyglGetAsConstVoidPointer( indirect )))
    return glDrawElementsIndirect(mode, type, indirect)
# <command>
#            <proto>void <name>glDrawElementsInstanced</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="DrawElementsType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(count,type)">const void *<name>indices</name></param>
#            <param><ptype>GLsizei</ptype> <name>instancecount</name></param>
#        </command>
#        
__glDrawElementsInstanced_impl=None
def glDrawElementsInstanced (mode, count, type, indices, instancecount):
    global __glDrawElementsInstanced_impl
    if not __glDrawElementsInstanced_impl:
        fptr = __pyglGetFuncAddress('glDrawElementsInstanced')
        if not fptr:
            raise RuntimeError('The function glDrawElementsInstanced is not available')
        __glDrawElementsInstanced_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p, c_int)(fptr)
    glDrawElementsInstanced = (lambda mode,count,type,indices,instancecount:__glDrawElementsInstanced_impl(mode,count,type,__pyglGetAsConstVoidPointer( indices ),instancecount))
    return glDrawElementsInstanced(mode, count, type, indices, instancecount)
# <command>
#            <proto>void <name>glDrawElementsInstancedBaseInstance</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="count">const void *<name>indices</name></param>
#            <param><ptype>GLsizei</ptype> <name>instancecount</name></param>
#            <param><ptype>GLuint</ptype> <name>baseinstance</name></param>
#        </command>
#        
__glDrawElementsInstancedBaseInstance_impl=None
def glDrawElementsInstancedBaseInstance (mode, count, type, indices, instancecount, baseinstance):
    global __glDrawElementsInstancedBaseInstance_impl
    if not __glDrawElementsInstancedBaseInstance_impl:
        fptr = __pyglGetFuncAddress('glDrawElementsInstancedBaseInstance')
        if not fptr:
            raise RuntimeError('The function glDrawElementsInstancedBaseInstance is not available')
        __glDrawElementsInstancedBaseInstance_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p, c_int, c_uint)(fptr)
    glDrawElementsInstancedBaseInstance = (lambda mode,count,type,indices,instancecount,baseinstance:__glDrawElementsInstancedBaseInstance_impl(mode,count,type,__pyglGetAsConstVoidPointer( indices ),instancecount,baseinstance))
    return glDrawElementsInstancedBaseInstance(mode, count, type, indices, instancecount, baseinstance)
# <command>
#            <proto>void <name>glDrawElementsInstancedBaseVertex</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="DrawElementsType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(count,type)">const void *<name>indices</name></param>
#            <param><ptype>GLsizei</ptype> <name>instancecount</name></param>
#            <param><ptype>GLint</ptype> <name>basevertex</name></param>
#        </command>
#        
__glDrawElementsInstancedBaseVertex_impl=None
def glDrawElementsInstancedBaseVertex (mode, count, type, indices, instancecount, basevertex):
    global __glDrawElementsInstancedBaseVertex_impl
    if not __glDrawElementsInstancedBaseVertex_impl:
        fptr = __pyglGetFuncAddress('glDrawElementsInstancedBaseVertex')
        if not fptr:
            raise RuntimeError('The function glDrawElementsInstancedBaseVertex is not available')
        __glDrawElementsInstancedBaseVertex_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p, c_int, c_int)(fptr)
    glDrawElementsInstancedBaseVertex = (lambda mode,count,type,indices,instancecount,basevertex:__glDrawElementsInstancedBaseVertex_impl(mode,count,type,__pyglGetAsConstVoidPointer( indices ),instancecount,basevertex))
    return glDrawElementsInstancedBaseVertex(mode, count, type, indices, instancecount, basevertex)
# <command>
#            <proto>void <name>glDrawElementsInstancedBaseVertexBaseInstance</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="count">const void *<name>indices</name></param>
#            <param><ptype>GLsizei</ptype> <name>instancecount</name></param>
#            <param><ptype>GLint</ptype> <name>basevertex</name></param>
#            <param><ptype>GLuint</ptype> <name>baseinstance</name></param>
#        </command>
#        
__glDrawElementsInstancedBaseVertexBaseInstance_impl=None
def glDrawElementsInstancedBaseVertexBaseInstance (mode, count, type, indices, instancecount, basevertex, baseinstance):
    global __glDrawElementsInstancedBaseVertexBaseInstance_impl
    if not __glDrawElementsInstancedBaseVertexBaseInstance_impl:
        fptr = __pyglGetFuncAddress('glDrawElementsInstancedBaseVertexBaseInstance')
        if not fptr:
            raise RuntimeError('The function glDrawElementsInstancedBaseVertexBaseInstance is not available')
        __glDrawElementsInstancedBaseVertexBaseInstance_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p, c_int, c_int, c_uint)(fptr)
    glDrawElementsInstancedBaseVertexBaseInstance = (lambda mode,count,type,indices,instancecount,basevertex,baseinstance:__glDrawElementsInstancedBaseVertexBaseInstance_impl(mode,count,type,__pyglGetAsConstVoidPointer( indices ),instancecount,basevertex,baseinstance))
    return glDrawElementsInstancedBaseVertexBaseInstance(mode, count, type, indices, instancecount, basevertex, baseinstance)
# <command>
#            <proto>void <name>glDrawRangeElements</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLuint</ptype> <name>start</name></param>
#            <param><ptype>GLuint</ptype> <name>end</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="DrawElementsType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(count,type)">const void *<name>indices</name></param>
#        </command>
#        
__glDrawRangeElements_impl=None
def glDrawRangeElements (mode, start, end, count, type, indices):
    global __glDrawRangeElements_impl
    if not __glDrawRangeElements_impl:
        fptr = __pyglGetFuncAddress('glDrawRangeElements')
        if not fptr:
            raise RuntimeError('The function glDrawRangeElements is not available')
        __glDrawRangeElements_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_uint, c_void_p)(fptr)
    glDrawRangeElements = (lambda mode,start,end,count,type,indices:__glDrawRangeElements_impl(mode,start,end,count,type,__pyglGetAsConstVoidPointer( indices )))
    return glDrawRangeElements(mode, start, end, count, type, indices)
# <command>
#            <proto>void <name>glDrawRangeElementsBaseVertex</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLuint</ptype> <name>start</name></param>
#            <param><ptype>GLuint</ptype> <name>end</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="DrawElementsType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(count,type)">const void *<name>indices</name></param>
#            <param><ptype>GLint</ptype> <name>basevertex</name></param>
#        </command>
#        
__glDrawRangeElementsBaseVertex_impl=None
def glDrawRangeElementsBaseVertex (mode, start, end, count, type, indices, basevertex):
    global __glDrawRangeElementsBaseVertex_impl
    if not __glDrawRangeElementsBaseVertex_impl:
        fptr = __pyglGetFuncAddress('glDrawRangeElementsBaseVertex')
        if not fptr:
            raise RuntimeError('The function glDrawRangeElementsBaseVertex is not available')
        __glDrawRangeElementsBaseVertex_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_uint, c_void_p, c_int)(fptr)
    glDrawRangeElementsBaseVertex = (lambda mode,start,end,count,type,indices,basevertex:__glDrawRangeElementsBaseVertex_impl(mode,start,end,count,type,__pyglGetAsConstVoidPointer( indices ),basevertex))
    return glDrawRangeElementsBaseVertex(mode, start, end, count, type, indices, basevertex)
# <command>
#            <proto>void <name>glDrawTransformFeedback</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#        </command>
#        
__glDrawTransformFeedback_impl=None
def glDrawTransformFeedback (mode, id):
    global __glDrawTransformFeedback_impl
    if not __glDrawTransformFeedback_impl:
        fptr = __pyglGetFuncAddress('glDrawTransformFeedback')
        if not fptr:
            raise RuntimeError('The function glDrawTransformFeedback is not available')
        __glDrawTransformFeedback_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glDrawTransformFeedback = __glDrawTransformFeedback_impl
    return glDrawTransformFeedback(mode, id)
# <command>
#            <proto>void <name>glDrawTransformFeedbackInstanced</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLsizei</ptype> <name>instancecount</name></param>
#        </command>
#        
__glDrawTransformFeedbackInstanced_impl=None
def glDrawTransformFeedbackInstanced (mode, id, instancecount):
    global __glDrawTransformFeedbackInstanced_impl
    if not __glDrawTransformFeedbackInstanced_impl:
        fptr = __pyglGetFuncAddress('glDrawTransformFeedbackInstanced')
        if not fptr:
            raise RuntimeError('The function glDrawTransformFeedbackInstanced is not available')
        __glDrawTransformFeedbackInstanced_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int)(fptr)
    glDrawTransformFeedbackInstanced = __glDrawTransformFeedbackInstanced_impl
    return glDrawTransformFeedbackInstanced(mode, id, instancecount)
# <command>
#            <proto>void <name>glDrawTransformFeedbackStream</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLuint</ptype> <name>stream</name></param>
#        </command>
#        
__glDrawTransformFeedbackStream_impl=None
def glDrawTransformFeedbackStream (mode, id, stream):
    global __glDrawTransformFeedbackStream_impl
    if not __glDrawTransformFeedbackStream_impl:
        fptr = __pyglGetFuncAddress('glDrawTransformFeedbackStream')
        if not fptr:
            raise RuntimeError('The function glDrawTransformFeedbackStream is not available')
        __glDrawTransformFeedbackStream_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glDrawTransformFeedbackStream = __glDrawTransformFeedbackStream_impl
    return glDrawTransformFeedbackStream(mode, id, stream)
# <command>
#            <proto>void <name>glDrawTransformFeedbackStreamInstanced</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLuint</ptype> <name>stream</name></param>
#            <param><ptype>GLsizei</ptype> <name>instancecount</name></param>
#        </command>
#        
__glDrawTransformFeedbackStreamInstanced_impl=None
def glDrawTransformFeedbackStreamInstanced (mode, id, stream, instancecount):
    global __glDrawTransformFeedbackStreamInstanced_impl
    if not __glDrawTransformFeedbackStreamInstanced_impl:
        fptr = __pyglGetFuncAddress('glDrawTransformFeedbackStreamInstanced')
        if not fptr:
            raise RuntimeError('The function glDrawTransformFeedbackStreamInstanced is not available')
        __glDrawTransformFeedbackStreamInstanced_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int)(fptr)
    glDrawTransformFeedbackStreamInstanced = __glDrawTransformFeedbackStreamInstanced_impl
    return glDrawTransformFeedbackStreamInstanced(mode, id, stream, instancecount)
# <command>
#            <proto>void <name>glEnable</name></proto>
#            <param group="EnableCap"><ptype>GLenum</ptype> <name>cap</name></param>
#            <glx opcode="139" type="render" />
#        </command>
#        
__glEnable_impl=None
def glEnable (cap):
    global __glEnable_impl
    if not __glEnable_impl:
        fptr = __pyglGetFuncAddress('glEnable')
        if not fptr:
            raise RuntimeError('The function glEnable is not available')
        __glEnable_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glEnable = __glEnable_impl
    return glEnable(cap)
# <command>
#            <proto>void <name>glEnableVertexArrayAttrib</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glEnableVertexArrayAttrib_impl=None
def glEnableVertexArrayAttrib (vaobj, index):
    global __glEnableVertexArrayAttrib_impl
    if not __glEnableVertexArrayAttrib_impl:
        fptr = __pyglGetFuncAddress('glEnableVertexArrayAttrib')
        if not fptr:
            raise RuntimeError('The function glEnableVertexArrayAttrib is not available')
        __glEnableVertexArrayAttrib_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glEnableVertexArrayAttrib = __glEnableVertexArrayAttrib_impl
    return glEnableVertexArrayAttrib(vaobj, index)
# <command>
#            <proto>void <name>glEnableVertexAttribArray</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glEnableVertexAttribArray_impl=None
def glEnableVertexAttribArray (index):
    global __glEnableVertexAttribArray_impl
    if not __glEnableVertexAttribArray_impl:
        fptr = __pyglGetFuncAddress('glEnableVertexAttribArray')
        if not fptr:
            raise RuntimeError('The function glEnableVertexAttribArray is not available')
        __glEnableVertexAttribArray_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glEnableVertexAttribArray = __glEnableVertexAttribArray_impl
    return glEnableVertexAttribArray(index)
# <command>
#            <proto>void <name>glEnablei</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glEnablei_impl=None
def glEnablei (target, index):
    global __glEnablei_impl
    if not __glEnablei_impl:
        fptr = __pyglGetFuncAddress('glEnablei')
        if not fptr:
            raise RuntimeError('The function glEnablei is not available')
        __glEnablei_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glEnablei = __glEnablei_impl
    return glEnablei(target, index)
# <command>
#            <proto>void <name>glEndConditionalRender</name></proto>
#            <glx opcode="349" type="render" />
#        </command>
#        
__glEndConditionalRender_impl=None
def glEndConditionalRender ():
    global __glEndConditionalRender_impl
    if not __glEndConditionalRender_impl:
        fptr = __pyglGetFuncAddress('glEndConditionalRender')
        if not fptr:
            raise RuntimeError('The function glEndConditionalRender is not available')
        __glEndConditionalRender_impl = __PYGL_FUNC_TYPE( None ,)(fptr)
    glEndConditionalRender = __glEndConditionalRender_impl
    return glEndConditionalRender()
# <command>
#            <proto>void <name>glEndQuery</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <glx opcode="232" type="render" />
#        </command>
#        
__glEndQuery_impl=None
def glEndQuery (target):
    global __glEndQuery_impl
    if not __glEndQuery_impl:
        fptr = __pyglGetFuncAddress('glEndQuery')
        if not fptr:
            raise RuntimeError('The function glEndQuery is not available')
        __glEndQuery_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glEndQuery = __glEndQuery_impl
    return glEndQuery(target)
# <command>
#            <proto>void <name>glEndQueryIndexed</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glEndQueryIndexed_impl=None
def glEndQueryIndexed (target, index):
    global __glEndQueryIndexed_impl
    if not __glEndQueryIndexed_impl:
        fptr = __pyglGetFuncAddress('glEndQueryIndexed')
        if not fptr:
            raise RuntimeError('The function glEndQueryIndexed is not available')
        __glEndQueryIndexed_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glEndQueryIndexed = __glEndQueryIndexed_impl
    return glEndQueryIndexed(target, index)
# <command>
#            <proto>void <name>glEndTransformFeedback</name></proto>
#        </command>
#        
__glEndTransformFeedback_impl=None
def glEndTransformFeedback ():
    global __glEndTransformFeedback_impl
    if not __glEndTransformFeedback_impl:
        fptr = __pyglGetFuncAddress('glEndTransformFeedback')
        if not fptr:
            raise RuntimeError('The function glEndTransformFeedback is not available')
        __glEndTransformFeedback_impl = __PYGL_FUNC_TYPE( None ,)(fptr)
    glEndTransformFeedback = __glEndTransformFeedback_impl
    return glEndTransformFeedback()
# <command>
#            <proto group="sync"><ptype>GLsync</ptype> <name>glFenceSync</name></proto>
#            <param><ptype>GLenum</ptype> <name>condition</name></param>
#            <param><ptype>GLbitfield</ptype> <name>flags</name></param>
#        </command>
#        
__glFenceSync_impl=None
def glFenceSync (condition, flags):
    global __glFenceSync_impl
    if not __glFenceSync_impl:
        fptr = __pyglGetFuncAddress('glFenceSync')
        if not fptr:
            raise RuntimeError('The function glFenceSync is not available')
        __glFenceSync_impl = __PYGL_FUNC_TYPE( c_void_p ,c_uint, c_uint)(fptr)
    glFenceSync = __glFenceSync_impl
    return glFenceSync(condition, flags)
# <command>
#            <proto>void <name>glFinish</name></proto>
#            <glx opcode="108" type="single" />
#        </command>
#        
__glFinish_impl=None
def glFinish ():
    global __glFinish_impl
    if not __glFinish_impl:
        fptr = __pyglGetFuncAddress('glFinish')
        if not fptr:
            raise RuntimeError('The function glFinish is not available')
        __glFinish_impl = __PYGL_FUNC_TYPE( None ,)(fptr)
    glFinish = __glFinish_impl
    return glFinish()
# <command>
#            <proto>void <name>glFlush</name></proto>
#            <glx opcode="142" type="single" />
#        </command>
#        
__glFlush_impl=None
def glFlush ():
    global __glFlush_impl
    if not __glFlush_impl:
        fptr = __pyglGetFuncAddress('glFlush')
        if not fptr:
            raise RuntimeError('The function glFlush is not available')
        __glFlush_impl = __PYGL_FUNC_TYPE( None ,)(fptr)
    glFlush = __glFlush_impl
    return glFlush()
# <command>
#            <proto>void <name>glFlushMappedBufferRange</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>length</name></param>
#        </command>
#        
__glFlushMappedBufferRange_impl=None
def glFlushMappedBufferRange (target, offset, length):
    global __glFlushMappedBufferRange_impl
    if not __glFlushMappedBufferRange_impl:
        fptr = __pyglGetFuncAddress('glFlushMappedBufferRange')
        if not fptr:
            raise RuntimeError('The function glFlushMappedBufferRange is not available')
        __glFlushMappedBufferRange_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_size_t, c_void_p)(fptr)
    glFlushMappedBufferRange = __glFlushMappedBufferRange_impl
    return glFlushMappedBufferRange(target, offset, length)
# <command>
#            <proto>void <name>glFlushMappedNamedBufferRange</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>length</name></param>
#        </command>
#        
__glFlushMappedNamedBufferRange_impl=None
def glFlushMappedNamedBufferRange (buffer, offset, length):
    global __glFlushMappedNamedBufferRange_impl
    if not __glFlushMappedNamedBufferRange_impl:
        fptr = __pyglGetFuncAddress('glFlushMappedNamedBufferRange')
        if not fptr:
            raise RuntimeError('The function glFlushMappedNamedBufferRange is not available')
        __glFlushMappedNamedBufferRange_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_size_t, c_void_p)(fptr)
    glFlushMappedNamedBufferRange = __glFlushMappedNamedBufferRange_impl
    return glFlushMappedNamedBufferRange(buffer, offset, length)
# <command>
#            <proto>void <name>glFramebufferParameteri</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> <name>param</name></param>
#        </command>
#        
__glFramebufferParameteri_impl=None
def glFramebufferParameteri (target, pname, param):
    global __glFramebufferParameteri_impl
    if not __glFramebufferParameteri_impl:
        fptr = __pyglGetFuncAddress('glFramebufferParameteri')
        if not fptr:
            raise RuntimeError('The function glFramebufferParameteri is not available')
        __glFramebufferParameteri_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int)(fptr)
    glFramebufferParameteri = __glFramebufferParameteri_impl
    return glFramebufferParameteri(target, pname, param)
# <command>
#            <proto>void <name>glFramebufferRenderbuffer</name></proto>
#            <param group="FramebufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="FramebufferAttachment"><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param group="RenderbufferTarget"><ptype>GLenum</ptype> <name>renderbuffertarget</name></param>
#            <param><ptype>GLuint</ptype> <name>renderbuffer</name></param>
#            <glx opcode="4324" type="render" />
#        </command>
#        
__glFramebufferRenderbuffer_impl=None
def glFramebufferRenderbuffer (target, attachment, renderbuffertarget, renderbuffer):
    global __glFramebufferRenderbuffer_impl
    if not __glFramebufferRenderbuffer_impl:
        fptr = __pyglGetFuncAddress('glFramebufferRenderbuffer')
        if not fptr:
            raise RuntimeError('The function glFramebufferRenderbuffer is not available')
        __glFramebufferRenderbuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint)(fptr)
    glFramebufferRenderbuffer = __glFramebufferRenderbuffer_impl
    return glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer)
# <command>
#            <proto>void <name>glFramebufferTexture</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#        </command>
#        
__glFramebufferTexture_impl=None
def glFramebufferTexture (target, attachment, texture, level):
    global __glFramebufferTexture_impl
    if not __glFramebufferTexture_impl:
        fptr = __pyglGetFuncAddress('glFramebufferTexture')
        if not fptr:
            raise RuntimeError('The function glFramebufferTexture is not available')
        __glFramebufferTexture_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int)(fptr)
    glFramebufferTexture = __glFramebufferTexture_impl
    return glFramebufferTexture(target, attachment, texture, level)
# <command>
#            <proto>void <name>glFramebufferTexture1D</name></proto>
#            <param group="FramebufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="FramebufferAttachment"><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param><ptype>GLenum</ptype> <name>textarget</name></param>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <glx opcode="4321" type="render" />
#        </command>
#        
__glFramebufferTexture1D_impl=None
def glFramebufferTexture1D (target, attachment, textarget, texture, level):
    global __glFramebufferTexture1D_impl
    if not __glFramebufferTexture1D_impl:
        fptr = __pyglGetFuncAddress('glFramebufferTexture1D')
        if not fptr:
            raise RuntimeError('The function glFramebufferTexture1D is not available')
        __glFramebufferTexture1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_int)(fptr)
    glFramebufferTexture1D = __glFramebufferTexture1D_impl
    return glFramebufferTexture1D(target, attachment, textarget, texture, level)
# <command>
#            <proto>void <name>glFramebufferTexture2D</name></proto>
#            <param group="FramebufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="FramebufferAttachment"><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param><ptype>GLenum</ptype> <name>textarget</name></param>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <glx opcode="4322" type="render" />
#        </command>
#        
__glFramebufferTexture2D_impl=None
def glFramebufferTexture2D (target, attachment, textarget, texture, level):
    global __glFramebufferTexture2D_impl
    if not __glFramebufferTexture2D_impl:
        fptr = __pyglGetFuncAddress('glFramebufferTexture2D')
        if not fptr:
            raise RuntimeError('The function glFramebufferTexture2D is not available')
        __glFramebufferTexture2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_int)(fptr)
    glFramebufferTexture2D = __glFramebufferTexture2D_impl
    return glFramebufferTexture2D(target, attachment, textarget, texture, level)
# <command>
#            <proto>void <name>glFramebufferTexture3D</name></proto>
#            <param group="FramebufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="FramebufferAttachment"><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param><ptype>GLenum</ptype> <name>textarget</name></param>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>zoffset</name></param>
#            <glx opcode="4323" type="render" />
#        </command>
#        
__glFramebufferTexture3D_impl=None
def glFramebufferTexture3D (target, attachment, textarget, texture, level, zoffset):
    global __glFramebufferTexture3D_impl
    if not __glFramebufferTexture3D_impl:
        fptr = __pyglGetFuncAddress('glFramebufferTexture3D')
        if not fptr:
            raise RuntimeError('The function glFramebufferTexture3D is not available')
        __glFramebufferTexture3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_int, c_int)(fptr)
    glFramebufferTexture3D = __glFramebufferTexture3D_impl
    return glFramebufferTexture3D(target, attachment, textarget, texture, level, zoffset)
# <command>
#            <proto>void <name>glFramebufferTextureLayer</name></proto>
#            <param group="FramebufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="FramebufferAttachment"><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param group="Texture"><ptype>GLuint</ptype> <name>texture</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>layer</name></param>
#            <glx opcode="237" type="render" />
#        </command>
#        
__glFramebufferTextureLayer_impl=None
def glFramebufferTextureLayer (target, attachment, texture, level, layer):
    global __glFramebufferTextureLayer_impl
    if not __glFramebufferTextureLayer_impl:
        fptr = __pyglGetFuncAddress('glFramebufferTextureLayer')
        if not fptr:
            raise RuntimeError('The function glFramebufferTextureLayer is not available')
        __glFramebufferTextureLayer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_int)(fptr)
    glFramebufferTextureLayer = __glFramebufferTextureLayer_impl
    return glFramebufferTextureLayer(target, attachment, texture, level, layer)
# <command>
#            <proto>void <name>glFrontFace</name></proto>
#            <param group="FrontFaceDirection"><ptype>GLenum</ptype> <name>mode</name></param>
#            <glx opcode="84" type="render" />
#        </command>
#        
__glFrontFace_impl=None
def glFrontFace (mode):
    global __glFrontFace_impl
    if not __glFrontFace_impl:
        fptr = __pyglGetFuncAddress('glFrontFace')
        if not fptr:
            raise RuntimeError('The function glFrontFace is not available')
        __glFrontFace_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glFrontFace = __glFrontFace_impl
    return glFrontFace(mode)
# <command>
#            <proto>void <name>glGenBuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n"><ptype>GLuint</ptype> *<name>buffers</name></param>
#        </command>
#        
__glGenBuffers_impl=None
def glGenBuffers (n, buffers):
    global __glGenBuffers_impl
    if not __glGenBuffers_impl:
        fptr = __pyglGetFuncAddress('glGenBuffers')
        if not fptr:
            raise RuntimeError('The function glGenBuffers is not available')
        __glGenBuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glGenBuffers = (lambda n,buffers:__glGenBuffers_impl(n,(c_uint8*len( buffers )).from_buffer( buffers )))
    return glGenBuffers(n, buffers)
# <command>
#            <proto>void <name>glGenFramebuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n"><ptype>GLuint</ptype> *<name>framebuffers</name></param>
#            <glx opcode="1426" type="vendor" />
#        </command>
#        
__glGenFramebuffers_impl=None
def glGenFramebuffers (n, framebuffers):
    global __glGenFramebuffers_impl
    if not __glGenFramebuffers_impl:
        fptr = __pyglGetFuncAddress('glGenFramebuffers')
        if not fptr:
            raise RuntimeError('The function glGenFramebuffers is not available')
        __glGenFramebuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glGenFramebuffers = (lambda n,framebuffers:__glGenFramebuffers_impl(n,(c_uint8*len( framebuffers )).from_buffer( framebuffers )))
    return glGenFramebuffers(n, framebuffers)
# <command>
#            <proto>void <name>glGenProgramPipelines</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n"><ptype>GLuint</ptype> *<name>pipelines</name></param>
#        </command>
#        
__glGenProgramPipelines_impl=None
def glGenProgramPipelines (n, pipelines):
    global __glGenProgramPipelines_impl
    if not __glGenProgramPipelines_impl:
        fptr = __pyglGetFuncAddress('glGenProgramPipelines')
        if not fptr:
            raise RuntimeError('The function glGenProgramPipelines is not available')
        __glGenProgramPipelines_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glGenProgramPipelines = (lambda n,pipelines:__glGenProgramPipelines_impl(n,(c_uint8*len( pipelines )).from_buffer( pipelines )))
    return glGenProgramPipelines(n, pipelines)
# <command>
#            <proto>void <name>glGenQueries</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n"><ptype>GLuint</ptype> *<name>ids</name></param>
#            <glx opcode="162" type="single" />
#        </command>
#        
__glGenQueries_impl=None
def glGenQueries (n, ids):
    global __glGenQueries_impl
    if not __glGenQueries_impl:
        fptr = __pyglGetFuncAddress('glGenQueries')
        if not fptr:
            raise RuntimeError('The function glGenQueries is not available')
        __glGenQueries_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glGenQueries = (lambda n,ids:__glGenQueries_impl(n,(c_uint8*len( ids )).from_buffer( ids )))
    return glGenQueries(n, ids)
# <command>
#            <proto>void <name>glGenRenderbuffers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n"><ptype>GLuint</ptype> *<name>renderbuffers</name></param>
#            <glx opcode="1423" type="vendor" />
#        </command>
#        
__glGenRenderbuffers_impl=None
def glGenRenderbuffers (n, renderbuffers):
    global __glGenRenderbuffers_impl
    if not __glGenRenderbuffers_impl:
        fptr = __pyglGetFuncAddress('glGenRenderbuffers')
        if not fptr:
            raise RuntimeError('The function glGenRenderbuffers is not available')
        __glGenRenderbuffers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glGenRenderbuffers = (lambda n,renderbuffers:__glGenRenderbuffers_impl(n,(c_uint8*len( renderbuffers )).from_buffer( renderbuffers )))
    return glGenRenderbuffers(n, renderbuffers)
# <command>
#            <proto>void <name>glGenSamplers</name></proto>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count"><ptype>GLuint</ptype> *<name>samplers</name></param>
#        </command>
#        
__glGenSamplers_impl=None
def glGenSamplers (count, samplers):
    global __glGenSamplers_impl
    if not __glGenSamplers_impl:
        fptr = __pyglGetFuncAddress('glGenSamplers')
        if not fptr:
            raise RuntimeError('The function glGenSamplers is not available')
        __glGenSamplers_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glGenSamplers = (lambda count,samplers:__glGenSamplers_impl(count,(c_uint8*len( samplers )).from_buffer( samplers )))
    return glGenSamplers(count, samplers)
# <command>
#            <proto>void <name>glGenTextures</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param group="Texture" len="n"><ptype>GLuint</ptype> *<name>textures</name></param>
#            <glx opcode="145" type="single" />
#        </command>
#        
__glGenTextures_impl=None
def glGenTextures (n, textures):
    global __glGenTextures_impl
    if not __glGenTextures_impl:
        fptr = __pyglGetFuncAddress('glGenTextures')
        if not fptr:
            raise RuntimeError('The function glGenTextures is not available')
        __glGenTextures_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glGenTextures = (lambda n,textures:__glGenTextures_impl(n,(c_uint8*len( textures )).from_buffer( textures )))
    return glGenTextures(n, textures)
# <command>
#            <proto>void <name>glGenTransformFeedbacks</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n"><ptype>GLuint</ptype> *<name>ids</name></param>
#        </command>
#        
__glGenTransformFeedbacks_impl=None
def glGenTransformFeedbacks (n, ids):
    global __glGenTransformFeedbacks_impl
    if not __glGenTransformFeedbacks_impl:
        fptr = __pyglGetFuncAddress('glGenTransformFeedbacks')
        if not fptr:
            raise RuntimeError('The function glGenTransformFeedbacks is not available')
        __glGenTransformFeedbacks_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glGenTransformFeedbacks = (lambda n,ids:__glGenTransformFeedbacks_impl(n,(c_uint8*len( ids )).from_buffer( ids )))
    return glGenTransformFeedbacks(n, ids)
# <command>
#            <proto>void <name>glGenVertexArrays</name></proto>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param len="n"><ptype>GLuint</ptype> *<name>arrays</name></param>
#            <glx opcode="206" type="single" />
#        </command>
#        
__glGenVertexArrays_impl=None
def glGenVertexArrays (n, arrays):
    global __glGenVertexArrays_impl
    if not __glGenVertexArrays_impl:
        fptr = __pyglGetFuncAddress('glGenVertexArrays')
        if not fptr:
            raise RuntimeError('The function glGenVertexArrays is not available')
        __glGenVertexArrays_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p)(fptr)
    glGenVertexArrays = (lambda n,arrays:__glGenVertexArrays_impl(n,(c_uint8*len( arrays )).from_buffer( arrays )))
    return glGenVertexArrays(n, arrays)
# <command>
#            <proto>void <name>glGenerateMipmap</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <glx opcode="4325" type="render" />
#        </command>
#        
__glGenerateMipmap_impl=None
def glGenerateMipmap (target):
    global __glGenerateMipmap_impl
    if not __glGenerateMipmap_impl:
        fptr = __pyglGetFuncAddress('glGenerateMipmap')
        if not fptr:
            raise RuntimeError('The function glGenerateMipmap is not available')
        __glGenerateMipmap_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glGenerateMipmap = __glGenerateMipmap_impl
    return glGenerateMipmap(target)
# <command>
#            <proto>void <name>glGenerateTextureMipmap</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#        </command>
#        
__glGenerateTextureMipmap_impl=None
def glGenerateTextureMipmap (texture):
    global __glGenerateTextureMipmap_impl
    if not __glGenerateTextureMipmap_impl:
        fptr = __pyglGetFuncAddress('glGenerateTextureMipmap')
        if not fptr:
            raise RuntimeError('The function glGenerateTextureMipmap is not available')
        __glGenerateTextureMipmap_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glGenerateTextureMipmap = __glGenerateTextureMipmap_impl
    return glGenerateTextureMipmap(texture)
# <command>
#            <proto>void <name>glGetActiveAtomicCounterBufferiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>bufferIndex</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetActiveAtomicCounterBufferiv_impl=None
def glGetActiveAtomicCounterBufferiv (program, bufferIndex, pname, params):
    global __glGetActiveAtomicCounterBufferiv_impl
    if not __glGetActiveAtomicCounterBufferiv_impl:
        fptr = __pyglGetFuncAddress('glGetActiveAtomicCounterBufferiv')
        if not fptr:
            raise RuntimeError('The function glGetActiveAtomicCounterBufferiv is not available')
        __glGetActiveAtomicCounterBufferiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetActiveAtomicCounterBufferiv = (lambda program,bufferIndex,pname,params:__glGetActiveAtomicCounterBufferiv_impl(program,bufferIndex,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetActiveAtomicCounterBufferiv(program, bufferIndex, pname, params)
# <command>
#            <proto>void <name>glGetActiveAttrib</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="1"><ptype>GLint</ptype> *<name>size</name></param>
#            <param len="1"><ptype>GLenum</ptype> *<name>type</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetActiveAttrib_impl=None
def glGetActiveAttrib (program, index, bufSize, length, size, type, name):
    global __glGetActiveAttrib_impl
    if not __glGetActiveAttrib_impl:
        fptr = __pyglGetFuncAddress('glGetActiveAttrib')
        if not fptr:
            raise RuntimeError('The function glGetActiveAttrib is not available')
        __glGetActiveAttrib_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p, c_void_p, c_void_p, c_void_p)(fptr)
    glGetActiveAttrib = (lambda program,index,bufSize,length,size,type,name:__glGetActiveAttrib_impl(program,index,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( size )).from_buffer( size ),(c_uint8*len( type )).from_buffer( type ),(c_uint8*len( name )).from_buffer( name )))
    return glGetActiveAttrib(program, index, bufSize, length, size, type, name)
# <command>
#            <proto>void <name>glGetActiveSubroutineName</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>shadertype</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufsize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufsize"><ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetActiveSubroutineName_impl=None
def glGetActiveSubroutineName (program, shadertype, index, bufsize, length, name):
    global __glGetActiveSubroutineName_impl
    if not __glGetActiveSubroutineName_impl:
        fptr = __pyglGetFuncAddress('glGetActiveSubroutineName')
        if not fptr:
            raise RuntimeError('The function glGetActiveSubroutineName is not available')
        __glGetActiveSubroutineName_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetActiveSubroutineName = (lambda program,shadertype,index,bufsize,length,name:__glGetActiveSubroutineName_impl(program,shadertype,index,bufsize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( name )).from_buffer( name )))
    return glGetActiveSubroutineName(program, shadertype, index, bufsize, length, name)
# <command>
#            <proto>void <name>glGetActiveSubroutineUniformName</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>shadertype</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufsize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufsize"><ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetActiveSubroutineUniformName_impl=None
def glGetActiveSubroutineUniformName (program, shadertype, index, bufsize, length, name):
    global __glGetActiveSubroutineUniformName_impl
    if not __glGetActiveSubroutineUniformName_impl:
        fptr = __pyglGetFuncAddress('glGetActiveSubroutineUniformName')
        if not fptr:
            raise RuntimeError('The function glGetActiveSubroutineUniformName is not available')
        __glGetActiveSubroutineUniformName_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetActiveSubroutineUniformName = (lambda program,shadertype,index,bufsize,length,name:__glGetActiveSubroutineUniformName_impl(program,shadertype,index,bufsize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( name )).from_buffer( name )))
    return glGetActiveSubroutineUniformName(program, shadertype, index, bufsize, length, name)
# <command>
#            <proto>void <name>glGetActiveSubroutineUniformiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>shadertype</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>values</name></param>
#        </command>
#        
__glGetActiveSubroutineUniformiv_impl=None
def glGetActiveSubroutineUniformiv (program, shadertype, index, pname, values):
    global __glGetActiveSubroutineUniformiv_impl
    if not __glGetActiveSubroutineUniformiv_impl:
        fptr = __pyglGetFuncAddress('glGetActiveSubroutineUniformiv')
        if not fptr:
            raise RuntimeError('The function glGetActiveSubroutineUniformiv is not available')
        __glGetActiveSubroutineUniformiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetActiveSubroutineUniformiv = (lambda program,shadertype,index,pname,values:__glGetActiveSubroutineUniformiv_impl(program,shadertype,index,pname,(c_uint8*len( values )).from_buffer( values )))
    return glGetActiveSubroutineUniformiv(program, shadertype, index, pname, values)
# <command>
#            <proto>void <name>glGetActiveUniform</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="1"><ptype>GLint</ptype> *<name>size</name></param>
#            <param len="1"><ptype>GLenum</ptype> *<name>type</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetActiveUniform_impl=None
def glGetActiveUniform (program, index, bufSize, length, size, type, name):
    global __glGetActiveUniform_impl
    if not __glGetActiveUniform_impl:
        fptr = __pyglGetFuncAddress('glGetActiveUniform')
        if not fptr:
            raise RuntimeError('The function glGetActiveUniform is not available')
        __glGetActiveUniform_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p, c_void_p, c_void_p, c_void_p)(fptr)
    glGetActiveUniform = (lambda program,index,bufSize,length,size,type,name:__glGetActiveUniform_impl(program,index,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( size )).from_buffer( size ),(c_uint8*len( type )).from_buffer( type ),(c_uint8*len( name )).from_buffer( name )))
    return glGetActiveUniform(program, index, bufSize, length, size, type, name)
# <command>
#            <proto>void <name>glGetActiveUniformBlockName</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>uniformBlockIndex</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>uniformBlockName</name></param>
#        </command>
#        
__glGetActiveUniformBlockName_impl=None
def glGetActiveUniformBlockName (program, uniformBlockIndex, bufSize, length, uniformBlockName):
    global __glGetActiveUniformBlockName_impl
    if not __glGetActiveUniformBlockName_impl:
        fptr = __pyglGetFuncAddress('glGetActiveUniformBlockName')
        if not fptr:
            raise RuntimeError('The function glGetActiveUniformBlockName is not available')
        __glGetActiveUniformBlockName_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetActiveUniformBlockName = (lambda program,uniformBlockIndex,bufSize,length,uniformBlockName:__glGetActiveUniformBlockName_impl(program,uniformBlockIndex,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( uniformBlockName )).from_buffer( uniformBlockName )))
    return glGetActiveUniformBlockName(program, uniformBlockIndex, bufSize, length, uniformBlockName)
# <command>
#            <proto>void <name>glGetActiveUniformBlockiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>uniformBlockIndex</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(program,uniformBlockIndex,pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetActiveUniformBlockiv_impl=None
def glGetActiveUniformBlockiv (program, uniformBlockIndex, pname, params):
    global __glGetActiveUniformBlockiv_impl
    if not __glGetActiveUniformBlockiv_impl:
        fptr = __pyglGetFuncAddress('glGetActiveUniformBlockiv')
        if not fptr:
            raise RuntimeError('The function glGetActiveUniformBlockiv is not available')
        __glGetActiveUniformBlockiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetActiveUniformBlockiv = (lambda program,uniformBlockIndex,pname,params:__glGetActiveUniformBlockiv_impl(program,uniformBlockIndex,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetActiveUniformBlockiv(program, uniformBlockIndex, pname, params)
# <command>
#            <proto>void <name>glGetActiveUniformName</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>uniformIndex</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>uniformName</name></param>
#        </command>
#        
__glGetActiveUniformName_impl=None
def glGetActiveUniformName (program, uniformIndex, bufSize, length, uniformName):
    global __glGetActiveUniformName_impl
    if not __glGetActiveUniformName_impl:
        fptr = __pyglGetFuncAddress('glGetActiveUniformName')
        if not fptr:
            raise RuntimeError('The function glGetActiveUniformName is not available')
        __glGetActiveUniformName_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetActiveUniformName = (lambda program,uniformIndex,bufSize,length,uniformName:__glGetActiveUniformName_impl(program,uniformIndex,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( uniformName )).from_buffer( uniformName )))
    return glGetActiveUniformName(program, uniformIndex, bufSize, length, uniformName)
# <command>
#            <proto>void <name>glGetActiveUniformsiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLsizei</ptype> <name>uniformCount</name></param>
#            <param len="uniformCount">const <ptype>GLuint</ptype> *<name>uniformIndices</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(uniformCount,pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetActiveUniformsiv_impl=None
def glGetActiveUniformsiv (program, uniformCount, uniformIndices, pname, params):
    global __glGetActiveUniformsiv_impl
    if not __glGetActiveUniformsiv_impl:
        fptr = __pyglGetFuncAddress('glGetActiveUniformsiv')
        if not fptr:
            raise RuntimeError('The function glGetActiveUniformsiv is not available')
        __glGetActiveUniformsiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_uint, c_void_p)(fptr)
    glGetActiveUniformsiv = (lambda program,uniformCount,uniformIndices,pname,params:__glGetActiveUniformsiv_impl(program,uniformCount,__pyglGetAsConstVoidPointer( uniformIndices ),pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetActiveUniformsiv(program, uniformCount, uniformIndices, pname, params)
# <command>
#            <proto>void <name>glGetAttachedShaders</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLsizei</ptype> <name>maxCount</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>count</name></param>
#            <param len="maxCount"><ptype>GLuint</ptype> *<name>shaders</name></param>
#        </command>
#        
__glGetAttachedShaders_impl=None
def glGetAttachedShaders (program, maxCount, count, shaders):
    global __glGetAttachedShaders_impl
    if not __glGetAttachedShaders_impl:
        fptr = __pyglGetFuncAddress('glGetAttachedShaders')
        if not fptr:
            raise RuntimeError('The function glGetAttachedShaders is not available')
        __glGetAttachedShaders_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetAttachedShaders = (lambda program,maxCount,count,shaders:__glGetAttachedShaders_impl(program,maxCount,(c_uint8*len( count )).from_buffer( count ),(c_uint8*len( shaders )).from_buffer( shaders )))
    return glGetAttachedShaders(program, maxCount, count, shaders)
# <command>
#            <proto><ptype>GLint</ptype> <name>glGetAttribLocation</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param>const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetAttribLocation_impl=None
def glGetAttribLocation (program, name):
    global __glGetAttribLocation_impl
    if not __glGetAttribLocation_impl:
        fptr = __pyglGetFuncAddress('glGetAttribLocation')
        if not fptr:
            raise RuntimeError('The function glGetAttribLocation is not available')
        __glGetAttribLocation_impl = __PYGL_FUNC_TYPE( c_int ,c_uint, c_void_p)(fptr)
    glGetAttribLocation = (lambda program,name:__glGetAttribLocation_impl(program,c_char_p( name .encode() )))
    return glGetAttribLocation(program, name)
# <command>
#            <proto>void <name>glGetBooleani_v</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param group="Boolean" len="COMPSIZE(target)"><ptype>GLboolean</ptype> *<name>data</name></param>
#        </command>
#        
__glGetBooleani_v_impl=None
def glGetBooleani_v (target, index, data):
    global __glGetBooleani_v_impl
    if not __glGetBooleani_v_impl:
        fptr = __pyglGetFuncAddress('glGetBooleani_v')
        if not fptr:
            raise RuntimeError('The function glGetBooleani_v is not available')
        __glGetBooleani_v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetBooleani_v = (lambda target,index,data:__glGetBooleani_v_impl(target,index,(c_uint8*len( data )).from_buffer( data )))
    return glGetBooleani_v(target, index, data)
# <command>
#            <proto>void <name>glGetBooleanv</name></proto>
#            <param group="GetPName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param group="Boolean" len="COMPSIZE(pname)"><ptype>GLboolean</ptype> *<name>data</name></param>
#            <glx opcode="112" type="single" />
#        </command>
#        
__glGetBooleanv_impl=None
def glGetBooleanv (pname, data):
    global __glGetBooleanv_impl
    if not __glGetBooleanv_impl:
        fptr = __pyglGetFuncAddress('glGetBooleanv')
        if not fptr:
            raise RuntimeError('The function glGetBooleanv is not available')
        __glGetBooleanv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glGetBooleanv = (lambda pname,data:__glGetBooleanv_impl(pname,(c_uint8*len( data )).from_buffer( data )))
    return glGetBooleanv(pname, data)
# <command>
#            <proto>void <name>glGetBufferParameteri64v</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="BufferPNameARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint64</ptype> *<name>params</name></param>
#        </command>
#        
__glGetBufferParameteri64v_impl=None
def glGetBufferParameteri64v (target, pname, params):
    global __glGetBufferParameteri64v_impl
    if not __glGetBufferParameteri64v_impl:
        fptr = __pyglGetFuncAddress('glGetBufferParameteri64v')
        if not fptr:
            raise RuntimeError('The function glGetBufferParameteri64v is not available')
        __glGetBufferParameteri64v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetBufferParameteri64v = (lambda target,pname,params:__glGetBufferParameteri64v_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetBufferParameteri64v(target, pname, params)
# <command>
#            <proto>void <name>glGetBufferParameteriv</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="BufferPNameARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetBufferParameteriv_impl=None
def glGetBufferParameteriv (target, pname, params):
    global __glGetBufferParameteriv_impl
    if not __glGetBufferParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetBufferParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetBufferParameteriv is not available')
        __glGetBufferParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetBufferParameteriv = (lambda target,pname,params:__glGetBufferParameteriv_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetBufferParameteriv(target, pname, params)
# <command>
#            <proto>void <name>glGetBufferPointerv</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="BufferPointerNameARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="1">void **<name>params</name></param>
#        </command>
#        
__glGetBufferPointerv_impl=None
def glGetBufferPointerv (target, pname, params):
    global __glGetBufferPointerv_impl
    if not __glGetBufferPointerv_impl:
        fptr = __pyglGetFuncAddress('glGetBufferPointerv')
        if not fptr:
            raise RuntimeError('The function glGetBufferPointerv is not available')
        __glGetBufferPointerv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetBufferPointerv = (lambda target,pname,params:__glGetBufferPointerv_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetBufferPointerv(target, pname, params)
# <command>
#            <proto>void <name>glGetBufferSubData</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param len="size">void *<name>data</name></param>
#        </command>
#        
__glGetBufferSubData_impl=None
def glGetBufferSubData (target, offset, size, data):
    global __glGetBufferSubData_impl
    if not __glGetBufferSubData_impl:
        fptr = __pyglGetFuncAddress('glGetBufferSubData')
        if not fptr:
            raise RuntimeError('The function glGetBufferSubData is not available')
        __glGetBufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_size_t, c_void_p, c_void_p)(fptr)
    glGetBufferSubData = (lambda target,offset,size,data:__glGetBufferSubData_impl(target,offset,size,(c_uint8*len( data )).from_buffer( data )))
    return glGetBufferSubData(target, offset, size, data)
# <command>
#            <proto>void <name>glGetCompressedTexImage</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CompressedTextureARB" len="COMPSIZE(target,level)">void *<name>img</name></param>
#            <glx opcode="160" type="single" />
#            <glx comment="PBO protocol" name="glGetCompressedTexImagePBO" opcode="335" type="render" />
#        </command>
#        
__glGetCompressedTexImage_impl=None
def glGetCompressedTexImage (target, level, img):
    global __glGetCompressedTexImage_impl
    if not __glGetCompressedTexImage_impl:
        fptr = __pyglGetFuncAddress('glGetCompressedTexImage')
        if not fptr:
            raise RuntimeError('The function glGetCompressedTexImage is not available')
        __glGetCompressedTexImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glGetCompressedTexImage = (lambda target,level,img:__glGetCompressedTexImage_impl(target,level,(c_uint8*len( img )).from_buffer( img )))
    return glGetCompressedTexImage(target, level, img)
# <command>
#            <proto>void <name>glGetCompressedTextureImage</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param>void *<name>pixels</name></param>
#        </command>
#        
__glGetCompressedTextureImage_impl=None
def glGetCompressedTextureImage (texture, level, bufSize, pixels):
    global __glGetCompressedTextureImage_impl
    if not __glGetCompressedTextureImage_impl:
        fptr = __pyglGetFuncAddress('glGetCompressedTextureImage')
        if not fptr:
            raise RuntimeError('The function glGetCompressedTextureImage is not available')
        __glGetCompressedTextureImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glGetCompressedTextureImage = (lambda texture,level,bufSize,pixels:__glGetCompressedTextureImage_impl(texture,level,bufSize,(c_uint8*len( pixels )).from_buffer( pixels )))
    return glGetCompressedTextureImage(texture, level, bufSize, pixels)
# <command>
#            <proto>void <name>glGetCompressedTextureSubImage</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param>void *<name>pixels</name></param>
#        </command>
#        
__glGetCompressedTextureSubImage_impl=None
def glGetCompressedTextureSubImage (texture, level, xoffset, yoffset, zoffset, width, height, depth, bufSize, pixels):
    global __glGetCompressedTextureSubImage_impl
    if not __glGetCompressedTextureSubImage_impl:
        fptr = __pyglGetFuncAddress('glGetCompressedTextureSubImage')
        if not fptr:
            raise RuntimeError('The function glGetCompressedTextureSubImage is not available')
        __glGetCompressedTextureSubImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_void_p)(fptr)
    glGetCompressedTextureSubImage = (lambda texture,level,xoffset,yoffset,zoffset,width,height,depth,bufSize,pixels:__glGetCompressedTextureSubImage_impl(texture,level,xoffset,yoffset,zoffset,width,height,depth,bufSize,(c_uint8*len( pixels )).from_buffer( pixels )))
    return glGetCompressedTextureSubImage(texture, level, xoffset, yoffset, zoffset, width, height, depth, bufSize, pixels)
# <command>
#            <proto><ptype>GLuint</ptype> <name>glGetDebugMessageLog</name></proto>
#            <param><ptype>GLuint</ptype> <name>count</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="count"><ptype>GLenum</ptype> *<name>sources</name></param>
#            <param len="count"><ptype>GLenum</ptype> *<name>types</name></param>
#            <param len="count"><ptype>GLuint</ptype> *<name>ids</name></param>
#            <param len="count"><ptype>GLenum</ptype> *<name>severities</name></param>
#            <param len="count"><ptype>GLsizei</ptype> *<name>lengths</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>messageLog</name></param>
#        </command>
#        
__glGetDebugMessageLog_impl=None
def glGetDebugMessageLog (count, bufSize, sources, types, ids, severities, lengths, messageLog):
    global __glGetDebugMessageLog_impl
    if not __glGetDebugMessageLog_impl:
        fptr = __pyglGetFuncAddress('glGetDebugMessageLog')
        if not fptr:
            raise RuntimeError('The function glGetDebugMessageLog is not available')
        __glGetDebugMessageLog_impl = __PYGL_FUNC_TYPE( c_uint ,c_uint, c_int, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p)(fptr)
    glGetDebugMessageLog = (lambda count,bufSize,sources,types,ids,severities,lengths,messageLog:__glGetDebugMessageLog_impl(count,bufSize,(c_uint8*len( sources )).from_buffer( sources ),(c_uint8*len( types )).from_buffer( types ),(c_uint8*len( ids )).from_buffer( ids ),(c_uint8*len( severities )).from_buffer( severities ),(c_uint8*len( lengths )).from_buffer( lengths ),(c_uint8*len( messageLog )).from_buffer( messageLog )))
    return glGetDebugMessageLog(count, bufSize, sources, types, ids, severities, lengths, messageLog)
# <command>
#            <proto>void <name>glGetDoublei_v</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="COMPSIZE(target)"><ptype>GLdouble</ptype> *<name>data</name></param>
#        </command>
#        
__glGetDoublei_v_impl=None
def glGetDoublei_v (target, index, data):
    global __glGetDoublei_v_impl
    if not __glGetDoublei_v_impl:
        fptr = __pyglGetFuncAddress('glGetDoublei_v')
        if not fptr:
            raise RuntimeError('The function glGetDoublei_v is not available')
        __glGetDoublei_v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetDoublei_v = (lambda target,index,data:__glGetDoublei_v_impl(target,index,(c_uint8*len( data )).from_buffer( data )))
    return glGetDoublei_v(target, index, data)
# <command>
#            <proto>void <name>glGetDoublev</name></proto>
#            <param group="GetPName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLdouble</ptype> *<name>data</name></param>
#            <glx opcode="114" type="single" />
#        </command>
#        
__glGetDoublev_impl=None
def glGetDoublev (pname, data):
    global __glGetDoublev_impl
    if not __glGetDoublev_impl:
        fptr = __pyglGetFuncAddress('glGetDoublev')
        if not fptr:
            raise RuntimeError('The function glGetDoublev is not available')
        __glGetDoublev_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glGetDoublev = (lambda pname,data:__glGetDoublev_impl(pname,(c_uint8*len( data )).from_buffer( data )))
    return glGetDoublev(pname, data)
# <command>
#            <proto group="ErrorCode"><ptype>GLenum</ptype> <name>glGetError</name></proto>
#            <glx opcode="115" type="single" />
#        </command>
#        
__glGetError_impl=None
def glGetError ():
    global __glGetError_impl
    if not __glGetError_impl:
        fptr = __pyglGetFuncAddress('glGetError')
        if not fptr:
            raise RuntimeError('The function glGetError is not available')
        __glGetError_impl = __PYGL_FUNC_TYPE( c_uint ,)(fptr)
    glGetError = __glGetError_impl
    return glGetError()
# <command>
#            <proto>void <name>glGetFloati_v</name></proto>
#            <param group="TypeEnum"><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="COMPSIZE(target)"><ptype>GLfloat</ptype> *<name>data</name></param>
#        </command>
#        
__glGetFloati_v_impl=None
def glGetFloati_v (target, index, data):
    global __glGetFloati_v_impl
    if not __glGetFloati_v_impl:
        fptr = __pyglGetFuncAddress('glGetFloati_v')
        if not fptr:
            raise RuntimeError('The function glGetFloati_v is not available')
        __glGetFloati_v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetFloati_v = (lambda target,index,data:__glGetFloati_v_impl(target,index,(c_uint8*len( data )).from_buffer( data )))
    return glGetFloati_v(target, index, data)
# <command>
#            <proto>void <name>glGetFloatv</name></proto>
#            <param group="GetPName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLfloat</ptype> *<name>data</name></param>
#            <glx opcode="116" type="single" />
#        </command>
#        
__glGetFloatv_impl=None
def glGetFloatv (pname, data):
    global __glGetFloatv_impl
    if not __glGetFloatv_impl:
        fptr = __pyglGetFuncAddress('glGetFloatv')
        if not fptr:
            raise RuntimeError('The function glGetFloatv is not available')
        __glGetFloatv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glGetFloatv = (lambda pname,data:__glGetFloatv_impl(pname,(c_uint8*len( data )).from_buffer( data )))
    return glGetFloatv(pname, data)
# <command>
#            <proto><ptype>GLint</ptype> <name>glGetFragDataIndex</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param>const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetFragDataIndex_impl=None
def glGetFragDataIndex (program, name):
    global __glGetFragDataIndex_impl
    if not __glGetFragDataIndex_impl:
        fptr = __pyglGetFuncAddress('glGetFragDataIndex')
        if not fptr:
            raise RuntimeError('The function glGetFragDataIndex is not available')
        __glGetFragDataIndex_impl = __PYGL_FUNC_TYPE( c_int ,c_uint, c_void_p)(fptr)
    glGetFragDataIndex = (lambda program,name:__glGetFragDataIndex_impl(program,c_char_p( name .encode() )))
    return glGetFragDataIndex(program, name)
# <command>
#            <proto><ptype>GLint</ptype> <name>glGetFragDataLocation</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param len="COMPSIZE(name)">const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetFragDataLocation_impl=None
def glGetFragDataLocation (program, name):
    global __glGetFragDataLocation_impl
    if not __glGetFragDataLocation_impl:
        fptr = __pyglGetFuncAddress('glGetFragDataLocation')
        if not fptr:
            raise RuntimeError('The function glGetFragDataLocation is not available')
        __glGetFragDataLocation_impl = __PYGL_FUNC_TYPE( c_int ,c_uint, c_void_p)(fptr)
    glGetFragDataLocation = (lambda program,name:__glGetFragDataLocation_impl(program,c_char_p( name .encode() )))
    return glGetFragDataLocation(program, name)
# <command>
#            <proto>void <name>glGetFramebufferAttachmentParameteriv</name></proto>
#            <param group="FramebufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="FramebufferAttachment"><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="1428" type="vendor" />
#        </command>
#        
__glGetFramebufferAttachmentParameteriv_impl=None
def glGetFramebufferAttachmentParameteriv (target, attachment, pname, params):
    global __glGetFramebufferAttachmentParameteriv_impl
    if not __glGetFramebufferAttachmentParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetFramebufferAttachmentParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetFramebufferAttachmentParameteriv is not available')
        __glGetFramebufferAttachmentParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetFramebufferAttachmentParameteriv = (lambda target,attachment,pname,params:__glGetFramebufferAttachmentParameteriv_impl(target,attachment,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetFramebufferAttachmentParameteriv(target, attachment, pname, params)
# <command>
#            <proto>void <name>glGetFramebufferParameteriv</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetFramebufferParameteriv_impl=None
def glGetFramebufferParameteriv (target, pname, params):
    global __glGetFramebufferParameteriv_impl
    if not __glGetFramebufferParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetFramebufferParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetFramebufferParameteriv is not available')
        __glGetFramebufferParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetFramebufferParameteriv = (lambda target,pname,params:__glGetFramebufferParameteriv_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetFramebufferParameteriv(target, pname, params)
# <command>
#            <proto><ptype>GLenum</ptype> <name>glGetGraphicsResetStatus</name></proto>
#        </command>
#        
__glGetGraphicsResetStatus_impl=None
def glGetGraphicsResetStatus ():
    global __glGetGraphicsResetStatus_impl
    if not __glGetGraphicsResetStatus_impl:
        fptr = __pyglGetFuncAddress('glGetGraphicsResetStatus')
        if not fptr:
            raise RuntimeError('The function glGetGraphicsResetStatus is not available')
        __glGetGraphicsResetStatus_impl = __PYGL_FUNC_TYPE( c_uint ,)(fptr)
    glGetGraphicsResetStatus = __glGetGraphicsResetStatus_impl
    return glGetGraphicsResetStatus()
# <command>
#            <proto>void <name>glGetInteger64i_v</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="COMPSIZE(target)"><ptype>GLint64</ptype> *<name>data</name></param>
#        </command>
#        
__glGetInteger64i_v_impl=None
def glGetInteger64i_v (target, index, data):
    global __glGetInteger64i_v_impl
    if not __glGetInteger64i_v_impl:
        fptr = __pyglGetFuncAddress('glGetInteger64i_v')
        if not fptr:
            raise RuntimeError('The function glGetInteger64i_v is not available')
        __glGetInteger64i_v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetInteger64i_v = (lambda target,index,data:__glGetInteger64i_v_impl(target,index,(c_uint8*len( data )).from_buffer( data )))
    return glGetInteger64i_v(target, index, data)
# <command>
#            <proto>void <name>glGetInteger64v</name></proto>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint64</ptype> *<name>data</name></param>
#        </command>
#        
__glGetInteger64v_impl=None
def glGetInteger64v (pname, data):
    global __glGetInteger64v_impl
    if not __glGetInteger64v_impl:
        fptr = __pyglGetFuncAddress('glGetInteger64v')
        if not fptr:
            raise RuntimeError('The function glGetInteger64v is not available')
        __glGetInteger64v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glGetInteger64v = (lambda pname,data:__glGetInteger64v_impl(pname,(c_uint8*len( data )).from_buffer( data )))
    return glGetInteger64v(pname, data)
# <command>
#            <proto>void <name>glGetIntegeri_v</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="COMPSIZE(target)"><ptype>GLint</ptype> *<name>data</name></param>
#        </command>
#        
__glGetIntegeri_v_impl=None
def glGetIntegeri_v (target, index, data):
    global __glGetIntegeri_v_impl
    if not __glGetIntegeri_v_impl:
        fptr = __pyglGetFuncAddress('glGetIntegeri_v')
        if not fptr:
            raise RuntimeError('The function glGetIntegeri_v is not available')
        __glGetIntegeri_v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetIntegeri_v = (lambda target,index,data:__glGetIntegeri_v_impl(target,index,(c_uint8*len( data )).from_buffer( data )))
    return glGetIntegeri_v(target, index, data)
# <command>
#            <proto>void <name>glGetIntegerv</name></proto>
#            <param group="GetPName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>data</name></param>
#            <glx opcode="117" type="single" />
#        </command>
#        
__glGetIntegerv_impl=None
def glGetIntegerv (pname, data):
    global __glGetIntegerv_impl
    if not __glGetIntegerv_impl:
        fptr = __pyglGetFuncAddress('glGetIntegerv')
        if not fptr:
            raise RuntimeError('The function glGetIntegerv is not available')
        __glGetIntegerv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glGetIntegerv = (lambda pname,data:__glGetIntegerv_impl(pname,(c_uint8*len( data )).from_buffer( data )))
    return glGetIntegerv(pname, data)
# <command>
#            <proto>void <name>glGetInternalformati64v</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="bufSize"><ptype>GLint64</ptype> *<name>params</name></param>
#        </command>
#        
__glGetInternalformati64v_impl=None
def glGetInternalformati64v (target, internalformat, pname, bufSize, params):
    global __glGetInternalformati64v_impl
    if not __glGetInternalformati64v_impl:
        fptr = __pyglGetFuncAddress('glGetInternalformati64v')
        if not fptr:
            raise RuntimeError('The function glGetInternalformati64v is not available')
        __glGetInternalformati64v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_void_p)(fptr)
    glGetInternalformati64v = (lambda target,internalformat,pname,bufSize,params:__glGetInternalformati64v_impl(target,internalformat,pname,bufSize,(c_uint8*len( params )).from_buffer( params )))
    return glGetInternalformati64v(target, internalformat, pname, bufSize, params)
# <command>
#            <proto>void <name>glGetInternalformativ</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="bufSize"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetInternalformativ_impl=None
def glGetInternalformativ (target, internalformat, pname, bufSize, params):
    global __glGetInternalformativ_impl
    if not __glGetInternalformativ_impl:
        fptr = __pyglGetFuncAddress('glGetInternalformativ')
        if not fptr:
            raise RuntimeError('The function glGetInternalformativ is not available')
        __glGetInternalformativ_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_void_p)(fptr)
    glGetInternalformativ = (lambda target,internalformat,pname,bufSize,params:__glGetInternalformativ_impl(target,internalformat,pname,bufSize,(c_uint8*len( params )).from_buffer( params )))
    return glGetInternalformativ(target, internalformat, pname, bufSize, params)
# <command>
#            <proto>void <name>glGetMultisamplefv</name></proto>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLfloat</ptype> *<name>val</name></param>
#        </command>
#        
__glGetMultisamplefv_impl=None
def glGetMultisamplefv (pname, index, val):
    global __glGetMultisamplefv_impl
    if not __glGetMultisamplefv_impl:
        fptr = __pyglGetFuncAddress('glGetMultisamplefv')
        if not fptr:
            raise RuntimeError('The function glGetMultisamplefv is not available')
        __glGetMultisamplefv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetMultisamplefv = (lambda pname,index,val:__glGetMultisamplefv_impl(pname,index,(c_uint8*len( val )).from_buffer( val )))
    return glGetMultisamplefv(pname, index, val)
# <command>
#            <proto>void <name>glGetNamedBufferParameteri64v</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint64</ptype> *<name>params</name></param>
#        </command>
#        
__glGetNamedBufferParameteri64v_impl=None
def glGetNamedBufferParameteri64v (buffer, pname, params):
    global __glGetNamedBufferParameteri64v_impl
    if not __glGetNamedBufferParameteri64v_impl:
        fptr = __pyglGetFuncAddress('glGetNamedBufferParameteri64v')
        if not fptr:
            raise RuntimeError('The function glGetNamedBufferParameteri64v is not available')
        __glGetNamedBufferParameteri64v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetNamedBufferParameteri64v = (lambda buffer,pname,params:__glGetNamedBufferParameteri64v_impl(buffer,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetNamedBufferParameteri64v(buffer, pname, params)
# <command>
#            <proto>void <name>glGetNamedBufferParameteriv</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetNamedBufferParameteriv_impl=None
def glGetNamedBufferParameteriv (buffer, pname, params):
    global __glGetNamedBufferParameteriv_impl
    if not __glGetNamedBufferParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetNamedBufferParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetNamedBufferParameteriv is not available')
        __glGetNamedBufferParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetNamedBufferParameteriv = (lambda buffer,pname,params:__glGetNamedBufferParameteriv_impl(buffer,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetNamedBufferParameteriv(buffer, pname, params)
# <command>
#            <proto>void <name>glGetNamedBufferPointerv</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param>void **<name>params</name></param>
#        </command>
#        
__glGetNamedBufferPointerv_impl=None
def glGetNamedBufferPointerv (buffer, pname, params):
    global __glGetNamedBufferPointerv_impl
    if not __glGetNamedBufferPointerv_impl:
        fptr = __pyglGetFuncAddress('glGetNamedBufferPointerv')
        if not fptr:
            raise RuntimeError('The function glGetNamedBufferPointerv is not available')
        __glGetNamedBufferPointerv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetNamedBufferPointerv = (lambda buffer,pname,params:__glGetNamedBufferPointerv_impl(buffer,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetNamedBufferPointerv(buffer, pname, params)
# <command>
#            <proto>void <name>glGetNamedBufferSubData</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param>void *<name>data</name></param>
#        </command>
#        
__glGetNamedBufferSubData_impl=None
def glGetNamedBufferSubData (buffer, offset, size, data):
    global __glGetNamedBufferSubData_impl
    if not __glGetNamedBufferSubData_impl:
        fptr = __pyglGetFuncAddress('glGetNamedBufferSubData')
        if not fptr:
            raise RuntimeError('The function glGetNamedBufferSubData is not available')
        __glGetNamedBufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_size_t, c_void_p, c_void_p)(fptr)
    glGetNamedBufferSubData = (lambda buffer,offset,size,data:__glGetNamedBufferSubData_impl(buffer,offset,size,(c_uint8*len( data )).from_buffer( data )))
    return glGetNamedBufferSubData(buffer, offset, size, data)
# <command>
#            <proto>void <name>glGetNamedFramebufferAttachmentParameteriv</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetNamedFramebufferAttachmentParameteriv_impl=None
def glGetNamedFramebufferAttachmentParameteriv (framebuffer, attachment, pname, params):
    global __glGetNamedFramebufferAttachmentParameteriv_impl
    if not __glGetNamedFramebufferAttachmentParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetNamedFramebufferAttachmentParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetNamedFramebufferAttachmentParameteriv is not available')
        __glGetNamedFramebufferAttachmentParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetNamedFramebufferAttachmentParameteriv = (lambda framebuffer,attachment,pname,params:__glGetNamedFramebufferAttachmentParameteriv_impl(framebuffer,attachment,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetNamedFramebufferAttachmentParameteriv(framebuffer, attachment, pname, params)
# <command>
#            <proto>void <name>glGetNamedFramebufferParameteriv</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>param</name></param>
#        </command>
#        
__glGetNamedFramebufferParameteriv_impl=None
def glGetNamedFramebufferParameteriv (framebuffer, pname, param):
    global __glGetNamedFramebufferParameteriv_impl
    if not __glGetNamedFramebufferParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetNamedFramebufferParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetNamedFramebufferParameteriv is not available')
        __glGetNamedFramebufferParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetNamedFramebufferParameteriv = (lambda framebuffer,pname,param:__glGetNamedFramebufferParameteriv_impl(framebuffer,pname,(c_uint8*len( param )).from_buffer( param )))
    return glGetNamedFramebufferParameteriv(framebuffer, pname, param)
# <command>
#            <proto>void <name>glGetNamedRenderbufferParameteriv</name></proto>
#            <param><ptype>GLuint</ptype> <name>renderbuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetNamedRenderbufferParameteriv_impl=None
def glGetNamedRenderbufferParameteriv (renderbuffer, pname, params):
    global __glGetNamedRenderbufferParameteriv_impl
    if not __glGetNamedRenderbufferParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetNamedRenderbufferParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetNamedRenderbufferParameteriv is not available')
        __glGetNamedRenderbufferParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetNamedRenderbufferParameteriv = (lambda renderbuffer,pname,params:__glGetNamedRenderbufferParameteriv_impl(renderbuffer,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetNamedRenderbufferParameteriv(renderbuffer, pname, params)
# <command>
#            <proto>void <name>glGetObjectLabel</name></proto>
#            <param><ptype>GLenum</ptype> <name>identifier</name></param>
#            <param><ptype>GLuint</ptype> <name>name</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>label</name></param>
#        </command>
#        
__glGetObjectLabel_impl=None
def glGetObjectLabel (identifier, name, bufSize, length, label):
    global __glGetObjectLabel_impl
    if not __glGetObjectLabel_impl:
        fptr = __pyglGetFuncAddress('glGetObjectLabel')
        if not fptr:
            raise RuntimeError('The function glGetObjectLabel is not available')
        __glGetObjectLabel_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetObjectLabel = (lambda identifier,name,bufSize,length,label:__glGetObjectLabel_impl(identifier,name,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( label )).from_buffer( label )))
    return glGetObjectLabel(identifier, name, bufSize, length, label)
# <command>
#            <proto>void <name>glGetObjectPtrLabel</name></proto>
#            <param>const void *<name>ptr</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>label</name></param>
#        </command>
#        
__glGetObjectPtrLabel_impl=None
def glGetObjectPtrLabel (ptr, bufSize, length, label):
    global __glGetObjectPtrLabel_impl
    if not __glGetObjectPtrLabel_impl:
        fptr = __pyglGetFuncAddress('glGetObjectPtrLabel')
        if not fptr:
            raise RuntimeError('The function glGetObjectPtrLabel is not available')
        __glGetObjectPtrLabel_impl = __PYGL_FUNC_TYPE( None ,c_void_p, c_int, c_void_p, c_void_p)(fptr)
    glGetObjectPtrLabel = (lambda ptr,bufSize,length,label:__glGetObjectPtrLabel_impl(__pyglGetAsConstVoidPointer( ptr ),bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( label )).from_buffer( label )))
    return glGetObjectPtrLabel(ptr, bufSize, length, label)
# <command>
#            <proto>void <name>glGetProgramBinary</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="1"><ptype>GLenum</ptype> *<name>binaryFormat</name></param>
#            <param len="bufSize">void *<name>binary</name></param>
#        </command>
#        
__glGetProgramBinary_impl=None
def glGetProgramBinary (program, bufSize, length, binaryFormat, binary):
    global __glGetProgramBinary_impl
    if not __glGetProgramBinary_impl:
        fptr = __pyglGetFuncAddress('glGetProgramBinary')
        if not fptr:
            raise RuntimeError('The function glGetProgramBinary is not available')
        __glGetProgramBinary_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_void_p, c_void_p)(fptr)
    glGetProgramBinary = (lambda program,bufSize,length,binaryFormat,binary:__glGetProgramBinary_impl(program,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( binaryFormat )).from_buffer( binaryFormat ),(c_uint8*len( binary )).from_buffer( binary )))
    return glGetProgramBinary(program, bufSize, length, binaryFormat, binary)
# <command>
#            <proto>void <name>glGetProgramInfoLog</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>infoLog</name></param>
#            <glx opcode="201" type="single" />
#        </command>
#        
__glGetProgramInfoLog_impl=None
def glGetProgramInfoLog (program, bufSize, length, infoLog):
    global __glGetProgramInfoLog_impl
    if not __glGetProgramInfoLog_impl:
        fptr = __pyglGetFuncAddress('glGetProgramInfoLog')
        if not fptr:
            raise RuntimeError('The function glGetProgramInfoLog is not available')
        __glGetProgramInfoLog_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetProgramInfoLog = (lambda program,bufSize,length,infoLog:__glGetProgramInfoLog_impl(program,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( infoLog )).from_buffer( infoLog )))
    return glGetProgramInfoLog(program, bufSize, length, infoLog)
# <command>
#            <proto>void <name>glGetProgramInterfaceiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>programInterface</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetProgramInterfaceiv_impl=None
def glGetProgramInterfaceiv (program, programInterface, pname, params):
    global __glGetProgramInterfaceiv_impl
    if not __glGetProgramInterfaceiv_impl:
        fptr = __pyglGetFuncAddress('glGetProgramInterfaceiv')
        if not fptr:
            raise RuntimeError('The function glGetProgramInterfaceiv is not available')
        __glGetProgramInterfaceiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetProgramInterfaceiv = (lambda program,programInterface,pname,params:__glGetProgramInterfaceiv_impl(program,programInterface,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetProgramInterfaceiv(program, programInterface, pname, params)
# <command>
#            <proto>void <name>glGetProgramPipelineInfoLog</name></proto>
#            <param><ptype>GLuint</ptype> <name>pipeline</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>infoLog</name></param>
#        </command>
#        
__glGetProgramPipelineInfoLog_impl=None
def glGetProgramPipelineInfoLog (pipeline, bufSize, length, infoLog):
    global __glGetProgramPipelineInfoLog_impl
    if not __glGetProgramPipelineInfoLog_impl:
        fptr = __pyglGetFuncAddress('glGetProgramPipelineInfoLog')
        if not fptr:
            raise RuntimeError('The function glGetProgramPipelineInfoLog is not available')
        __glGetProgramPipelineInfoLog_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetProgramPipelineInfoLog = (lambda pipeline,bufSize,length,infoLog:__glGetProgramPipelineInfoLog_impl(pipeline,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( infoLog )).from_buffer( infoLog )))
    return glGetProgramPipelineInfoLog(pipeline, bufSize, length, infoLog)
# <command>
#            <proto>void <name>glGetProgramPipelineiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>pipeline</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetProgramPipelineiv_impl=None
def glGetProgramPipelineiv (pipeline, pname, params):
    global __glGetProgramPipelineiv_impl
    if not __glGetProgramPipelineiv_impl:
        fptr = __pyglGetFuncAddress('glGetProgramPipelineiv')
        if not fptr:
            raise RuntimeError('The function glGetProgramPipelineiv is not available')
        __glGetProgramPipelineiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetProgramPipelineiv = (lambda pipeline,pname,params:__glGetProgramPipelineiv_impl(pipeline,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetProgramPipelineiv(pipeline, pname, params)
# <command>
#            <proto><ptype>GLuint</ptype> <name>glGetProgramResourceIndex</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>programInterface</name></param>
#            <param len="COMPSIZE(name)">const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetProgramResourceIndex_impl=None
def glGetProgramResourceIndex (program, programInterface, name):
    global __glGetProgramResourceIndex_impl
    if not __glGetProgramResourceIndex_impl:
        fptr = __pyglGetFuncAddress('glGetProgramResourceIndex')
        if not fptr:
            raise RuntimeError('The function glGetProgramResourceIndex is not available')
        __glGetProgramResourceIndex_impl = __PYGL_FUNC_TYPE( c_uint ,c_uint, c_uint, c_void_p)(fptr)
    glGetProgramResourceIndex = (lambda program,programInterface,name:__glGetProgramResourceIndex_impl(program,programInterface,c_char_p( name .encode() )))
    return glGetProgramResourceIndex(program, programInterface, name)
# <command>
#            <proto><ptype>GLint</ptype> <name>glGetProgramResourceLocation</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>programInterface</name></param>
#            <param len="COMPSIZE(name)">const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetProgramResourceLocation_impl=None
def glGetProgramResourceLocation (program, programInterface, name):
    global __glGetProgramResourceLocation_impl
    if not __glGetProgramResourceLocation_impl:
        fptr = __pyglGetFuncAddress('glGetProgramResourceLocation')
        if not fptr:
            raise RuntimeError('The function glGetProgramResourceLocation is not available')
        __glGetProgramResourceLocation_impl = __PYGL_FUNC_TYPE( c_int ,c_uint, c_uint, c_void_p)(fptr)
    glGetProgramResourceLocation = (lambda program,programInterface,name:__glGetProgramResourceLocation_impl(program,programInterface,c_char_p( name .encode() )))
    return glGetProgramResourceLocation(program, programInterface, name)
# <command>
#            <proto><ptype>GLint</ptype> <name>glGetProgramResourceLocationIndex</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>programInterface</name></param>
#            <param len="COMPSIZE(name)">const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetProgramResourceLocationIndex_impl=None
def glGetProgramResourceLocationIndex (program, programInterface, name):
    global __glGetProgramResourceLocationIndex_impl
    if not __glGetProgramResourceLocationIndex_impl:
        fptr = __pyglGetFuncAddress('glGetProgramResourceLocationIndex')
        if not fptr:
            raise RuntimeError('The function glGetProgramResourceLocationIndex is not available')
        __glGetProgramResourceLocationIndex_impl = __PYGL_FUNC_TYPE( c_int ,c_uint, c_uint, c_void_p)(fptr)
    glGetProgramResourceLocationIndex = (lambda program,programInterface,name:__glGetProgramResourceLocationIndex_impl(program,programInterface,c_char_p( name .encode() )))
    return glGetProgramResourceLocationIndex(program, programInterface, name)
# <command>
#            <proto>void <name>glGetProgramResourceName</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>programInterface</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetProgramResourceName_impl=None
def glGetProgramResourceName (program, programInterface, index, bufSize, length, name):
    global __glGetProgramResourceName_impl
    if not __glGetProgramResourceName_impl:
        fptr = __pyglGetFuncAddress('glGetProgramResourceName')
        if not fptr:
            raise RuntimeError('The function glGetProgramResourceName is not available')
        __glGetProgramResourceName_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetProgramResourceName = (lambda program,programInterface,index,bufSize,length,name:__glGetProgramResourceName_impl(program,programInterface,index,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( name )).from_buffer( name )))
    return glGetProgramResourceName(program, programInterface, index, bufSize, length, name)
# <command>
#            <proto>void <name>glGetProgramResourceiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>programInterface</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLsizei</ptype> <name>propCount</name></param>
#            <param len="propCount">const <ptype>GLenum</ptype> *<name>props</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetProgramResourceiv_impl=None
def glGetProgramResourceiv (program, programInterface, index, propCount, props, bufSize, length, params):
    global __glGetProgramResourceiv_impl
    if not __glGetProgramResourceiv_impl:
        fptr = __pyglGetFuncAddress('glGetProgramResourceiv')
        if not fptr:
            raise RuntimeError('The function glGetProgramResourceiv is not available')
        __glGetProgramResourceiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_void_p, c_int, c_void_p, c_void_p)(fptr)
    glGetProgramResourceiv = (lambda program,programInterface,index,propCount,props,bufSize,length,params:__glGetProgramResourceiv_impl(program,programInterface,index,propCount,__pyglGetAsConstVoidPointer( props ),bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( params )).from_buffer( params )))
    return glGetProgramResourceiv(program, programInterface, index, propCount, props, bufSize, length, params)
# <command>
#            <proto>void <name>glGetProgramStageiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>shadertype</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="1"><ptype>GLint</ptype> *<name>values</name></param>
#        </command>
#        
__glGetProgramStageiv_impl=None
def glGetProgramStageiv (program, shadertype, pname, values):
    global __glGetProgramStageiv_impl
    if not __glGetProgramStageiv_impl:
        fptr = __pyglGetFuncAddress('glGetProgramStageiv')
        if not fptr:
            raise RuntimeError('The function glGetProgramStageiv is not available')
        __glGetProgramStageiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetProgramStageiv = (lambda program,shadertype,pname,values:__glGetProgramStageiv_impl(program,shadertype,pname,(c_uint8*len( values )).from_buffer( values )))
    return glGetProgramStageiv(program, shadertype, pname, values)
# <command>
#            <proto>void <name>glGetProgramiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="199" type="single" />
#        </command>
#        
__glGetProgramiv_impl=None
def glGetProgramiv (program, pname, params):
    global __glGetProgramiv_impl
    if not __glGetProgramiv_impl:
        fptr = __pyglGetFuncAddress('glGetProgramiv')
        if not fptr:
            raise RuntimeError('The function glGetProgramiv is not available')
        __glGetProgramiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetProgramiv = (lambda program,pname,params:__glGetProgramiv_impl(program,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetProgramiv(program, pname, params)
# <command>
#            <proto>void <name>glGetQueryBufferObjecti64v</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#        </command>
#        
__glGetQueryBufferObjecti64v_impl=None
def glGetQueryBufferObjecti64v (id, buffer, pname, offset):
    global __glGetQueryBufferObjecti64v_impl
    if not __glGetQueryBufferObjecti64v_impl:
        fptr = __pyglGetFuncAddress('glGetQueryBufferObjecti64v')
        if not fptr:
            raise RuntimeError('The function glGetQueryBufferObjecti64v is not available')
        __glGetQueryBufferObjecti64v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_size_t)(fptr)
    glGetQueryBufferObjecti64v = __glGetQueryBufferObjecti64v_impl
    return glGetQueryBufferObjecti64v(id, buffer, pname, offset)
# <command>
#            <proto>void <name>glGetQueryBufferObjectiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#        </command>
#        
__glGetQueryBufferObjectiv_impl=None
def glGetQueryBufferObjectiv (id, buffer, pname, offset):
    global __glGetQueryBufferObjectiv_impl
    if not __glGetQueryBufferObjectiv_impl:
        fptr = __pyglGetFuncAddress('glGetQueryBufferObjectiv')
        if not fptr:
            raise RuntimeError('The function glGetQueryBufferObjectiv is not available')
        __glGetQueryBufferObjectiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_size_t)(fptr)
    glGetQueryBufferObjectiv = __glGetQueryBufferObjectiv_impl
    return glGetQueryBufferObjectiv(id, buffer, pname, offset)
# <command>
#            <proto>void <name>glGetQueryBufferObjectui64v</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#        </command>
#        
__glGetQueryBufferObjectui64v_impl=None
def glGetQueryBufferObjectui64v (id, buffer, pname, offset):
    global __glGetQueryBufferObjectui64v_impl
    if not __glGetQueryBufferObjectui64v_impl:
        fptr = __pyglGetFuncAddress('glGetQueryBufferObjectui64v')
        if not fptr:
            raise RuntimeError('The function glGetQueryBufferObjectui64v is not available')
        __glGetQueryBufferObjectui64v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_size_t)(fptr)
    glGetQueryBufferObjectui64v = __glGetQueryBufferObjectui64v_impl
    return glGetQueryBufferObjectui64v(id, buffer, pname, offset)
# <command>
#            <proto>void <name>glGetQueryBufferObjectuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#        </command>
#        
__glGetQueryBufferObjectuiv_impl=None
def glGetQueryBufferObjectuiv (id, buffer, pname, offset):
    global __glGetQueryBufferObjectuiv_impl
    if not __glGetQueryBufferObjectuiv_impl:
        fptr = __pyglGetFuncAddress('glGetQueryBufferObjectuiv')
        if not fptr:
            raise RuntimeError('The function glGetQueryBufferObjectuiv is not available')
        __glGetQueryBufferObjectuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_size_t)(fptr)
    glGetQueryBufferObjectuiv = __glGetQueryBufferObjectuiv_impl
    return glGetQueryBufferObjectuiv(id, buffer, pname, offset)
# <command>
#            <proto>void <name>glGetQueryIndexediv</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetQueryIndexediv_impl=None
def glGetQueryIndexediv (target, index, pname, params):
    global __glGetQueryIndexediv_impl
    if not __glGetQueryIndexediv_impl:
        fptr = __pyglGetFuncAddress('glGetQueryIndexediv')
        if not fptr:
            raise RuntimeError('The function glGetQueryIndexediv is not available')
        __glGetQueryIndexediv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetQueryIndexediv = (lambda target,index,pname,params:__glGetQueryIndexediv_impl(target,index,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetQueryIndexediv(target, index, pname, params)
# <command>
#            <proto>void <name>glGetQueryObjecti64v</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint64</ptype> *<name>params</name></param>
#        </command>
#        
__glGetQueryObjecti64v_impl=None
def glGetQueryObjecti64v (id, pname, params):
    global __glGetQueryObjecti64v_impl
    if not __glGetQueryObjecti64v_impl:
        fptr = __pyglGetFuncAddress('glGetQueryObjecti64v')
        if not fptr:
            raise RuntimeError('The function glGetQueryObjecti64v is not available')
        __glGetQueryObjecti64v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetQueryObjecti64v = (lambda id,pname,params:__glGetQueryObjecti64v_impl(id,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetQueryObjecti64v(id, pname, params)
# <command>
#            <proto>void <name>glGetQueryObjectiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="165" type="single" />
#        </command>
#        
__glGetQueryObjectiv_impl=None
def glGetQueryObjectiv (id, pname, params):
    global __glGetQueryObjectiv_impl
    if not __glGetQueryObjectiv_impl:
        fptr = __pyglGetFuncAddress('glGetQueryObjectiv')
        if not fptr:
            raise RuntimeError('The function glGetQueryObjectiv is not available')
        __glGetQueryObjectiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetQueryObjectiv = (lambda id,pname,params:__glGetQueryObjectiv_impl(id,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetQueryObjectiv(id, pname, params)
# <command>
#            <proto>void <name>glGetQueryObjectui64v</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLuint64</ptype> *<name>params</name></param>
#        </command>
#        
__glGetQueryObjectui64v_impl=None
def glGetQueryObjectui64v (id, pname, params):
    global __glGetQueryObjectui64v_impl
    if not __glGetQueryObjectui64v_impl:
        fptr = __pyglGetFuncAddress('glGetQueryObjectui64v')
        if not fptr:
            raise RuntimeError('The function glGetQueryObjectui64v is not available')
        __glGetQueryObjectui64v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetQueryObjectui64v = (lambda id,pname,params:__glGetQueryObjectui64v_impl(id,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetQueryObjectui64v(id, pname, params)
# <command>
#            <proto>void <name>glGetQueryObjectuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLuint</ptype> *<name>params</name></param>
#            <glx opcode="166" type="single" />
#        </command>
#        
__glGetQueryObjectuiv_impl=None
def glGetQueryObjectuiv (id, pname, params):
    global __glGetQueryObjectuiv_impl
    if not __glGetQueryObjectuiv_impl:
        fptr = __pyglGetFuncAddress('glGetQueryObjectuiv')
        if not fptr:
            raise RuntimeError('The function glGetQueryObjectuiv is not available')
        __glGetQueryObjectuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetQueryObjectuiv = (lambda id,pname,params:__glGetQueryObjectuiv_impl(id,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetQueryObjectuiv(id, pname, params)
# <command>
#            <proto>void <name>glGetQueryiv</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="164" type="single" />
#        </command>
#        
__glGetQueryiv_impl=None
def glGetQueryiv (target, pname, params):
    global __glGetQueryiv_impl
    if not __glGetQueryiv_impl:
        fptr = __pyglGetFuncAddress('glGetQueryiv')
        if not fptr:
            raise RuntimeError('The function glGetQueryiv is not available')
        __glGetQueryiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetQueryiv = (lambda target,pname,params:__glGetQueryiv_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetQueryiv(target, pname, params)
# <command>
#            <proto>void <name>glGetRenderbufferParameteriv</name></proto>
#            <param group="RenderbufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="1424" type="vendor" />
#        </command>
#        
__glGetRenderbufferParameteriv_impl=None
def glGetRenderbufferParameteriv (target, pname, params):
    global __glGetRenderbufferParameteriv_impl
    if not __glGetRenderbufferParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetRenderbufferParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetRenderbufferParameteriv is not available')
        __glGetRenderbufferParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetRenderbufferParameteriv = (lambda target,pname,params:__glGetRenderbufferParameteriv_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetRenderbufferParameteriv(target, pname, params)
# <command>
#            <proto>void <name>glGetSamplerParameterIiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetSamplerParameterIiv_impl=None
def glGetSamplerParameterIiv (sampler, pname, params):
    global __glGetSamplerParameterIiv_impl
    if not __glGetSamplerParameterIiv_impl:
        fptr = __pyglGetFuncAddress('glGetSamplerParameterIiv')
        if not fptr:
            raise RuntimeError('The function glGetSamplerParameterIiv is not available')
        __glGetSamplerParameterIiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetSamplerParameterIiv = (lambda sampler,pname,params:__glGetSamplerParameterIiv_impl(sampler,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetSamplerParameterIiv(sampler, pname, params)
# <command>
#            <proto>void <name>glGetSamplerParameterIuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLuint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetSamplerParameterIuiv_impl=None
def glGetSamplerParameterIuiv (sampler, pname, params):
    global __glGetSamplerParameterIuiv_impl
    if not __glGetSamplerParameterIuiv_impl:
        fptr = __pyglGetFuncAddress('glGetSamplerParameterIuiv')
        if not fptr:
            raise RuntimeError('The function glGetSamplerParameterIuiv is not available')
        __glGetSamplerParameterIuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetSamplerParameterIuiv = (lambda sampler,pname,params:__glGetSamplerParameterIuiv_impl(sampler,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetSamplerParameterIuiv(sampler, pname, params)
# <command>
#            <proto>void <name>glGetSamplerParameterfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLfloat</ptype> *<name>params</name></param>
#        </command>
#        
__glGetSamplerParameterfv_impl=None
def glGetSamplerParameterfv (sampler, pname, params):
    global __glGetSamplerParameterfv_impl
    if not __glGetSamplerParameterfv_impl:
        fptr = __pyglGetFuncAddress('glGetSamplerParameterfv')
        if not fptr:
            raise RuntimeError('The function glGetSamplerParameterfv is not available')
        __glGetSamplerParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetSamplerParameterfv = (lambda sampler,pname,params:__glGetSamplerParameterfv_impl(sampler,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetSamplerParameterfv(sampler, pname, params)
# <command>
#            <proto>void <name>glGetSamplerParameteriv</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetSamplerParameteriv_impl=None
def glGetSamplerParameteriv (sampler, pname, params):
    global __glGetSamplerParameteriv_impl
    if not __glGetSamplerParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetSamplerParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetSamplerParameteriv is not available')
        __glGetSamplerParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetSamplerParameteriv = (lambda sampler,pname,params:__glGetSamplerParameteriv_impl(sampler,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetSamplerParameteriv(sampler, pname, params)
# <command>
#            <proto>void <name>glGetShaderInfoLog</name></proto>
#            <param><ptype>GLuint</ptype> <name>shader</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>infoLog</name></param>
#            <glx opcode="200" type="single" />
#        </command>
#        
__glGetShaderInfoLog_impl=None
def glGetShaderInfoLog (shader, bufSize, length, infoLog):
    global __glGetShaderInfoLog_impl
    if not __glGetShaderInfoLog_impl:
        fptr = __pyglGetFuncAddress('glGetShaderInfoLog')
        if not fptr:
            raise RuntimeError('The function glGetShaderInfoLog is not available')
        __glGetShaderInfoLog_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetShaderInfoLog = (lambda shader,bufSize,length,infoLog:__glGetShaderInfoLog_impl(shader,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( infoLog )).from_buffer( infoLog )))
    return glGetShaderInfoLog(shader, bufSize, length, infoLog)
# <command>
#            <proto>void <name>glGetShaderPrecisionFormat</name></proto>
#            <param><ptype>GLenum</ptype> <name>shadertype</name></param>
#            <param><ptype>GLenum</ptype> <name>precisiontype</name></param>
#            <param len="2"><ptype>GLint</ptype> *<name>range</name></param>
#            <param len="2"><ptype>GLint</ptype> *<name>precision</name></param>
#        </command>
#        
__glGetShaderPrecisionFormat_impl=None
def glGetShaderPrecisionFormat (shadertype, precisiontype, range, precision):
    global __glGetShaderPrecisionFormat_impl
    if not __glGetShaderPrecisionFormat_impl:
        fptr = __pyglGetFuncAddress('glGetShaderPrecisionFormat')
        if not fptr:
            raise RuntimeError('The function glGetShaderPrecisionFormat is not available')
        __glGetShaderPrecisionFormat_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p, c_void_p)(fptr)
    glGetShaderPrecisionFormat = (lambda shadertype,precisiontype,range,precision:__glGetShaderPrecisionFormat_impl(shadertype,precisiontype,(c_uint8*len( range )).from_buffer( range ),(c_uint8*len( precision )).from_buffer( precision )))
    return glGetShaderPrecisionFormat(shadertype, precisiontype, range, precision)
# <command>
#            <proto>void <name>glGetShaderSource</name></proto>
#            <param><ptype>GLuint</ptype> <name>shader</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>source</name></param>
#        </command>
#        
__glGetShaderSource_impl=None
def glGetShaderSource (shader, bufSize, length, source):
    global __glGetShaderSource_impl
    if not __glGetShaderSource_impl:
        fptr = __pyglGetFuncAddress('glGetShaderSource')
        if not fptr:
            raise RuntimeError('The function glGetShaderSource is not available')
        __glGetShaderSource_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetShaderSource = (lambda shader,bufSize,length,source:__glGetShaderSource_impl(shader,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( source )).from_buffer( source )))
    return glGetShaderSource(shader, bufSize, length, source)
# <command>
#            <proto>void <name>glGetShaderiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>shader</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="198" type="single" />
#        </command>
#        
__glGetShaderiv_impl=None
def glGetShaderiv (shader, pname, params):
    global __glGetShaderiv_impl
    if not __glGetShaderiv_impl:
        fptr = __pyglGetFuncAddress('glGetShaderiv')
        if not fptr:
            raise RuntimeError('The function glGetShaderiv is not available')
        __glGetShaderiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetShaderiv = (lambda shader,pname,params:__glGetShaderiv_impl(shader,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetShaderiv(shader, pname, params)
# <command>
#            <proto group="String">const <ptype>GLubyte</ptype> *<name>glGetString</name></proto>
#            <param group="StringName"><ptype>GLenum</ptype> <name>name</name></param>
#            <glx opcode="129" type="single" />
#        </command>
#        
__glGetString_impl=None
def glGetString (name):
    global __glGetString_impl
    if not __glGetString_impl:
        fptr = __pyglGetFuncAddress('glGetString')
        if not fptr:
            raise RuntimeError('The function glGetString is not available')
        __glGetString_impl = __PYGL_FUNC_TYPE( c_char_p ,c_uint)(fptr)
    glGetString = __glGetString_impl
    return glGetString(name)
# <command>
#            <proto group="String">const <ptype>GLubyte</ptype> *<name>glGetStringi</name></proto>
#            <param><ptype>GLenum</ptype> <name>name</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glGetStringi_impl=None
def glGetStringi (name, index):
    global __glGetStringi_impl
    if not __glGetStringi_impl:
        fptr = __pyglGetFuncAddress('glGetStringi')
        if not fptr:
            raise RuntimeError('The function glGetStringi is not available')
        __glGetStringi_impl = __PYGL_FUNC_TYPE( c_char_p ,c_uint, c_uint)(fptr)
    glGetStringi = __glGetStringi_impl
    return glGetStringi(name, index)
# <command>
#            <proto><ptype>GLuint</ptype> <name>glGetSubroutineIndex</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>shadertype</name></param>
#            <param>const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetSubroutineIndex_impl=None
def glGetSubroutineIndex (program, shadertype, name):
    global __glGetSubroutineIndex_impl
    if not __glGetSubroutineIndex_impl:
        fptr = __pyglGetFuncAddress('glGetSubroutineIndex')
        if not fptr:
            raise RuntimeError('The function glGetSubroutineIndex is not available')
        __glGetSubroutineIndex_impl = __PYGL_FUNC_TYPE( c_uint ,c_uint, c_uint, c_void_p)(fptr)
    glGetSubroutineIndex = (lambda program,shadertype,name:__glGetSubroutineIndex_impl(program,shadertype,c_char_p( name .encode() )))
    return glGetSubroutineIndex(program, shadertype, name)
# <command>
#            <proto><ptype>GLint</ptype> <name>glGetSubroutineUniformLocation</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>shadertype</name></param>
#            <param>const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetSubroutineUniformLocation_impl=None
def glGetSubroutineUniformLocation (program, shadertype, name):
    global __glGetSubroutineUniformLocation_impl
    if not __glGetSubroutineUniformLocation_impl:
        fptr = __pyglGetFuncAddress('glGetSubroutineUniformLocation')
        if not fptr:
            raise RuntimeError('The function glGetSubroutineUniformLocation is not available')
        __glGetSubroutineUniformLocation_impl = __PYGL_FUNC_TYPE( c_int ,c_uint, c_uint, c_void_p)(fptr)
    glGetSubroutineUniformLocation = (lambda program,shadertype,name:__glGetSubroutineUniformLocation_impl(program,shadertype,c_char_p( name .encode() )))
    return glGetSubroutineUniformLocation(program, shadertype, name)
# <command>
#            <proto>void <name>glGetSynciv</name></proto>
#            <param group="sync"><ptype>GLsync</ptype> <name>sync</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="bufSize"><ptype>GLint</ptype> *<name>values</name></param>
#        </command>
#        
__glGetSynciv_impl=None
def glGetSynciv (sync, pname, bufSize, length, values):
    global __glGetSynciv_impl
    if not __glGetSynciv_impl:
        fptr = __pyglGetFuncAddress('glGetSynciv')
        if not fptr:
            raise RuntimeError('The function glGetSynciv is not available')
        __glGetSynciv_impl = __PYGL_FUNC_TYPE( None ,c_void_p, c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetSynciv = (lambda sync,pname,bufSize,length,values:__glGetSynciv_impl(sync,pname,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( values )).from_buffer( values )))
    return glGetSynciv(sync, pname, bufSize, length, values)
# <command>
#            <proto>void <name>glGetTexImage</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param group="PixelType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(target,level,format,type)">void *<name>pixels</name></param>
#            <glx opcode="135" type="single" />
#            <glx comment="PBO protocol" name="glGetTexImagePBO" opcode="344" type="render" />
#        </command>
#        
__glGetTexImage_impl=None
def glGetTexImage (target, level, format, type, pixels):
    global __glGetTexImage_impl
    if not __glGetTexImage_impl:
        fptr = __pyglGetFuncAddress('glGetTexImage')
        if not fptr:
            raise RuntimeError('The function glGetTexImage is not available')
        __glGetTexImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_uint, c_void_p)(fptr)
    glGetTexImage = (lambda target,level,format,type,pixels:__glGetTexImage_impl(target,level,format,type,(c_uint8*len( pixels )).from_buffer( pixels )))
    return glGetTexImage(target, level, format, type, pixels)
# <command>
#            <proto>void <name>glGetTexLevelParameterfv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="GetTextureParameter"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLfloat</ptype> *<name>params</name></param>
#            <glx opcode="138" type="single" />
#        </command>
#        
__glGetTexLevelParameterfv_impl=None
def glGetTexLevelParameterfv (target, level, pname, params):
    global __glGetTexLevelParameterfv_impl
    if not __glGetTexLevelParameterfv_impl:
        fptr = __pyglGetFuncAddress('glGetTexLevelParameterfv')
        if not fptr:
            raise RuntimeError('The function glGetTexLevelParameterfv is not available')
        __glGetTexLevelParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p)(fptr)
    glGetTexLevelParameterfv = (lambda target,level,pname,params:__glGetTexLevelParameterfv_impl(target,level,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTexLevelParameterfv(target, level, pname, params)
# <command>
#            <proto>void <name>glGetTexLevelParameteriv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="GetTextureParameter"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="139" type="single" />
#        </command>
#        
__glGetTexLevelParameteriv_impl=None
def glGetTexLevelParameteriv (target, level, pname, params):
    global __glGetTexLevelParameteriv_impl
    if not __glGetTexLevelParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetTexLevelParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetTexLevelParameteriv is not available')
        __glGetTexLevelParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p)(fptr)
    glGetTexLevelParameteriv = (lambda target,level,pname,params:__glGetTexLevelParameteriv_impl(target,level,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTexLevelParameteriv(target, level, pname, params)
# <command>
#            <proto>void <name>glGetTexParameterIiv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="GetTextureParameter"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="203" type="single" />
#        </command>
#        
__glGetTexParameterIiv_impl=None
def glGetTexParameterIiv (target, pname, params):
    global __glGetTexParameterIiv_impl
    if not __glGetTexParameterIiv_impl:
        fptr = __pyglGetFuncAddress('glGetTexParameterIiv')
        if not fptr:
            raise RuntimeError('The function glGetTexParameterIiv is not available')
        __glGetTexParameterIiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetTexParameterIiv = (lambda target,pname,params:__glGetTexParameterIiv_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTexParameterIiv(target, pname, params)
# <command>
#            <proto>void <name>glGetTexParameterIuiv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="GetTextureParameter"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLuint</ptype> *<name>params</name></param>
#            <glx opcode="204" type="single" />
#        </command>
#        
__glGetTexParameterIuiv_impl=None
def glGetTexParameterIuiv (target, pname, params):
    global __glGetTexParameterIuiv_impl
    if not __glGetTexParameterIuiv_impl:
        fptr = __pyglGetFuncAddress('glGetTexParameterIuiv')
        if not fptr:
            raise RuntimeError('The function glGetTexParameterIuiv is not available')
        __glGetTexParameterIuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetTexParameterIuiv = (lambda target,pname,params:__glGetTexParameterIuiv_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTexParameterIuiv(target, pname, params)
# <command>
#            <proto>void <name>glGetTexParameterfv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="GetTextureParameter"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLfloat</ptype> *<name>params</name></param>
#            <glx opcode="136" type="single" />
#        </command>
#        
__glGetTexParameterfv_impl=None
def glGetTexParameterfv (target, pname, params):
    global __glGetTexParameterfv_impl
    if not __glGetTexParameterfv_impl:
        fptr = __pyglGetFuncAddress('glGetTexParameterfv')
        if not fptr:
            raise RuntimeError('The function glGetTexParameterfv is not available')
        __glGetTexParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetTexParameterfv = (lambda target,pname,params:__glGetTexParameterfv_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTexParameterfv(target, pname, params)
# <command>
#            <proto>void <name>glGetTexParameteriv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="GetTextureParameter"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="137" type="single" />
#        </command>
#        
__glGetTexParameteriv_impl=None
def glGetTexParameteriv (target, pname, params):
    global __glGetTexParameteriv_impl
    if not __glGetTexParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetTexParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetTexParameteriv is not available')
        __glGetTexParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetTexParameteriv = (lambda target,pname,params:__glGetTexParameteriv_impl(target,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTexParameteriv(target, pname, params)
# <command>
#            <proto>void <name>glGetTextureImage</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param>void *<name>pixels</name></param>
#        </command>
#        
__glGetTextureImage_impl=None
def glGetTextureImage (texture, level, format, type, bufSize, pixels):
    global __glGetTextureImage_impl
    if not __glGetTextureImage_impl:
        fptr = __pyglGetFuncAddress('glGetTextureImage')
        if not fptr:
            raise RuntimeError('The function glGetTextureImage is not available')
        __glGetTextureImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_uint, c_int, c_void_p)(fptr)
    glGetTextureImage = (lambda texture,level,format,type,bufSize,pixels:__glGetTextureImage_impl(texture,level,format,type,bufSize,(c_uint8*len( pixels )).from_buffer( pixels )))
    return glGetTextureImage(texture, level, format, type, bufSize, pixels)
# <command>
#            <proto>void <name>glGetTextureLevelParameterfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLfloat</ptype> *<name>params</name></param>
#        </command>
#        
__glGetTextureLevelParameterfv_impl=None
def glGetTextureLevelParameterfv (texture, level, pname, params):
    global __glGetTextureLevelParameterfv_impl
    if not __glGetTextureLevelParameterfv_impl:
        fptr = __pyglGetFuncAddress('glGetTextureLevelParameterfv')
        if not fptr:
            raise RuntimeError('The function glGetTextureLevelParameterfv is not available')
        __glGetTextureLevelParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p)(fptr)
    glGetTextureLevelParameterfv = (lambda texture,level,pname,params:__glGetTextureLevelParameterfv_impl(texture,level,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTextureLevelParameterfv(texture, level, pname, params)
# <command>
#            <proto>void <name>glGetTextureLevelParameteriv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetTextureLevelParameteriv_impl=None
def glGetTextureLevelParameteriv (texture, level, pname, params):
    global __glGetTextureLevelParameteriv_impl
    if not __glGetTextureLevelParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetTextureLevelParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetTextureLevelParameteriv is not available')
        __glGetTextureLevelParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_void_p)(fptr)
    glGetTextureLevelParameteriv = (lambda texture,level,pname,params:__glGetTextureLevelParameteriv_impl(texture,level,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTextureLevelParameteriv(texture, level, pname, params)
# <command>
#            <proto>void <name>glGetTextureParameterIiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetTextureParameterIiv_impl=None
def glGetTextureParameterIiv (texture, pname, params):
    global __glGetTextureParameterIiv_impl
    if not __glGetTextureParameterIiv_impl:
        fptr = __pyglGetFuncAddress('glGetTextureParameterIiv')
        if not fptr:
            raise RuntimeError('The function glGetTextureParameterIiv is not available')
        __glGetTextureParameterIiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetTextureParameterIiv = (lambda texture,pname,params:__glGetTextureParameterIiv_impl(texture,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTextureParameterIiv(texture, pname, params)
# <command>
#            <proto>void <name>glGetTextureParameterIuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLuint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetTextureParameterIuiv_impl=None
def glGetTextureParameterIuiv (texture, pname, params):
    global __glGetTextureParameterIuiv_impl
    if not __glGetTextureParameterIuiv_impl:
        fptr = __pyglGetFuncAddress('glGetTextureParameterIuiv')
        if not fptr:
            raise RuntimeError('The function glGetTextureParameterIuiv is not available')
        __glGetTextureParameterIuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetTextureParameterIuiv = (lambda texture,pname,params:__glGetTextureParameterIuiv_impl(texture,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTextureParameterIuiv(texture, pname, params)
# <command>
#            <proto>void <name>glGetTextureParameterfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLfloat</ptype> *<name>params</name></param>
#        </command>
#        
__glGetTextureParameterfv_impl=None
def glGetTextureParameterfv (texture, pname, params):
    global __glGetTextureParameterfv_impl
    if not __glGetTextureParameterfv_impl:
        fptr = __pyglGetFuncAddress('glGetTextureParameterfv')
        if not fptr:
            raise RuntimeError('The function glGetTextureParameterfv is not available')
        __glGetTextureParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetTextureParameterfv = (lambda texture,pname,params:__glGetTextureParameterfv_impl(texture,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTextureParameterfv(texture, pname, params)
# <command>
#            <proto>void <name>glGetTextureParameteriv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetTextureParameteriv_impl=None
def glGetTextureParameteriv (texture, pname, params):
    global __glGetTextureParameteriv_impl
    if not __glGetTextureParameteriv_impl:
        fptr = __pyglGetFuncAddress('glGetTextureParameteriv')
        if not fptr:
            raise RuntimeError('The function glGetTextureParameteriv is not available')
        __glGetTextureParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetTextureParameteriv = (lambda texture,pname,params:__glGetTextureParameteriv_impl(texture,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetTextureParameteriv(texture, pname, params)
# <command>
#            <proto>void <name>glGetTextureSubImage</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param>void *<name>pixels</name></param>
#        </command>
#        
__glGetTextureSubImage_impl=None
def glGetTextureSubImage (texture, level, xoffset, yoffset, zoffset, width, height, depth, format, type, bufSize, pixels):
    global __glGetTextureSubImage_impl
    if not __glGetTextureSubImage_impl:
        fptr = __pyglGetFuncAddress('glGetTextureSubImage')
        if not fptr:
            raise RuntimeError('The function glGetTextureSubImage is not available')
        __glGetTextureSubImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint, c_int, c_void_p)(fptr)
    glGetTextureSubImage = (lambda texture,level,xoffset,yoffset,zoffset,width,height,depth,format,type,bufSize,pixels:__glGetTextureSubImage_impl(texture,level,xoffset,yoffset,zoffset,width,height,depth,format,type,bufSize,(c_uint8*len( pixels )).from_buffer( pixels )))
    return glGetTextureSubImage(texture, level, xoffset, yoffset, zoffset, width, height, depth, format, type, bufSize, pixels)
# <command>
#            <proto>void <name>glGetTransformFeedbackVarying</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>length</name></param>
#            <param len="1"><ptype>GLsizei</ptype> *<name>size</name></param>
#            <param len="1"><ptype>GLenum</ptype> *<name>type</name></param>
#            <param len="bufSize"><ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetTransformFeedbackVarying_impl=None
def glGetTransformFeedbackVarying (program, index, bufSize, length, size, type, name):
    global __glGetTransformFeedbackVarying_impl
    if not __glGetTransformFeedbackVarying_impl:
        fptr = __pyglGetFuncAddress('glGetTransformFeedbackVarying')
        if not fptr:
            raise RuntimeError('The function glGetTransformFeedbackVarying is not available')
        __glGetTransformFeedbackVarying_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p, c_void_p, c_void_p, c_void_p)(fptr)
    glGetTransformFeedbackVarying = (lambda program,index,bufSize,length,size,type,name:__glGetTransformFeedbackVarying_impl(program,index,bufSize,(c_uint8*len( length )).from_buffer( length ),(c_uint8*len( size )).from_buffer( size ),(c_uint8*len( type )).from_buffer( type ),(c_uint8*len( name )).from_buffer( name )))
    return glGetTransformFeedbackVarying(program, index, bufSize, length, size, type, name)
# <command>
#            <proto>void <name>glGetTransformFeedbacki64_v</name></proto>
#            <param><ptype>GLuint</ptype> <name>xfb</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLint64</ptype> *<name>param</name></param>
#        </command>
#        
__glGetTransformFeedbacki64_v_impl=None
def glGetTransformFeedbacki64_v (xfb, pname, index, param):
    global __glGetTransformFeedbacki64_v_impl
    if not __glGetTransformFeedbacki64_v_impl:
        fptr = __pyglGetFuncAddress('glGetTransformFeedbacki64_v')
        if not fptr:
            raise RuntimeError('The function glGetTransformFeedbacki64_v is not available')
        __glGetTransformFeedbacki64_v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetTransformFeedbacki64_v = (lambda xfb,pname,index,param:__glGetTransformFeedbacki64_v_impl(xfb,pname,index,(c_uint8*len( param )).from_buffer( param )))
    return glGetTransformFeedbacki64_v(xfb, pname, index, param)
# <command>
#            <proto>void <name>glGetTransformFeedbacki_v</name></proto>
#            <param><ptype>GLuint</ptype> <name>xfb</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLint</ptype> *<name>param</name></param>
#        </command>
#        
__glGetTransformFeedbacki_v_impl=None
def glGetTransformFeedbacki_v (xfb, pname, index, param):
    global __glGetTransformFeedbacki_v_impl
    if not __glGetTransformFeedbacki_v_impl:
        fptr = __pyglGetFuncAddress('glGetTransformFeedbacki_v')
        if not fptr:
            raise RuntimeError('The function glGetTransformFeedbacki_v is not available')
        __glGetTransformFeedbacki_v_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetTransformFeedbacki_v = (lambda xfb,pname,index,param:__glGetTransformFeedbacki_v_impl(xfb,pname,index,(c_uint8*len( param )).from_buffer( param )))
    return glGetTransformFeedbacki_v(xfb, pname, index, param)
# <command>
#            <proto>void <name>glGetTransformFeedbackiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>xfb</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>param</name></param>
#        </command>
#        
__glGetTransformFeedbackiv_impl=None
def glGetTransformFeedbackiv (xfb, pname, param):
    global __glGetTransformFeedbackiv_impl
    if not __glGetTransformFeedbackiv_impl:
        fptr = __pyglGetFuncAddress('glGetTransformFeedbackiv')
        if not fptr:
            raise RuntimeError('The function glGetTransformFeedbackiv is not available')
        __glGetTransformFeedbackiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetTransformFeedbackiv = (lambda xfb,pname,param:__glGetTransformFeedbackiv_impl(xfb,pname,(c_uint8*len( param )).from_buffer( param )))
    return glGetTransformFeedbackiv(xfb, pname, param)
# <command>
#            <proto><ptype>GLuint</ptype> <name>glGetUniformBlockIndex</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param len="COMPSIZE()">const <ptype>GLchar</ptype> *<name>uniformBlockName</name></param>
#        </command>
#        
__glGetUniformBlockIndex_impl=None
def glGetUniformBlockIndex (program, uniformBlockName):
    global __glGetUniformBlockIndex_impl
    if not __glGetUniformBlockIndex_impl:
        fptr = __pyglGetFuncAddress('glGetUniformBlockIndex')
        if not fptr:
            raise RuntimeError('The function glGetUniformBlockIndex is not available')
        __glGetUniformBlockIndex_impl = __PYGL_FUNC_TYPE( c_uint ,c_uint, c_void_p)(fptr)
    glGetUniformBlockIndex = (lambda program,uniformBlockName:__glGetUniformBlockIndex_impl(program,c_char_p( uniformBlockName .encode() )))
    return glGetUniformBlockIndex(program, uniformBlockName)
# <command>
#            <proto>void <name>glGetUniformIndices</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLsizei</ptype> <name>uniformCount</name></param>
#            <param len="COMPSIZE(uniformCount)">const <ptype>GLchar</ptype> *const*<name>uniformNames</name></param>
#            <param len="COMPSIZE(uniformCount)"><ptype>GLuint</ptype> *<name>uniformIndices</name></param>
#        </command>
#        
__glGetUniformIndices_impl=None
def glGetUniformIndices (program, uniformCount, uniformNames, uniformIndices):
    global __glGetUniformIndices_impl
    if not __glGetUniformIndices_impl:
        fptr = __pyglGetFuncAddress('glGetUniformIndices')
        if not fptr:
            raise RuntimeError('The function glGetUniformIndices is not available')
        __glGetUniformIndices_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_void_p)(fptr)
    glGetUniformIndices = (lambda program,uniformCount,uniformNames,uniformIndices:__glGetUniformIndices_impl(program,uniformCount,c_char_p( uniformNames .encode() ),(c_uint8*len( uniformIndices )).from_buffer( uniformIndices )))
    return glGetUniformIndices(program, uniformCount, uniformNames, uniformIndices)
# <command>
#            <proto><ptype>GLint</ptype> <name>glGetUniformLocation</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param>const <ptype>GLchar</ptype> *<name>name</name></param>
#        </command>
#        
__glGetUniformLocation_impl=None
def glGetUniformLocation (program, name):
    global __glGetUniformLocation_impl
    if not __glGetUniformLocation_impl:
        fptr = __pyglGetFuncAddress('glGetUniformLocation')
        if not fptr:
            raise RuntimeError('The function glGetUniformLocation is not available')
        __glGetUniformLocation_impl = __PYGL_FUNC_TYPE( c_int ,c_uint, c_void_p)(fptr)
    glGetUniformLocation = (lambda program,name:__glGetUniformLocation_impl(program,c_char_p( name .encode() )))
    return glGetUniformLocation(program, name)
# <command>
#            <proto>void <name>glGetUniformSubroutineuiv</name></proto>
#            <param><ptype>GLenum</ptype> <name>shadertype</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param len="1"><ptype>GLuint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetUniformSubroutineuiv_impl=None
def glGetUniformSubroutineuiv (shadertype, location, params):
    global __glGetUniformSubroutineuiv_impl
    if not __glGetUniformSubroutineuiv_impl:
        fptr = __pyglGetFuncAddress('glGetUniformSubroutineuiv')
        if not fptr:
            raise RuntimeError('The function glGetUniformSubroutineuiv is not available')
        __glGetUniformSubroutineuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glGetUniformSubroutineuiv = (lambda shadertype,location,params:__glGetUniformSubroutineuiv_impl(shadertype,location,(c_uint8*len( params )).from_buffer( params )))
    return glGetUniformSubroutineuiv(shadertype, location, params)
# <command>
#            <proto>void <name>glGetUniformdv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param len="COMPSIZE(program,location)"><ptype>GLdouble</ptype> *<name>params</name></param>
#        </command>
#        
__glGetUniformdv_impl=None
def glGetUniformdv (program, location, params):
    global __glGetUniformdv_impl
    if not __glGetUniformdv_impl:
        fptr = __pyglGetFuncAddress('glGetUniformdv')
        if not fptr:
            raise RuntimeError('The function glGetUniformdv is not available')
        __glGetUniformdv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glGetUniformdv = (lambda program,location,params:__glGetUniformdv_impl(program,location,(c_uint8*len( params )).from_buffer( params )))
    return glGetUniformdv(program, location, params)
# <command>
#            <proto>void <name>glGetUniformfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param len="COMPSIZE(program,location)"><ptype>GLfloat</ptype> *<name>params</name></param>
#        </command>
#        
__glGetUniformfv_impl=None
def glGetUniformfv (program, location, params):
    global __glGetUniformfv_impl
    if not __glGetUniformfv_impl:
        fptr = __pyglGetFuncAddress('glGetUniformfv')
        if not fptr:
            raise RuntimeError('The function glGetUniformfv is not available')
        __glGetUniformfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glGetUniformfv = (lambda program,location,params:__glGetUniformfv_impl(program,location,(c_uint8*len( params )).from_buffer( params )))
    return glGetUniformfv(program, location, params)
# <command>
#            <proto>void <name>glGetUniformiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param len="COMPSIZE(program,location)"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetUniformiv_impl=None
def glGetUniformiv (program, location, params):
    global __glGetUniformiv_impl
    if not __glGetUniformiv_impl:
        fptr = __pyglGetFuncAddress('glGetUniformiv')
        if not fptr:
            raise RuntimeError('The function glGetUniformiv is not available')
        __glGetUniformiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glGetUniformiv = (lambda program,location,params:__glGetUniformiv_impl(program,location,(c_uint8*len( params )).from_buffer( params )))
    return glGetUniformiv(program, location, params)
# <command>
#            <proto>void <name>glGetUniformuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param len="COMPSIZE(program,location)"><ptype>GLuint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetUniformuiv_impl=None
def glGetUniformuiv (program, location, params):
    global __glGetUniformuiv_impl
    if not __glGetUniformuiv_impl:
        fptr = __pyglGetFuncAddress('glGetUniformuiv')
        if not fptr:
            raise RuntimeError('The function glGetUniformuiv is not available')
        __glGetUniformuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glGetUniformuiv = (lambda program,location,params:__glGetUniformuiv_impl(program,location,(c_uint8*len( params )).from_buffer( params )))
    return glGetUniformuiv(program, location, params)
# <command>
#            <proto>void <name>glGetVertexArrayIndexed64iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint64</ptype> *<name>param</name></param>
#        </command>
#        
__glGetVertexArrayIndexed64iv_impl=None
def glGetVertexArrayIndexed64iv (vaobj, index, pname, param):
    global __glGetVertexArrayIndexed64iv_impl
    if not __glGetVertexArrayIndexed64iv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexArrayIndexed64iv')
        if not fptr:
            raise RuntimeError('The function glGetVertexArrayIndexed64iv is not available')
        __glGetVertexArrayIndexed64iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetVertexArrayIndexed64iv = (lambda vaobj,index,pname,param:__glGetVertexArrayIndexed64iv_impl(vaobj,index,pname,(c_uint8*len( param )).from_buffer( param )))
    return glGetVertexArrayIndexed64iv(vaobj, index, pname, param)
# <command>
#            <proto>void <name>glGetVertexArrayIndexediv</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>param</name></param>
#        </command>
#        
__glGetVertexArrayIndexediv_impl=None
def glGetVertexArrayIndexediv (vaobj, index, pname, param):
    global __glGetVertexArrayIndexediv_impl
    if not __glGetVertexArrayIndexediv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexArrayIndexediv')
        if not fptr:
            raise RuntimeError('The function glGetVertexArrayIndexediv is not available')
        __glGetVertexArrayIndexediv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_void_p)(fptr)
    glGetVertexArrayIndexediv = (lambda vaobj,index,pname,param:__glGetVertexArrayIndexediv_impl(vaobj,index,pname,(c_uint8*len( param )).from_buffer( param )))
    return glGetVertexArrayIndexediv(vaobj, index, pname, param)
# <command>
#            <proto>void <name>glGetVertexArrayiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> *<name>param</name></param>
#        </command>
#        
__glGetVertexArrayiv_impl=None
def glGetVertexArrayiv (vaobj, pname, param):
    global __glGetVertexArrayiv_impl
    if not __glGetVertexArrayiv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexArrayiv')
        if not fptr:
            raise RuntimeError('The function glGetVertexArrayiv is not available')
        __glGetVertexArrayiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetVertexArrayiv = (lambda vaobj,pname,param:__glGetVertexArrayiv_impl(vaobj,pname,(c_uint8*len( param )).from_buffer( param )))
    return glGetVertexArrayiv(vaobj, pname, param)
# <command>
#            <proto>void <name>glGetVertexAttribIiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param group="VertexAttribEnum"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="1"><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetVertexAttribIiv_impl=None
def glGetVertexAttribIiv (index, pname, params):
    global __glGetVertexAttribIiv_impl
    if not __glGetVertexAttribIiv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexAttribIiv')
        if not fptr:
            raise RuntimeError('The function glGetVertexAttribIiv is not available')
        __glGetVertexAttribIiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetVertexAttribIiv = (lambda index,pname,params:__glGetVertexAttribIiv_impl(index,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetVertexAttribIiv(index, pname, params)
# <command>
#            <proto>void <name>glGetVertexAttribIuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param group="VertexAttribEnum"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="1"><ptype>GLuint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetVertexAttribIuiv_impl=None
def glGetVertexAttribIuiv (index, pname, params):
    global __glGetVertexAttribIuiv_impl
    if not __glGetVertexAttribIuiv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexAttribIuiv')
        if not fptr:
            raise RuntimeError('The function glGetVertexAttribIuiv is not available')
        __glGetVertexAttribIuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetVertexAttribIuiv = (lambda index,pname,params:__glGetVertexAttribIuiv_impl(index,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetVertexAttribIuiv(index, pname, params)
# <command>
#            <proto>void <name>glGetVertexAttribLdv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)"><ptype>GLdouble</ptype> *<name>params</name></param>
#        </command>
#        
__glGetVertexAttribLdv_impl=None
def glGetVertexAttribLdv (index, pname, params):
    global __glGetVertexAttribLdv_impl
    if not __glGetVertexAttribLdv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexAttribLdv')
        if not fptr:
            raise RuntimeError('The function glGetVertexAttribLdv is not available')
        __glGetVertexAttribLdv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetVertexAttribLdv = (lambda index,pname,params:__glGetVertexAttribLdv_impl(index,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetVertexAttribLdv(index, pname, params)
# <command>
#            <proto>void <name>glGetVertexAttribPointerv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param group="VertexAttribPointerPropertyARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="1">void **<name>pointer</name></param>
#            <glx opcode="209" type="single" />
#        </command>
#        
__glGetVertexAttribPointerv_impl=None
def glGetVertexAttribPointerv (index, pname, pointer):
    global __glGetVertexAttribPointerv_impl
    if not __glGetVertexAttribPointerv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexAttribPointerv')
        if not fptr:
            raise RuntimeError('The function glGetVertexAttribPointerv is not available')
        __glGetVertexAttribPointerv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetVertexAttribPointerv = (lambda index,pname,pointer:__glGetVertexAttribPointerv_impl(index,pname,(c_uint8*len( pointer )).from_buffer( pointer )))
    return glGetVertexAttribPointerv(index, pname, pointer)
# <command>
#            <proto>void <name>glGetVertexAttribdv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param group="VertexAttribPropertyARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="4"><ptype>GLdouble</ptype> *<name>params</name></param>
#            <glx opcode="1301" type="vendor" />
#        </command>
#        
__glGetVertexAttribdv_impl=None
def glGetVertexAttribdv (index, pname, params):
    global __glGetVertexAttribdv_impl
    if not __glGetVertexAttribdv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexAttribdv')
        if not fptr:
            raise RuntimeError('The function glGetVertexAttribdv is not available')
        __glGetVertexAttribdv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetVertexAttribdv = (lambda index,pname,params:__glGetVertexAttribdv_impl(index,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetVertexAttribdv(index, pname, params)
# <command>
#            <proto>void <name>glGetVertexAttribfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param group="VertexAttribPropertyARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="4"><ptype>GLfloat</ptype> *<name>params</name></param>
#            <glx opcode="1302" type="vendor" />
#        </command>
#        
__glGetVertexAttribfv_impl=None
def glGetVertexAttribfv (index, pname, params):
    global __glGetVertexAttribfv_impl
    if not __glGetVertexAttribfv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexAttribfv')
        if not fptr:
            raise RuntimeError('The function glGetVertexAttribfv is not available')
        __glGetVertexAttribfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetVertexAttribfv = (lambda index,pname,params:__glGetVertexAttribfv_impl(index,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetVertexAttribfv(index, pname, params)
# <command>
#            <proto>void <name>glGetVertexAttribiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param group="VertexAttribPropertyARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="4"><ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="1303" type="vendor" />
#        </command>
#        
__glGetVertexAttribiv_impl=None
def glGetVertexAttribiv (index, pname, params):
    global __glGetVertexAttribiv_impl
    if not __glGetVertexAttribiv_impl:
        fptr = __pyglGetFuncAddress('glGetVertexAttribiv')
        if not fptr:
            raise RuntimeError('The function glGetVertexAttribiv is not available')
        __glGetVertexAttribiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glGetVertexAttribiv = (lambda index,pname,params:__glGetVertexAttribiv_impl(index,pname,(c_uint8*len( params )).from_buffer( params )))
    return glGetVertexAttribiv(index, pname, params)
# <command>
#            <proto>void <name>glGetnCompressedTexImage</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLint</ptype> <name>lod</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param>void *<name>pixels</name></param>
#        </command>
#        
__glGetnCompressedTexImage_impl=None
def glGetnCompressedTexImage (target, lod, bufSize, pixels):
    global __glGetnCompressedTexImage_impl
    if not __glGetnCompressedTexImage_impl:
        fptr = __pyglGetFuncAddress('glGetnCompressedTexImage')
        if not fptr:
            raise RuntimeError('The function glGetnCompressedTexImage is not available')
        __glGetnCompressedTexImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glGetnCompressedTexImage = (lambda target,lod,bufSize,pixels:__glGetnCompressedTexImage_impl(target,lod,bufSize,(c_uint8*len( pixels )).from_buffer( pixels )))
    return glGetnCompressedTexImage(target, lod, bufSize, pixels)
# <command>
#            <proto>void <name>glGetnTexImage</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param>void *<name>pixels</name></param>
#        </command>
#        
__glGetnTexImage_impl=None
def glGetnTexImage (target, level, format, type, bufSize, pixels):
    global __glGetnTexImage_impl
    if not __glGetnTexImage_impl:
        fptr = __pyglGetFuncAddress('glGetnTexImage')
        if not fptr:
            raise RuntimeError('The function glGetnTexImage is not available')
        __glGetnTexImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_uint, c_int, c_void_p)(fptr)
    glGetnTexImage = (lambda target,level,format,type,bufSize,pixels:__glGetnTexImage_impl(target,level,format,type,bufSize,(c_uint8*len( pixels )).from_buffer( pixels )))
    return glGetnTexImage(target, level, format, type, bufSize, pixels)
# <command>
#            <proto>void <name>glGetnUniformdv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param><ptype>GLdouble</ptype> *<name>params</name></param>
#        </command>
#        
__glGetnUniformdv_impl=None
def glGetnUniformdv (program, location, bufSize, params):
    global __glGetnUniformdv_impl
    if not __glGetnUniformdv_impl:
        fptr = __pyglGetFuncAddress('glGetnUniformdv')
        if not fptr:
            raise RuntimeError('The function glGetnUniformdv is not available')
        __glGetnUniformdv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glGetnUniformdv = (lambda program,location,bufSize,params:__glGetnUniformdv_impl(program,location,bufSize,(c_uint8*len( params )).from_buffer( params )))
    return glGetnUniformdv(program, location, bufSize, params)
# <command>
#            <proto>void <name>glGetnUniformfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param><ptype>GLfloat</ptype> *<name>params</name></param>
#        </command>
#        
__glGetnUniformfv_impl=None
def glGetnUniformfv (program, location, bufSize, params):
    global __glGetnUniformfv_impl
    if not __glGetnUniformfv_impl:
        fptr = __pyglGetFuncAddress('glGetnUniformfv')
        if not fptr:
            raise RuntimeError('The function glGetnUniformfv is not available')
        __glGetnUniformfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glGetnUniformfv = (lambda program,location,bufSize,params:__glGetnUniformfv_impl(program,location,bufSize,(c_uint8*len( params )).from_buffer( params )))
    return glGetnUniformfv(program, location, bufSize, params)
# <command>
#            <proto>void <name>glGetnUniformiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param><ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetnUniformiv_impl=None
def glGetnUniformiv (program, location, bufSize, params):
    global __glGetnUniformiv_impl
    if not __glGetnUniformiv_impl:
        fptr = __pyglGetFuncAddress('glGetnUniformiv')
        if not fptr:
            raise RuntimeError('The function glGetnUniformiv is not available')
        __glGetnUniformiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glGetnUniformiv = (lambda program,location,bufSize,params:__glGetnUniformiv_impl(program,location,bufSize,(c_uint8*len( params )).from_buffer( params )))
    return glGetnUniformiv(program, location, bufSize, params)
# <command>
#            <proto>void <name>glGetnUniformuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param><ptype>GLuint</ptype> *<name>params</name></param>
#        </command>
#        
__glGetnUniformuiv_impl=None
def glGetnUniformuiv (program, location, bufSize, params):
    global __glGetnUniformuiv_impl
    if not __glGetnUniformuiv_impl:
        fptr = __pyglGetFuncAddress('glGetnUniformuiv')
        if not fptr:
            raise RuntimeError('The function glGetnUniformuiv is not available')
        __glGetnUniformuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glGetnUniformuiv = (lambda program,location,bufSize,params:__glGetnUniformuiv_impl(program,location,bufSize,(c_uint8*len( params )).from_buffer( params )))
    return glGetnUniformuiv(program, location, bufSize, params)
# <command>
#            <proto>void <name>glHint</name></proto>
#            <param group="HintTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="HintMode"><ptype>GLenum</ptype> <name>mode</name></param>
#            <glx opcode="85" type="render" />
#        </command>
#        
__glHint_impl=None
def glHint (target, mode):
    global __glHint_impl
    if not __glHint_impl:
        fptr = __pyglGetFuncAddress('glHint')
        if not fptr:
            raise RuntimeError('The function glHint is not available')
        __glHint_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glHint = __glHint_impl
    return glHint(target, mode)
# <command>
#            <proto>void <name>glInvalidateBufferData</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#        </command>
#        
__glInvalidateBufferData_impl=None
def glInvalidateBufferData (buffer):
    global __glInvalidateBufferData_impl
    if not __glInvalidateBufferData_impl:
        fptr = __pyglGetFuncAddress('glInvalidateBufferData')
        if not fptr:
            raise RuntimeError('The function glInvalidateBufferData is not available')
        __glInvalidateBufferData_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glInvalidateBufferData = __glInvalidateBufferData_impl
    return glInvalidateBufferData(buffer)
# <command>
#            <proto>void <name>glInvalidateBufferSubData</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>length</name></param>
#        </command>
#        
__glInvalidateBufferSubData_impl=None
def glInvalidateBufferSubData (buffer, offset, length):
    global __glInvalidateBufferSubData_impl
    if not __glInvalidateBufferSubData_impl:
        fptr = __pyglGetFuncAddress('glInvalidateBufferSubData')
        if not fptr:
            raise RuntimeError('The function glInvalidateBufferSubData is not available')
        __glInvalidateBufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_size_t, c_void_p)(fptr)
    glInvalidateBufferSubData = __glInvalidateBufferSubData_impl
    return glInvalidateBufferSubData(buffer, offset, length)
# <command>
#            <proto>void <name>glInvalidateFramebuffer</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLsizei</ptype> <name>numAttachments</name></param>
#            <param len="numAttachments">const <ptype>GLenum</ptype> *<name>attachments</name></param>
#        </command>
#        
__glInvalidateFramebuffer_impl=None
def glInvalidateFramebuffer (target, numAttachments, attachments):
    global __glInvalidateFramebuffer_impl
    if not __glInvalidateFramebuffer_impl:
        fptr = __pyglGetFuncAddress('glInvalidateFramebuffer')
        if not fptr:
            raise RuntimeError('The function glInvalidateFramebuffer is not available')
        __glInvalidateFramebuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glInvalidateFramebuffer = (lambda target,numAttachments,attachments:__glInvalidateFramebuffer_impl(target,numAttachments,__pyglGetAsConstVoidPointer( attachments )))
    return glInvalidateFramebuffer(target, numAttachments, attachments)
# <command>
#            <proto>void <name>glInvalidateNamedFramebufferData</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLsizei</ptype> <name>numAttachments</name></param>
#            <param>const <ptype>GLenum</ptype> *<name>attachments</name></param>
#        </command>
#        
__glInvalidateNamedFramebufferData_impl=None
def glInvalidateNamedFramebufferData (framebuffer, numAttachments, attachments):
    global __glInvalidateNamedFramebufferData_impl
    if not __glInvalidateNamedFramebufferData_impl:
        fptr = __pyglGetFuncAddress('glInvalidateNamedFramebufferData')
        if not fptr:
            raise RuntimeError('The function glInvalidateNamedFramebufferData is not available')
        __glInvalidateNamedFramebufferData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glInvalidateNamedFramebufferData = (lambda framebuffer,numAttachments,attachments:__glInvalidateNamedFramebufferData_impl(framebuffer,numAttachments,__pyglGetAsConstVoidPointer( attachments )))
    return glInvalidateNamedFramebufferData(framebuffer, numAttachments, attachments)
# <command>
#            <proto>void <name>glInvalidateNamedFramebufferSubData</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLsizei</ptype> <name>numAttachments</name></param>
#            <param>const <ptype>GLenum</ptype> *<name>attachments</name></param>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <param><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#        </command>
#        
__glInvalidateNamedFramebufferSubData_impl=None
def glInvalidateNamedFramebufferSubData (framebuffer, numAttachments, attachments, x, y, width, height):
    global __glInvalidateNamedFramebufferSubData_impl
    if not __glInvalidateNamedFramebufferSubData_impl:
        fptr = __pyglGetFuncAddress('glInvalidateNamedFramebufferSubData')
        if not fptr:
            raise RuntimeError('The function glInvalidateNamedFramebufferSubData is not available')
        __glInvalidateNamedFramebufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_int, c_int, c_int, c_int)(fptr)
    glInvalidateNamedFramebufferSubData = (lambda framebuffer,numAttachments,attachments,x,y,width,height:__glInvalidateNamedFramebufferSubData_impl(framebuffer,numAttachments,__pyglGetAsConstVoidPointer( attachments ),x,y,width,height))
    return glInvalidateNamedFramebufferSubData(framebuffer, numAttachments, attachments, x, y, width, height)
# <command>
#            <proto>void <name>glInvalidateSubFramebuffer</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLsizei</ptype> <name>numAttachments</name></param>
#            <param len="numAttachments">const <ptype>GLenum</ptype> *<name>attachments</name></param>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <param><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#        </command>
#        
__glInvalidateSubFramebuffer_impl=None
def glInvalidateSubFramebuffer (target, numAttachments, attachments, x, y, width, height):
    global __glInvalidateSubFramebuffer_impl
    if not __glInvalidateSubFramebuffer_impl:
        fptr = __pyglGetFuncAddress('glInvalidateSubFramebuffer')
        if not fptr:
            raise RuntimeError('The function glInvalidateSubFramebuffer is not available')
        __glInvalidateSubFramebuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_int, c_int, c_int, c_int)(fptr)
    glInvalidateSubFramebuffer = (lambda target,numAttachments,attachments,x,y,width,height:__glInvalidateSubFramebuffer_impl(target,numAttachments,__pyglGetAsConstVoidPointer( attachments ),x,y,width,height))
    return glInvalidateSubFramebuffer(target, numAttachments, attachments, x, y, width, height)
# <command>
#            <proto>void <name>glInvalidateTexImage</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#        </command>
#        
__glInvalidateTexImage_impl=None
def glInvalidateTexImage (texture, level):
    global __glInvalidateTexImage_impl
    if not __glInvalidateTexImage_impl:
        fptr = __pyglGetFuncAddress('glInvalidateTexImage')
        if not fptr:
            raise RuntimeError('The function glInvalidateTexImage is not available')
        __glInvalidateTexImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int)(fptr)
    glInvalidateTexImage = __glInvalidateTexImage_impl
    return glInvalidateTexImage(texture, level)
# <command>
#            <proto>void <name>glInvalidateTexSubImage</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#        </command>
#        
__glInvalidateTexSubImage_impl=None
def glInvalidateTexSubImage (texture, level, xoffset, yoffset, zoffset, width, height, depth):
    global __glInvalidateTexSubImage_impl
    if not __glInvalidateTexSubImage_impl:
        fptr = __pyglGetFuncAddress('glInvalidateTexSubImage')
        if not fptr:
            raise RuntimeError('The function glInvalidateTexSubImage is not available')
        __glInvalidateTexSubImage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int)(fptr)
    glInvalidateTexSubImage = __glInvalidateTexSubImage_impl
    return glInvalidateTexSubImage(texture, level, xoffset, yoffset, zoffset, width, height, depth)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsBuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#        </command>
#        
__glIsBuffer_impl=None
def glIsBuffer (buffer):
    global __glIsBuffer_impl
    if not __glIsBuffer_impl:
        fptr = __pyglGetFuncAddress('glIsBuffer')
        if not fptr:
            raise RuntimeError('The function glIsBuffer is not available')
        __glIsBuffer_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsBuffer = __glIsBuffer_impl
    return glIsBuffer(buffer)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsEnabled</name></proto>
#            <param group="EnableCap"><ptype>GLenum</ptype> <name>cap</name></param>
#            <glx opcode="140" type="single" />
#        </command>
#        
__glIsEnabled_impl=None
def glIsEnabled (cap):
    global __glIsEnabled_impl
    if not __glIsEnabled_impl:
        fptr = __pyglGetFuncAddress('glIsEnabled')
        if not fptr:
            raise RuntimeError('The function glIsEnabled is not available')
        __glIsEnabled_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsEnabled = __glIsEnabled_impl
    return glIsEnabled(cap)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsEnabledi</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glIsEnabledi_impl=None
def glIsEnabledi (target, index):
    global __glIsEnabledi_impl
    if not __glIsEnabledi_impl:
        fptr = __pyglGetFuncAddress('glIsEnabledi')
        if not fptr:
            raise RuntimeError('The function glIsEnabledi is not available')
        __glIsEnabledi_impl = __PYGL_FUNC_TYPE( c_char ,c_uint, c_uint)(fptr)
    glIsEnabledi = __glIsEnabledi_impl
    return glIsEnabledi(target, index)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsFramebuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <glx opcode="1425" type="vendor" />
#        </command>
#        
__glIsFramebuffer_impl=None
def glIsFramebuffer (framebuffer):
    global __glIsFramebuffer_impl
    if not __glIsFramebuffer_impl:
        fptr = __pyglGetFuncAddress('glIsFramebuffer')
        if not fptr:
            raise RuntimeError('The function glIsFramebuffer is not available')
        __glIsFramebuffer_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsFramebuffer = __glIsFramebuffer_impl
    return glIsFramebuffer(framebuffer)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsProgram</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <glx opcode="197" type="single" />
#        </command>
#        
__glIsProgram_impl=None
def glIsProgram (program):
    global __glIsProgram_impl
    if not __glIsProgram_impl:
        fptr = __pyglGetFuncAddress('glIsProgram')
        if not fptr:
            raise RuntimeError('The function glIsProgram is not available')
        __glIsProgram_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsProgram = __glIsProgram_impl
    return glIsProgram(program)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsProgramPipeline</name></proto>
#            <param><ptype>GLuint</ptype> <name>pipeline</name></param>
#        </command>
#        
__glIsProgramPipeline_impl=None
def glIsProgramPipeline (pipeline):
    global __glIsProgramPipeline_impl
    if not __glIsProgramPipeline_impl:
        fptr = __pyglGetFuncAddress('glIsProgramPipeline')
        if not fptr:
            raise RuntimeError('The function glIsProgramPipeline is not available')
        __glIsProgramPipeline_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsProgramPipeline = __glIsProgramPipeline_impl
    return glIsProgramPipeline(pipeline)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsQuery</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <glx opcode="163" type="single" />
#        </command>
#        
__glIsQuery_impl=None
def glIsQuery (id):
    global __glIsQuery_impl
    if not __glIsQuery_impl:
        fptr = __pyglGetFuncAddress('glIsQuery')
        if not fptr:
            raise RuntimeError('The function glIsQuery is not available')
        __glIsQuery_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsQuery = __glIsQuery_impl
    return glIsQuery(id)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsRenderbuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>renderbuffer</name></param>
#            <glx opcode="1422" type="vendor" />
#        </command>
#        
__glIsRenderbuffer_impl=None
def glIsRenderbuffer (renderbuffer):
    global __glIsRenderbuffer_impl
    if not __glIsRenderbuffer_impl:
        fptr = __pyglGetFuncAddress('glIsRenderbuffer')
        if not fptr:
            raise RuntimeError('The function glIsRenderbuffer is not available')
        __glIsRenderbuffer_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsRenderbuffer = __glIsRenderbuffer_impl
    return glIsRenderbuffer(renderbuffer)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsSampler</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#        </command>
#        
__glIsSampler_impl=None
def glIsSampler (sampler):
    global __glIsSampler_impl
    if not __glIsSampler_impl:
        fptr = __pyglGetFuncAddress('glIsSampler')
        if not fptr:
            raise RuntimeError('The function glIsSampler is not available')
        __glIsSampler_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsSampler = __glIsSampler_impl
    return glIsSampler(sampler)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsShader</name></proto>
#            <param><ptype>GLuint</ptype> <name>shader</name></param>
#            <glx opcode="196" type="single" />
#        </command>
#        
__glIsShader_impl=None
def glIsShader (shader):
    global __glIsShader_impl
    if not __glIsShader_impl:
        fptr = __pyglGetFuncAddress('glIsShader')
        if not fptr:
            raise RuntimeError('The function glIsShader is not available')
        __glIsShader_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsShader = __glIsShader_impl
    return glIsShader(shader)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsSync</name></proto>
#            <param group="sync"><ptype>GLsync</ptype> <name>sync</name></param>
#        </command>
#        
__glIsSync_impl=None
def glIsSync (sync):
    global __glIsSync_impl
    if not __glIsSync_impl:
        fptr = __pyglGetFuncAddress('glIsSync')
        if not fptr:
            raise RuntimeError('The function glIsSync is not available')
        __glIsSync_impl = __PYGL_FUNC_TYPE( c_char ,c_void_p)(fptr)
    glIsSync = __glIsSync_impl
    return glIsSync(sync)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsTexture</name></proto>
#            <param group="Texture"><ptype>GLuint</ptype> <name>texture</name></param>
#            <glx opcode="146" type="single" />
#        </command>
#        
__glIsTexture_impl=None
def glIsTexture (texture):
    global __glIsTexture_impl
    if not __glIsTexture_impl:
        fptr = __pyglGetFuncAddress('glIsTexture')
        if not fptr:
            raise RuntimeError('The function glIsTexture is not available')
        __glIsTexture_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsTexture = __glIsTexture_impl
    return glIsTexture(texture)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsTransformFeedback</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#        </command>
#        
__glIsTransformFeedback_impl=None
def glIsTransformFeedback (id):
    global __glIsTransformFeedback_impl
    if not __glIsTransformFeedback_impl:
        fptr = __pyglGetFuncAddress('glIsTransformFeedback')
        if not fptr:
            raise RuntimeError('The function glIsTransformFeedback is not available')
        __glIsTransformFeedback_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsTransformFeedback = __glIsTransformFeedback_impl
    return glIsTransformFeedback(id)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glIsVertexArray</name></proto>
#            <param><ptype>GLuint</ptype> <name>array</name></param>
#            <glx opcode="207" type="single" />
#        </command>
#        
__glIsVertexArray_impl=None
def glIsVertexArray (array):
    global __glIsVertexArray_impl
    if not __glIsVertexArray_impl:
        fptr = __pyglGetFuncAddress('glIsVertexArray')
        if not fptr:
            raise RuntimeError('The function glIsVertexArray is not available')
        __glIsVertexArray_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glIsVertexArray = __glIsVertexArray_impl
    return glIsVertexArray(array)
# <command>
#            <proto>void <name>glLineWidth</name></proto>
#            <param group="CheckedFloat32"><ptype>GLfloat</ptype> <name>width</name></param>
#            <glx opcode="95" type="render" />
#        </command>
#        
__glLineWidth_impl=None
def glLineWidth (width):
    global __glLineWidth_impl
    if not __glLineWidth_impl:
        fptr = __pyglGetFuncAddress('glLineWidth')
        if not fptr:
            raise RuntimeError('The function glLineWidth is not available')
        __glLineWidth_impl = __PYGL_FUNC_TYPE( None ,c_float)(fptr)
    glLineWidth = __glLineWidth_impl
    return glLineWidth(width)
# <command>
#            <proto>void <name>glLinkProgram</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#        </command>
#        
__glLinkProgram_impl=None
def glLinkProgram (program):
    global __glLinkProgram_impl
    if not __glLinkProgram_impl:
        fptr = __pyglGetFuncAddress('glLinkProgram')
        if not fptr:
            raise RuntimeError('The function glLinkProgram is not available')
        __glLinkProgram_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glLinkProgram = __glLinkProgram_impl
    return glLinkProgram(program)
# <command>
#            <proto>void <name>glLogicOp</name></proto>
#            <param group="LogicOp"><ptype>GLenum</ptype> <name>opcode</name></param>
#            <glx opcode="161" type="render" />
#        </command>
#        
__glLogicOp_impl=None
def glLogicOp (opcode):
    global __glLogicOp_impl
    if not __glLogicOp_impl:
        fptr = __pyglGetFuncAddress('glLogicOp')
        if not fptr:
            raise RuntimeError('The function glLogicOp is not available')
        __glLogicOp_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glLogicOp = __glLogicOp_impl
    return glLogicOp(opcode)
# <command>
#            <proto>void *<name>glMapBuffer</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="BufferAccessARB"><ptype>GLenum</ptype> <name>access</name></param>
#        </command>
#        
__glMapBuffer_impl=None
def glMapBuffer (target, access):
    global __glMapBuffer_impl
    if not __glMapBuffer_impl:
        fptr = __pyglGetFuncAddress('glMapBuffer')
        if not fptr:
            raise RuntimeError('The function glMapBuffer is not available')
        __glMapBuffer_impl = __PYGL_FUNC_TYPE( c_void_p ,c_uint, c_uint)(fptr)
    glMapBuffer = __glMapBuffer_impl
    return glMapBuffer(target, access)
# <command>
#            <proto>void *<name>glMapBufferRange</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>length</name></param>
#            <param group="BufferAccessMask"><ptype>GLbitfield</ptype> <name>access</name></param>
#            <glx opcode="205" type="single" />
#        </command>
#        
__glMapBufferRange_impl=None
def glMapBufferRange (target, offset, length, access):
    global __glMapBufferRange_impl
    if not __glMapBufferRange_impl:
        fptr = __pyglGetFuncAddress('glMapBufferRange')
        if not fptr:
            raise RuntimeError('The function glMapBufferRange is not available')
        __glMapBufferRange_impl = __PYGL_FUNC_TYPE( c_void_p ,c_uint, c_size_t, c_void_p, c_uint)(fptr)
    glMapBufferRange = __glMapBufferRange_impl
    return glMapBufferRange(target, offset, length, access)
# <command>
#            <proto>void *<name>glMapNamedBuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLenum</ptype> <name>access</name></param>
#        </command>
#        
__glMapNamedBuffer_impl=None
def glMapNamedBuffer (buffer, access):
    global __glMapNamedBuffer_impl
    if not __glMapNamedBuffer_impl:
        fptr = __pyglGetFuncAddress('glMapNamedBuffer')
        if not fptr:
            raise RuntimeError('The function glMapNamedBuffer is not available')
        __glMapNamedBuffer_impl = __PYGL_FUNC_TYPE( c_void_p ,c_uint, c_uint)(fptr)
    glMapNamedBuffer = __glMapNamedBuffer_impl
    return glMapNamedBuffer(buffer, access)
# <command>
#            <proto>void *<name>glMapNamedBufferRange</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>length</name></param>
#            <param><ptype>GLbitfield</ptype> <name>access</name></param>
#        </command>
#        
__glMapNamedBufferRange_impl=None
def glMapNamedBufferRange (buffer, offset, length, access):
    global __glMapNamedBufferRange_impl
    if not __glMapNamedBufferRange_impl:
        fptr = __pyglGetFuncAddress('glMapNamedBufferRange')
        if not fptr:
            raise RuntimeError('The function glMapNamedBufferRange is not available')
        __glMapNamedBufferRange_impl = __PYGL_FUNC_TYPE( c_void_p ,c_uint, c_size_t, c_void_p, c_uint)(fptr)
    glMapNamedBufferRange = __glMapNamedBufferRange_impl
    return glMapNamedBufferRange(buffer, offset, length, access)
# <command>
#            <proto>void <name>glMemoryBarrier</name></proto>
#            <param><ptype>GLbitfield</ptype> <name>barriers</name></param>
#        </command>
#        
__glMemoryBarrier_impl=None
def glMemoryBarrier (barriers):
    global __glMemoryBarrier_impl
    if not __glMemoryBarrier_impl:
        fptr = __pyglGetFuncAddress('glMemoryBarrier')
        if not fptr:
            raise RuntimeError('The function glMemoryBarrier is not available')
        __glMemoryBarrier_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glMemoryBarrier = __glMemoryBarrier_impl
    return glMemoryBarrier(barriers)
# <command>
#            <proto>void <name>glMemoryBarrierByRegion</name></proto>
#            <param><ptype>GLbitfield</ptype> <name>barriers</name></param>
#        </command>
#        
__glMemoryBarrierByRegion_impl=None
def glMemoryBarrierByRegion (barriers):
    global __glMemoryBarrierByRegion_impl
    if not __glMemoryBarrierByRegion_impl:
        fptr = __pyglGetFuncAddress('glMemoryBarrierByRegion')
        if not fptr:
            raise RuntimeError('The function glMemoryBarrierByRegion is not available')
        __glMemoryBarrierByRegion_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glMemoryBarrierByRegion = __glMemoryBarrierByRegion_impl
    return glMemoryBarrierByRegion(barriers)
# <command>
#            <proto>void <name>glMinSampleShading</name></proto>
#            <param group="ColorF"><ptype>GLfloat</ptype> <name>value</name></param>
#        </command>
#        
__glMinSampleShading_impl=None
def glMinSampleShading (value):
    global __glMinSampleShading_impl
    if not __glMinSampleShading_impl:
        fptr = __pyglGetFuncAddress('glMinSampleShading')
        if not fptr:
            raise RuntimeError('The function glMinSampleShading is not available')
        __glMinSampleShading_impl = __PYGL_FUNC_TYPE( None ,c_float)(fptr)
    glMinSampleShading = __glMinSampleShading_impl
    return glMinSampleShading(value)
# <command>
#            <proto>void <name>glMultiDrawArrays</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param len="COMPSIZE(count)">const <ptype>GLint</ptype> *<name>first</name></param>
#            <param len="COMPSIZE(drawcount)">const <ptype>GLsizei</ptype> *<name>count</name></param>
#            <param><ptype>GLsizei</ptype> <name>drawcount</name></param>
#        </command>
#        
__glMultiDrawArrays_impl=None
def glMultiDrawArrays (mode, first, count, drawcount):
    global __glMultiDrawArrays_impl
    if not __glMultiDrawArrays_impl:
        fptr = __pyglGetFuncAddress('glMultiDrawArrays')
        if not fptr:
            raise RuntimeError('The function glMultiDrawArrays is not available')
        __glMultiDrawArrays_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p, c_void_p, c_int)(fptr)
    glMultiDrawArrays = (lambda mode,first,count,drawcount:__glMultiDrawArrays_impl(mode,__pyglGetAsConstVoidPointer( first ),__pyglGetAsConstVoidPointer( count ),drawcount))
    return glMultiDrawArrays(mode, first, count, drawcount)
# <command>
#            <proto>void <name>glMultiDrawArraysIndirect</name></proto>
#            <param><ptype>GLenum</ptype> <name>mode</name></param>
#            <param len="COMPSIZE(drawcount,stride)">const void *<name>indirect</name></param>
#            <param><ptype>GLsizei</ptype> <name>drawcount</name></param>
#            <param><ptype>GLsizei</ptype> <name>stride</name></param>
#        </command>
#        
__glMultiDrawArraysIndirect_impl=None
def glMultiDrawArraysIndirect (mode, indirect, drawcount, stride):
    global __glMultiDrawArraysIndirect_impl
    if not __glMultiDrawArraysIndirect_impl:
        fptr = __pyglGetFuncAddress('glMultiDrawArraysIndirect')
        if not fptr:
            raise RuntimeError('The function glMultiDrawArraysIndirect is not available')
        __glMultiDrawArraysIndirect_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p, c_int, c_int)(fptr)
    glMultiDrawArraysIndirect = (lambda mode,indirect,drawcount,stride:__glMultiDrawArraysIndirect_impl(mode,__pyglGetAsConstVoidPointer( indirect ),drawcount,stride))
    return glMultiDrawArraysIndirect(mode, indirect, drawcount, stride)
# <command>
#            <proto>void <name>glMultiDrawElements</name></proto>
#            <param group="PrimitiveType"><ptype>GLenum</ptype> <name>mode</name></param>
#            <param len="COMPSIZE(drawcount)">const <ptype>GLsizei</ptype> *<name>count</name></param>
#            <param group="DrawElementsType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(drawcount)">const void *const*<name>indices</name></param>
#            <param><ptype>GLsizei</ptype> <name>drawcount</name></param>
#        </command>
#        
__glMultiDrawElements_impl=None
def glMultiDrawElements (mode, count, type, indices, drawcount):
    global __glMultiDrawElements_impl
    if not __glMultiDrawElements_impl:
        fptr = __pyglGetFuncAddress('glMultiDrawElements')
        if not fptr:
            raise RuntimeError('The function glMultiDrawElements is not available')
        __glMultiDrawElements_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p, c_uint, c_void_p, c_int)(fptr)
    glMultiDrawElements = (lambda mode,count,type,indices,drawcount:__glMultiDrawElements_impl(mode,__pyglGetAsConstVoidPointer( count ),type,__pyglGetAsConstVoidPointer( indices ),drawcount))
    return glMultiDrawElements(mode, count, type, indices, drawcount)
# <command>
#            <proto>void <name>glMultiDrawElementsBaseVertex</name></proto>
#            <param><ptype>GLenum</ptype> <name>mode</name></param>
#            <param len="COMPSIZE(drawcount)">const <ptype>GLsizei</ptype> *<name>count</name></param>
#            <param group="DrawElementsType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(drawcount)">const void *const*<name>indices</name></param>
#            <param><ptype>GLsizei</ptype> <name>drawcount</name></param>
#            <param len="COMPSIZE(drawcount)">const <ptype>GLint</ptype> *<name>basevertex</name></param>
#        </command>
#        
__glMultiDrawElementsBaseVertex_impl=None
def glMultiDrawElementsBaseVertex (mode, count, type, indices, drawcount, basevertex):
    global __glMultiDrawElementsBaseVertex_impl
    if not __glMultiDrawElementsBaseVertex_impl:
        fptr = __pyglGetFuncAddress('glMultiDrawElementsBaseVertex')
        if not fptr:
            raise RuntimeError('The function glMultiDrawElementsBaseVertex is not available')
        __glMultiDrawElementsBaseVertex_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p, c_uint, c_void_p, c_int, c_void_p)(fptr)
    glMultiDrawElementsBaseVertex = (lambda mode,count,type,indices,drawcount,basevertex:__glMultiDrawElementsBaseVertex_impl(mode,__pyglGetAsConstVoidPointer( count ),type,__pyglGetAsConstVoidPointer( indices ),drawcount,__pyglGetAsConstVoidPointer( basevertex )))
    return glMultiDrawElementsBaseVertex(mode, count, type, indices, drawcount, basevertex)
# <command>
#            <proto>void <name>glMultiDrawElementsIndirect</name></proto>
#            <param><ptype>GLenum</ptype> <name>mode</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(drawcount,stride)">const void *<name>indirect</name></param>
#            <param><ptype>GLsizei</ptype> <name>drawcount</name></param>
#            <param><ptype>GLsizei</ptype> <name>stride</name></param>
#        </command>
#        
__glMultiDrawElementsIndirect_impl=None
def glMultiDrawElementsIndirect (mode, type, indirect, drawcount, stride):
    global __glMultiDrawElementsIndirect_impl
    if not __glMultiDrawElementsIndirect_impl:
        fptr = __pyglGetFuncAddress('glMultiDrawElementsIndirect')
        if not fptr:
            raise RuntimeError('The function glMultiDrawElementsIndirect is not available')
        __glMultiDrawElementsIndirect_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p, c_int, c_int)(fptr)
    glMultiDrawElementsIndirect = (lambda mode,type,indirect,drawcount,stride:__glMultiDrawElementsIndirect_impl(mode,type,__pyglGetAsConstVoidPointer( indirect ),drawcount,stride))
    return glMultiDrawElementsIndirect(mode, type, indirect, drawcount, stride)
# <command>
#            <proto>void <name>glNamedBufferData</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param>const void *<name>data</name></param>
#            <param><ptype>GLenum</ptype> <name>usage</name></param>
#        </command>
#        
__glNamedBufferData_impl=None
def glNamedBufferData (buffer, size, data, usage):
    global __glNamedBufferData_impl
    if not __glNamedBufferData_impl:
        fptr = __pyglGetFuncAddress('glNamedBufferData')
        if not fptr:
            raise RuntimeError('The function glNamedBufferData is not available')
        __glNamedBufferData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p, c_void_p, c_uint)(fptr)
    glNamedBufferData = (lambda buffer,size,data,usage:__glNamedBufferData_impl(buffer,size,__pyglGetAsConstVoidPointer( data ),usage))
    return glNamedBufferData(buffer, size, data, usage)
# <command>
#            <proto>void <name>glNamedBufferStorage</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param len="size">const void *<name>data</name></param>
#            <param><ptype>GLbitfield</ptype> <name>flags</name></param>
#        </command>
#        
__glNamedBufferStorage_impl=None
def glNamedBufferStorage (buffer, size, data, flags):
    global __glNamedBufferStorage_impl
    if not __glNamedBufferStorage_impl:
        fptr = __pyglGetFuncAddress('glNamedBufferStorage')
        if not fptr:
            raise RuntimeError('The function glNamedBufferStorage is not available')
        __glNamedBufferStorage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p, c_void_p, c_uint)(fptr)
    glNamedBufferStorage = (lambda buffer,size,data,flags:__glNamedBufferStorage_impl(buffer,size,__pyglGetAsConstVoidPointer( data ),flags))
    return glNamedBufferStorage(buffer, size, data, flags)
# <command>
#            <proto>void <name>glNamedBufferSubData</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#            <param len="COMPSIZE(size)">const void *<name>data</name></param>
#        </command>
#        
__glNamedBufferSubData_impl=None
def glNamedBufferSubData (buffer, offset, size, data):
    global __glNamedBufferSubData_impl
    if not __glNamedBufferSubData_impl:
        fptr = __pyglGetFuncAddress('glNamedBufferSubData')
        if not fptr:
            raise RuntimeError('The function glNamedBufferSubData is not available')
        __glNamedBufferSubData_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_size_t, c_void_p, c_void_p)(fptr)
    glNamedBufferSubData = (lambda buffer,offset,size,data:__glNamedBufferSubData_impl(buffer,offset,size,__pyglGetAsConstVoidPointer( data )))
    return glNamedBufferSubData(buffer, offset, size, data)
# <command>
#            <proto>void <name>glNamedFramebufferDrawBuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>buf</name></param>
#        </command>
#        
__glNamedFramebufferDrawBuffer_impl=None
def glNamedFramebufferDrawBuffer (framebuffer, buf):
    global __glNamedFramebufferDrawBuffer_impl
    if not __glNamedFramebufferDrawBuffer_impl:
        fptr = __pyglGetFuncAddress('glNamedFramebufferDrawBuffer')
        if not fptr:
            raise RuntimeError('The function glNamedFramebufferDrawBuffer is not available')
        __glNamedFramebufferDrawBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glNamedFramebufferDrawBuffer = __glNamedFramebufferDrawBuffer_impl
    return glNamedFramebufferDrawBuffer(framebuffer, buf)
# <command>
#            <proto>void <name>glNamedFramebufferDrawBuffers</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLsizei</ptype> <name>n</name></param>
#            <param>const <ptype>GLenum</ptype> *<name>bufs</name></param>
#        </command>
#        
__glNamedFramebufferDrawBuffers_impl=None
def glNamedFramebufferDrawBuffers (framebuffer, n, bufs):
    global __glNamedFramebufferDrawBuffers_impl
    if not __glNamedFramebufferDrawBuffers_impl:
        fptr = __pyglGetFuncAddress('glNamedFramebufferDrawBuffers')
        if not fptr:
            raise RuntimeError('The function glNamedFramebufferDrawBuffers is not available')
        __glNamedFramebufferDrawBuffers_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glNamedFramebufferDrawBuffers = (lambda framebuffer,n,bufs:__glNamedFramebufferDrawBuffers_impl(framebuffer,n,__pyglGetAsConstVoidPointer( bufs )))
    return glNamedFramebufferDrawBuffers(framebuffer, n, bufs)
# <command>
#            <proto>void <name>glNamedFramebufferParameteri</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> <name>param</name></param>
#        </command>
#        
__glNamedFramebufferParameteri_impl=None
def glNamedFramebufferParameteri (framebuffer, pname, param):
    global __glNamedFramebufferParameteri_impl
    if not __glNamedFramebufferParameteri_impl:
        fptr = __pyglGetFuncAddress('glNamedFramebufferParameteri')
        if not fptr:
            raise RuntimeError('The function glNamedFramebufferParameteri is not available')
        __glNamedFramebufferParameteri_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int)(fptr)
    glNamedFramebufferParameteri = __glNamedFramebufferParameteri_impl
    return glNamedFramebufferParameteri(framebuffer, pname, param)
# <command>
#            <proto>void <name>glNamedFramebufferReadBuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>src</name></param>
#        </command>
#        
__glNamedFramebufferReadBuffer_impl=None
def glNamedFramebufferReadBuffer (framebuffer, src):
    global __glNamedFramebufferReadBuffer_impl
    if not __glNamedFramebufferReadBuffer_impl:
        fptr = __pyglGetFuncAddress('glNamedFramebufferReadBuffer')
        if not fptr:
            raise RuntimeError('The function glNamedFramebufferReadBuffer is not available')
        __glNamedFramebufferReadBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glNamedFramebufferReadBuffer = __glNamedFramebufferReadBuffer_impl
    return glNamedFramebufferReadBuffer(framebuffer, src)
# <command>
#            <proto>void <name>glNamedFramebufferRenderbuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param><ptype>GLenum</ptype> <name>renderbuffertarget</name></param>
#            <param><ptype>GLuint</ptype> <name>renderbuffer</name></param>
#        </command>
#        
__glNamedFramebufferRenderbuffer_impl=None
def glNamedFramebufferRenderbuffer (framebuffer, attachment, renderbuffertarget, renderbuffer):
    global __glNamedFramebufferRenderbuffer_impl
    if not __glNamedFramebufferRenderbuffer_impl:
        fptr = __pyglGetFuncAddress('glNamedFramebufferRenderbuffer')
        if not fptr:
            raise RuntimeError('The function glNamedFramebufferRenderbuffer is not available')
        __glNamedFramebufferRenderbuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint)(fptr)
    glNamedFramebufferRenderbuffer = __glNamedFramebufferRenderbuffer_impl
    return glNamedFramebufferRenderbuffer(framebuffer, attachment, renderbuffertarget, renderbuffer)
# <command>
#            <proto>void <name>glNamedFramebufferTexture</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#        </command>
#        
__glNamedFramebufferTexture_impl=None
def glNamedFramebufferTexture (framebuffer, attachment, texture, level):
    global __glNamedFramebufferTexture_impl
    if not __glNamedFramebufferTexture_impl:
        fptr = __pyglGetFuncAddress('glNamedFramebufferTexture')
        if not fptr:
            raise RuntimeError('The function glNamedFramebufferTexture is not available')
        __glNamedFramebufferTexture_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int)(fptr)
    glNamedFramebufferTexture = __glNamedFramebufferTexture_impl
    return glNamedFramebufferTexture(framebuffer, attachment, texture, level)
# <command>
#            <proto>void <name>glNamedFramebufferTextureLayer</name></proto>
#            <param><ptype>GLuint</ptype> <name>framebuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>attachment</name></param>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>layer</name></param>
#        </command>
#        
__glNamedFramebufferTextureLayer_impl=None
def glNamedFramebufferTextureLayer (framebuffer, attachment, texture, level, layer):
    global __glNamedFramebufferTextureLayer_impl
    if not __glNamedFramebufferTextureLayer_impl:
        fptr = __pyglGetFuncAddress('glNamedFramebufferTextureLayer')
        if not fptr:
            raise RuntimeError('The function glNamedFramebufferTextureLayer is not available')
        __glNamedFramebufferTextureLayer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_int, c_int)(fptr)
    glNamedFramebufferTextureLayer = __glNamedFramebufferTextureLayer_impl
    return glNamedFramebufferTextureLayer(framebuffer, attachment, texture, level, layer)
# <command>
#            <proto>void <name>glNamedRenderbufferStorage</name></proto>
#            <param><ptype>GLuint</ptype> <name>renderbuffer</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#        </command>
#        
__glNamedRenderbufferStorage_impl=None
def glNamedRenderbufferStorage (renderbuffer, internalformat, width, height):
    global __glNamedRenderbufferStorage_impl
    if not __glNamedRenderbufferStorage_impl:
        fptr = __pyglGetFuncAddress('glNamedRenderbufferStorage')
        if not fptr:
            raise RuntimeError('The function glNamedRenderbufferStorage is not available')
        __glNamedRenderbufferStorage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_int)(fptr)
    glNamedRenderbufferStorage = __glNamedRenderbufferStorage_impl
    return glNamedRenderbufferStorage(renderbuffer, internalformat, width, height)
# <command>
#            <proto>void <name>glNamedRenderbufferStorageMultisample</name></proto>
#            <param><ptype>GLuint</ptype> <name>renderbuffer</name></param>
#            <param><ptype>GLsizei</ptype> <name>samples</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#        </command>
#        
__glNamedRenderbufferStorageMultisample_impl=None
def glNamedRenderbufferStorageMultisample (renderbuffer, samples, internalformat, width, height):
    global __glNamedRenderbufferStorageMultisample_impl
    if not __glNamedRenderbufferStorageMultisample_impl:
        fptr = __pyglGetFuncAddress('glNamedRenderbufferStorageMultisample')
        if not fptr:
            raise RuntimeError('The function glNamedRenderbufferStorageMultisample is not available')
        __glNamedRenderbufferStorageMultisample_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int)(fptr)
    glNamedRenderbufferStorageMultisample = __glNamedRenderbufferStorageMultisample_impl
    return glNamedRenderbufferStorageMultisample(renderbuffer, samples, internalformat, width, height)
# <command>
#            <proto>void <name>glObjectLabel</name></proto>
#            <param><ptype>GLenum</ptype> <name>identifier</name></param>
#            <param><ptype>GLuint</ptype> <name>name</name></param>
#            <param><ptype>GLsizei</ptype> <name>length</name></param>
#            <param len="COMPSIZE(label,length)">const <ptype>GLchar</ptype> *<name>label</name></param>
#        </command>
#        
__glObjectLabel_impl=None
def glObjectLabel (identifier, name, length, label):
    global __glObjectLabel_impl
    if not __glObjectLabel_impl:
        fptr = __pyglGetFuncAddress('glObjectLabel')
        if not fptr:
            raise RuntimeError('The function glObjectLabel is not available')
        __glObjectLabel_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p)(fptr)
    glObjectLabel = (lambda identifier,name,length,label:__glObjectLabel_impl(identifier,name,length,c_char_p( label .encode() )))
    return glObjectLabel(identifier, name, length, label)
# <command>
#            <proto>void <name>glObjectPtrLabel</name></proto>
#            <param>const void *<name>ptr</name></param>
#            <param><ptype>GLsizei</ptype> <name>length</name></param>
#            <param len="COMPSIZE(label,length)">const <ptype>GLchar</ptype> *<name>label</name></param>
#        </command>
#        
__glObjectPtrLabel_impl=None
def glObjectPtrLabel (ptr, length, label):
    global __glObjectPtrLabel_impl
    if not __glObjectPtrLabel_impl:
        fptr = __pyglGetFuncAddress('glObjectPtrLabel')
        if not fptr:
            raise RuntimeError('The function glObjectPtrLabel is not available')
        __glObjectPtrLabel_impl = __PYGL_FUNC_TYPE( None ,c_void_p, c_int, c_void_p)(fptr)
    glObjectPtrLabel = (lambda ptr,length,label:__glObjectPtrLabel_impl(__pyglGetAsConstVoidPointer( ptr ),length,c_char_p( label .encode() )))
    return glObjectPtrLabel(ptr, length, label)
# <command>
#            <proto>void <name>glPatchParameterfv</name></proto>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)">const <ptype>GLfloat</ptype> *<name>values</name></param>
#        </command>
#        
__glPatchParameterfv_impl=None
def glPatchParameterfv (pname, values):
    global __glPatchParameterfv_impl
    if not __glPatchParameterfv_impl:
        fptr = __pyglGetFuncAddress('glPatchParameterfv')
        if not fptr:
            raise RuntimeError('The function glPatchParameterfv is not available')
        __glPatchParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glPatchParameterfv = (lambda pname,values:__glPatchParameterfv_impl(pname,__pyglGetAsConstVoidPointer( values )))
    return glPatchParameterfv(pname, values)
# <command>
#            <proto>void <name>glPatchParameteri</name></proto>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> <name>value</name></param>
#        </command>
#        
__glPatchParameteri_impl=None
def glPatchParameteri (pname, value):
    global __glPatchParameteri_impl
    if not __glPatchParameteri_impl:
        fptr = __pyglGetFuncAddress('glPatchParameteri')
        if not fptr:
            raise RuntimeError('The function glPatchParameteri is not available')
        __glPatchParameteri_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int)(fptr)
    glPatchParameteri = __glPatchParameteri_impl
    return glPatchParameteri(pname, value)
# <command>
#            <proto>void <name>glPauseTransformFeedback</name></proto>
#        </command>
#        
__glPauseTransformFeedback_impl=None
def glPauseTransformFeedback ():
    global __glPauseTransformFeedback_impl
    if not __glPauseTransformFeedback_impl:
        fptr = __pyglGetFuncAddress('glPauseTransformFeedback')
        if not fptr:
            raise RuntimeError('The function glPauseTransformFeedback is not available')
        __glPauseTransformFeedback_impl = __PYGL_FUNC_TYPE( None ,)(fptr)
    glPauseTransformFeedback = __glPauseTransformFeedback_impl
    return glPauseTransformFeedback()
# <command>
#            <proto>void <name>glPixelStoref</name></proto>
#            <param group="PixelStoreParameter"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param group="CheckedFloat32"><ptype>GLfloat</ptype> <name>param</name></param>
#            <glx opcode="109" type="single" />
#        </command>
#        
__glPixelStoref_impl=None
def glPixelStoref (pname, param):
    global __glPixelStoref_impl
    if not __glPixelStoref_impl:
        fptr = __pyglGetFuncAddress('glPixelStoref')
        if not fptr:
            raise RuntimeError('The function glPixelStoref is not available')
        __glPixelStoref_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_float)(fptr)
    glPixelStoref = __glPixelStoref_impl
    return glPixelStoref(pname, param)
# <command>
#            <proto>void <name>glPixelStorei</name></proto>
#            <param group="PixelStoreParameter"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>param</name></param>
#            <glx opcode="110" type="single" />
#        </command>
#        
__glPixelStorei_impl=None
def glPixelStorei (pname, param):
    global __glPixelStorei_impl
    if not __glPixelStorei_impl:
        fptr = __pyglGetFuncAddress('glPixelStorei')
        if not fptr:
            raise RuntimeError('The function glPixelStorei is not available')
        __glPixelStorei_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int)(fptr)
    glPixelStorei = __glPixelStorei_impl
    return glPixelStorei(pname, param)
# <command>
#            <proto>void <name>glPointParameterf</name></proto>
#            <param group="PointParameterNameARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param group="CheckedFloat32"><ptype>GLfloat</ptype> <name>param</name></param>
#            <glx opcode="2065" type="render" />
#        </command>
#        
__glPointParameterf_impl=None
def glPointParameterf (pname, param):
    global __glPointParameterf_impl
    if not __glPointParameterf_impl:
        fptr = __pyglGetFuncAddress('glPointParameterf')
        if not fptr:
            raise RuntimeError('The function glPointParameterf is not available')
        __glPointParameterf_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_float)(fptr)
    glPointParameterf = __glPointParameterf_impl
    return glPointParameterf(pname, param)
# <command>
#            <proto>void <name>glPointParameterfv</name></proto>
#            <param group="PointParameterNameARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param group="CheckedFloat32" len="COMPSIZE(pname)">const <ptype>GLfloat</ptype> *<name>params</name></param>
#            <glx opcode="2066" type="render" />
#        </command>
#        
__glPointParameterfv_impl=None
def glPointParameterfv (pname, params):
    global __glPointParameterfv_impl
    if not __glPointParameterfv_impl:
        fptr = __pyglGetFuncAddress('glPointParameterfv')
        if not fptr:
            raise RuntimeError('The function glPointParameterfv is not available')
        __glPointParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glPointParameterfv = (lambda pname,params:__glPointParameterfv_impl(pname,__pyglGetAsConstVoidPointer( params )))
    return glPointParameterfv(pname, params)
# <command>
#            <proto>void <name>glPointParameteri</name></proto>
#            <param group="PointParameterNameARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> <name>param</name></param>
#            <glx opcode="4221" type="render" />
#        </command>
#        
__glPointParameteri_impl=None
def glPointParameteri (pname, param):
    global __glPointParameteri_impl
    if not __glPointParameteri_impl:
        fptr = __pyglGetFuncAddress('glPointParameteri')
        if not fptr:
            raise RuntimeError('The function glPointParameteri is not available')
        __glPointParameteri_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int)(fptr)
    glPointParameteri = __glPointParameteri_impl
    return glPointParameteri(pname, param)
# <command>
#            <proto>void <name>glPointParameteriv</name></proto>
#            <param group="PointParameterNameARB"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)">const <ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="4222" type="render" />
#        </command>
#        
__glPointParameteriv_impl=None
def glPointParameteriv (pname, params):
    global __glPointParameteriv_impl
    if not __glPointParameteriv_impl:
        fptr = __pyglGetFuncAddress('glPointParameteriv')
        if not fptr:
            raise RuntimeError('The function glPointParameteriv is not available')
        __glPointParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glPointParameteriv = (lambda pname,params:__glPointParameteriv_impl(pname,__pyglGetAsConstVoidPointer( params )))
    return glPointParameteriv(pname, params)
# <command>
#            <proto>void <name>glPointSize</name></proto>
#            <param group="CheckedFloat32"><ptype>GLfloat</ptype> <name>size</name></param>
#            <glx opcode="100" type="render" />
#        </command>
#        
__glPointSize_impl=None
def glPointSize (size):
    global __glPointSize_impl
    if not __glPointSize_impl:
        fptr = __pyglGetFuncAddress('glPointSize')
        if not fptr:
            raise RuntimeError('The function glPointSize is not available')
        __glPointSize_impl = __PYGL_FUNC_TYPE( None ,c_float)(fptr)
    glPointSize = __glPointSize_impl
    return glPointSize(size)
# <command>
#            <proto>void <name>glPolygonMode</name></proto>
#            <param group="MaterialFace"><ptype>GLenum</ptype> <name>face</name></param>
#            <param group="PolygonMode"><ptype>GLenum</ptype> <name>mode</name></param>
#            <glx opcode="101" type="render" />
#        </command>
#        
__glPolygonMode_impl=None
def glPolygonMode (face, mode):
    global __glPolygonMode_impl
    if not __glPolygonMode_impl:
        fptr = __pyglGetFuncAddress('glPolygonMode')
        if not fptr:
            raise RuntimeError('The function glPolygonMode is not available')
        __glPolygonMode_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glPolygonMode = __glPolygonMode_impl
    return glPolygonMode(face, mode)
# <command>
#            <proto>void <name>glPolygonOffset</name></proto>
#            <param><ptype>GLfloat</ptype> <name>factor</name></param>
#            <param><ptype>GLfloat</ptype> <name>units</name></param>
#            <glx opcode="192" type="render" />
#        </command>
#        
__glPolygonOffset_impl=None
def glPolygonOffset (factor, units):
    global __glPolygonOffset_impl
    if not __glPolygonOffset_impl:
        fptr = __pyglGetFuncAddress('glPolygonOffset')
        if not fptr:
            raise RuntimeError('The function glPolygonOffset is not available')
        __glPolygonOffset_impl = __PYGL_FUNC_TYPE( None ,c_float, c_float)(fptr)
    glPolygonOffset = __glPolygonOffset_impl
    return glPolygonOffset(factor, units)
# <command>
#            <proto>void <name>glPopDebugGroup</name></proto>
#        </command>
#        
__glPopDebugGroup_impl=None
def glPopDebugGroup ():
    global __glPopDebugGroup_impl
    if not __glPopDebugGroup_impl:
        fptr = __pyglGetFuncAddress('glPopDebugGroup')
        if not fptr:
            raise RuntimeError('The function glPopDebugGroup is not available')
        __glPopDebugGroup_impl = __PYGL_FUNC_TYPE( None ,)(fptr)
    glPopDebugGroup = __glPopDebugGroup_impl
    return glPopDebugGroup()
# <command>
#            <proto>void <name>glPrimitiveRestartIndex</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#        </command>
#        
__glPrimitiveRestartIndex_impl=None
def glPrimitiveRestartIndex (index):
    global __glPrimitiveRestartIndex_impl
    if not __glPrimitiveRestartIndex_impl:
        fptr = __pyglGetFuncAddress('glPrimitiveRestartIndex')
        if not fptr:
            raise RuntimeError('The function glPrimitiveRestartIndex is not available')
        __glPrimitiveRestartIndex_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glPrimitiveRestartIndex = __glPrimitiveRestartIndex_impl
    return glPrimitiveRestartIndex(index)
# <command>
#            <proto>void <name>glProgramBinary</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLenum</ptype> <name>binaryFormat</name></param>
#            <param len="length">const void *<name>binary</name></param>
#            <param><ptype>GLsizei</ptype> <name>length</name></param>
#        </command>
#        
__glProgramBinary_impl=None
def glProgramBinary (program, binaryFormat, binary, length):
    global __glProgramBinary_impl
    if not __glProgramBinary_impl:
        fptr = __pyglGetFuncAddress('glProgramBinary')
        if not fptr:
            raise RuntimeError('The function glProgramBinary is not available')
        __glProgramBinary_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p, c_int)(fptr)
    glProgramBinary = (lambda program,binaryFormat,binary,length:__glProgramBinary_impl(program,binaryFormat,__pyglGetAsConstVoidPointer( binary ),length))
    return glProgramBinary(program, binaryFormat, binary, length)
# <command>
#            <proto>void <name>glProgramParameteri</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param group="ProgramParameterPName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> <name>value</name></param>
#        </command>
#        
__glProgramParameteri_impl=None
def glProgramParameteri (program, pname, value):
    global __glProgramParameteri_impl
    if not __glProgramParameteri_impl:
        fptr = __pyglGetFuncAddress('glProgramParameteri')
        if not fptr:
            raise RuntimeError('The function glProgramParameteri is not available')
        __glProgramParameteri_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int)(fptr)
    glProgramParameteri = __glProgramParameteri_impl
    return glProgramParameteri(program, pname, value)
# <command>
#            <proto>void <name>glProgramUniform1d</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLdouble</ptype> <name>v0</name></param>
#        </command>
#        
__glProgramUniform1d_impl=None
def glProgramUniform1d (program, location, v0):
    global __glProgramUniform1d_impl
    if not __glProgramUniform1d_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform1d')
        if not fptr:
            raise RuntimeError('The function glProgramUniform1d is not available')
        __glProgramUniform1d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_double)(fptr)
    glProgramUniform1d = __glProgramUniform1d_impl
    return glProgramUniform1d(program, location, v0)
# <command>
#            <proto>void <name>glProgramUniform1dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="1">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform1dv_impl=None
def glProgramUniform1dv (program, location, count, value):
    global __glProgramUniform1dv_impl
    if not __glProgramUniform1dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform1dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform1dv is not available')
        __glProgramUniform1dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform1dv = (lambda program,location,count,value:__glProgramUniform1dv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform1dv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform1f</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLfloat</ptype> <name>v0</name></param>
#        </command>
#        
__glProgramUniform1f_impl=None
def glProgramUniform1f (program, location, v0):
    global __glProgramUniform1f_impl
    if not __glProgramUniform1f_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform1f')
        if not fptr:
            raise RuntimeError('The function glProgramUniform1f is not available')
        __glProgramUniform1f_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_float)(fptr)
    glProgramUniform1f = __glProgramUniform1f_impl
    return glProgramUniform1f(program, location, v0)
# <command>
#            <proto>void <name>glProgramUniform1fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="1">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform1fv_impl=None
def glProgramUniform1fv (program, location, count, value):
    global __glProgramUniform1fv_impl
    if not __glProgramUniform1fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform1fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform1fv is not available')
        __glProgramUniform1fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform1fv = (lambda program,location,count,value:__glProgramUniform1fv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform1fv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform1i</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLint</ptype> <name>v0</name></param>
#        </command>
#        
__glProgramUniform1i_impl=None
def glProgramUniform1i (program, location, v0):
    global __glProgramUniform1i_impl
    if not __glProgramUniform1i_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform1i')
        if not fptr:
            raise RuntimeError('The function glProgramUniform1i is not available')
        __glProgramUniform1i_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int)(fptr)
    glProgramUniform1i = __glProgramUniform1i_impl
    return glProgramUniform1i(program, location, v0)
# <command>
#            <proto>void <name>glProgramUniform1iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="1">const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform1iv_impl=None
def glProgramUniform1iv (program, location, count, value):
    global __glProgramUniform1iv_impl
    if not __glProgramUniform1iv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform1iv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform1iv is not available')
        __glProgramUniform1iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform1iv = (lambda program,location,count,value:__glProgramUniform1iv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform1iv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform1ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLuint</ptype> <name>v0</name></param>
#        </command>
#        
__glProgramUniform1ui_impl=None
def glProgramUniform1ui (program, location, v0):
    global __glProgramUniform1ui_impl
    if not __glProgramUniform1ui_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform1ui')
        if not fptr:
            raise RuntimeError('The function glProgramUniform1ui is not available')
        __glProgramUniform1ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint)(fptr)
    glProgramUniform1ui = __glProgramUniform1ui_impl
    return glProgramUniform1ui(program, location, v0)
# <command>
#            <proto>void <name>glProgramUniform1uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="1">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform1uiv_impl=None
def glProgramUniform1uiv (program, location, count, value):
    global __glProgramUniform1uiv_impl
    if not __glProgramUniform1uiv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform1uiv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform1uiv is not available')
        __glProgramUniform1uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform1uiv = (lambda program,location,count,value:__glProgramUniform1uiv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform1uiv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform2d</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLdouble</ptype> <name>v0</name></param>
#            <param><ptype>GLdouble</ptype> <name>v1</name></param>
#        </command>
#        
__glProgramUniform2d_impl=None
def glProgramUniform2d (program, location, v0, v1):
    global __glProgramUniform2d_impl
    if not __glProgramUniform2d_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform2d')
        if not fptr:
            raise RuntimeError('The function glProgramUniform2d is not available')
        __glProgramUniform2d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_double, c_double)(fptr)
    glProgramUniform2d = __glProgramUniform2d_impl
    return glProgramUniform2d(program, location, v0, v1)
# <command>
#            <proto>void <name>glProgramUniform2dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="2">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform2dv_impl=None
def glProgramUniform2dv (program, location, count, value):
    global __glProgramUniform2dv_impl
    if not __glProgramUniform2dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform2dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform2dv is not available')
        __glProgramUniform2dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform2dv = (lambda program,location,count,value:__glProgramUniform2dv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform2dv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform2f</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLfloat</ptype> <name>v0</name></param>
#            <param><ptype>GLfloat</ptype> <name>v1</name></param>
#        </command>
#        
__glProgramUniform2f_impl=None
def glProgramUniform2f (program, location, v0, v1):
    global __glProgramUniform2f_impl
    if not __glProgramUniform2f_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform2f')
        if not fptr:
            raise RuntimeError('The function glProgramUniform2f is not available')
        __glProgramUniform2f_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_float, c_float)(fptr)
    glProgramUniform2f = __glProgramUniform2f_impl
    return glProgramUniform2f(program, location, v0, v1)
# <command>
#            <proto>void <name>glProgramUniform2fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="2">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform2fv_impl=None
def glProgramUniform2fv (program, location, count, value):
    global __glProgramUniform2fv_impl
    if not __glProgramUniform2fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform2fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform2fv is not available')
        __glProgramUniform2fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform2fv = (lambda program,location,count,value:__glProgramUniform2fv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform2fv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform2i</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLint</ptype> <name>v0</name></param>
#            <param><ptype>GLint</ptype> <name>v1</name></param>
#        </command>
#        
__glProgramUniform2i_impl=None
def glProgramUniform2i (program, location, v0, v1):
    global __glProgramUniform2i_impl
    if not __glProgramUniform2i_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform2i')
        if not fptr:
            raise RuntimeError('The function glProgramUniform2i is not available')
        __glProgramUniform2i_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int)(fptr)
    glProgramUniform2i = __glProgramUniform2i_impl
    return glProgramUniform2i(program, location, v0, v1)
# <command>
#            <proto>void <name>glProgramUniform2iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="2">const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform2iv_impl=None
def glProgramUniform2iv (program, location, count, value):
    global __glProgramUniform2iv_impl
    if not __glProgramUniform2iv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform2iv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform2iv is not available')
        __glProgramUniform2iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform2iv = (lambda program,location,count,value:__glProgramUniform2iv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform2iv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform2ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLuint</ptype> <name>v0</name></param>
#            <param><ptype>GLuint</ptype> <name>v1</name></param>
#        </command>
#        
__glProgramUniform2ui_impl=None
def glProgramUniform2ui (program, location, v0, v1):
    global __glProgramUniform2ui_impl
    if not __glProgramUniform2ui_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform2ui')
        if not fptr:
            raise RuntimeError('The function glProgramUniform2ui is not available')
        __glProgramUniform2ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_uint)(fptr)
    glProgramUniform2ui = __glProgramUniform2ui_impl
    return glProgramUniform2ui(program, location, v0, v1)
# <command>
#            <proto>void <name>glProgramUniform2uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="2">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform2uiv_impl=None
def glProgramUniform2uiv (program, location, count, value):
    global __glProgramUniform2uiv_impl
    if not __glProgramUniform2uiv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform2uiv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform2uiv is not available')
        __glProgramUniform2uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform2uiv = (lambda program,location,count,value:__glProgramUniform2uiv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform2uiv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform3d</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLdouble</ptype> <name>v0</name></param>
#            <param><ptype>GLdouble</ptype> <name>v1</name></param>
#            <param><ptype>GLdouble</ptype> <name>v2</name></param>
#        </command>
#        
__glProgramUniform3d_impl=None
def glProgramUniform3d (program, location, v0, v1, v2):
    global __glProgramUniform3d_impl
    if not __glProgramUniform3d_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform3d')
        if not fptr:
            raise RuntimeError('The function glProgramUniform3d is not available')
        __glProgramUniform3d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_double, c_double, c_double)(fptr)
    glProgramUniform3d = __glProgramUniform3d_impl
    return glProgramUniform3d(program, location, v0, v1, v2)
# <command>
#            <proto>void <name>glProgramUniform3dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="3">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform3dv_impl=None
def glProgramUniform3dv (program, location, count, value):
    global __glProgramUniform3dv_impl
    if not __glProgramUniform3dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform3dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform3dv is not available')
        __glProgramUniform3dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform3dv = (lambda program,location,count,value:__glProgramUniform3dv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform3dv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform3f</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLfloat</ptype> <name>v0</name></param>
#            <param><ptype>GLfloat</ptype> <name>v1</name></param>
#            <param><ptype>GLfloat</ptype> <name>v2</name></param>
#        </command>
#        
__glProgramUniform3f_impl=None
def glProgramUniform3f (program, location, v0, v1, v2):
    global __glProgramUniform3f_impl
    if not __glProgramUniform3f_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform3f')
        if not fptr:
            raise RuntimeError('The function glProgramUniform3f is not available')
        __glProgramUniform3f_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_float, c_float, c_float)(fptr)
    glProgramUniform3f = __glProgramUniform3f_impl
    return glProgramUniform3f(program, location, v0, v1, v2)
# <command>
#            <proto>void <name>glProgramUniform3fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="3">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform3fv_impl=None
def glProgramUniform3fv (program, location, count, value):
    global __glProgramUniform3fv_impl
    if not __glProgramUniform3fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform3fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform3fv is not available')
        __glProgramUniform3fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform3fv = (lambda program,location,count,value:__glProgramUniform3fv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform3fv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform3i</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLint</ptype> <name>v0</name></param>
#            <param><ptype>GLint</ptype> <name>v1</name></param>
#            <param><ptype>GLint</ptype> <name>v2</name></param>
#        </command>
#        
__glProgramUniform3i_impl=None
def glProgramUniform3i (program, location, v0, v1, v2):
    global __glProgramUniform3i_impl
    if not __glProgramUniform3i_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform3i')
        if not fptr:
            raise RuntimeError('The function glProgramUniform3i is not available')
        __glProgramUniform3i_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int)(fptr)
    glProgramUniform3i = __glProgramUniform3i_impl
    return glProgramUniform3i(program, location, v0, v1, v2)
# <command>
#            <proto>void <name>glProgramUniform3iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="3">const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform3iv_impl=None
def glProgramUniform3iv (program, location, count, value):
    global __glProgramUniform3iv_impl
    if not __glProgramUniform3iv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform3iv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform3iv is not available')
        __glProgramUniform3iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform3iv = (lambda program,location,count,value:__glProgramUniform3iv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform3iv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform3ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLuint</ptype> <name>v0</name></param>
#            <param><ptype>GLuint</ptype> <name>v1</name></param>
#            <param><ptype>GLuint</ptype> <name>v2</name></param>
#        </command>
#        
__glProgramUniform3ui_impl=None
def glProgramUniform3ui (program, location, v0, v1, v2):
    global __glProgramUniform3ui_impl
    if not __glProgramUniform3ui_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform3ui')
        if not fptr:
            raise RuntimeError('The function glProgramUniform3ui is not available')
        __glProgramUniform3ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_uint, c_uint)(fptr)
    glProgramUniform3ui = __glProgramUniform3ui_impl
    return glProgramUniform3ui(program, location, v0, v1, v2)
# <command>
#            <proto>void <name>glProgramUniform3uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="3">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform3uiv_impl=None
def glProgramUniform3uiv (program, location, count, value):
    global __glProgramUniform3uiv_impl
    if not __glProgramUniform3uiv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform3uiv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform3uiv is not available')
        __glProgramUniform3uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform3uiv = (lambda program,location,count,value:__glProgramUniform3uiv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform3uiv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform4d</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLdouble</ptype> <name>v0</name></param>
#            <param><ptype>GLdouble</ptype> <name>v1</name></param>
#            <param><ptype>GLdouble</ptype> <name>v2</name></param>
#            <param><ptype>GLdouble</ptype> <name>v3</name></param>
#        </command>
#        
__glProgramUniform4d_impl=None
def glProgramUniform4d (program, location, v0, v1, v2, v3):
    global __glProgramUniform4d_impl
    if not __glProgramUniform4d_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform4d')
        if not fptr:
            raise RuntimeError('The function glProgramUniform4d is not available')
        __glProgramUniform4d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_double, c_double, c_double, c_double)(fptr)
    glProgramUniform4d = __glProgramUniform4d_impl
    return glProgramUniform4d(program, location, v0, v1, v2, v3)
# <command>
#            <proto>void <name>glProgramUniform4dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="4">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform4dv_impl=None
def glProgramUniform4dv (program, location, count, value):
    global __glProgramUniform4dv_impl
    if not __glProgramUniform4dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform4dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform4dv is not available')
        __glProgramUniform4dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform4dv = (lambda program,location,count,value:__glProgramUniform4dv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform4dv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform4f</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLfloat</ptype> <name>v0</name></param>
#            <param><ptype>GLfloat</ptype> <name>v1</name></param>
#            <param><ptype>GLfloat</ptype> <name>v2</name></param>
#            <param><ptype>GLfloat</ptype> <name>v3</name></param>
#        </command>
#        
__glProgramUniform4f_impl=None
def glProgramUniform4f (program, location, v0, v1, v2, v3):
    global __glProgramUniform4f_impl
    if not __glProgramUniform4f_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform4f')
        if not fptr:
            raise RuntimeError('The function glProgramUniform4f is not available')
        __glProgramUniform4f_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_float, c_float, c_float, c_float)(fptr)
    glProgramUniform4f = __glProgramUniform4f_impl
    return glProgramUniform4f(program, location, v0, v1, v2, v3)
# <command>
#            <proto>void <name>glProgramUniform4fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="4">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform4fv_impl=None
def glProgramUniform4fv (program, location, count, value):
    global __glProgramUniform4fv_impl
    if not __glProgramUniform4fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform4fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform4fv is not available')
        __glProgramUniform4fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform4fv = (lambda program,location,count,value:__glProgramUniform4fv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform4fv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform4i</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLint</ptype> <name>v0</name></param>
#            <param><ptype>GLint</ptype> <name>v1</name></param>
#            <param><ptype>GLint</ptype> <name>v2</name></param>
#            <param><ptype>GLint</ptype> <name>v3</name></param>
#        </command>
#        
__glProgramUniform4i_impl=None
def glProgramUniform4i (program, location, v0, v1, v2, v3):
    global __glProgramUniform4i_impl
    if not __glProgramUniform4i_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform4i')
        if not fptr:
            raise RuntimeError('The function glProgramUniform4i is not available')
        __glProgramUniform4i_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int)(fptr)
    glProgramUniform4i = __glProgramUniform4i_impl
    return glProgramUniform4i(program, location, v0, v1, v2, v3)
# <command>
#            <proto>void <name>glProgramUniform4iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="4">const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform4iv_impl=None
def glProgramUniform4iv (program, location, count, value):
    global __glProgramUniform4iv_impl
    if not __glProgramUniform4iv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform4iv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform4iv is not available')
        __glProgramUniform4iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform4iv = (lambda program,location,count,value:__glProgramUniform4iv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform4iv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniform4ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLuint</ptype> <name>v0</name></param>
#            <param><ptype>GLuint</ptype> <name>v1</name></param>
#            <param><ptype>GLuint</ptype> <name>v2</name></param>
#            <param><ptype>GLuint</ptype> <name>v3</name></param>
#        </command>
#        
__glProgramUniform4ui_impl=None
def glProgramUniform4ui (program, location, v0, v1, v2, v3):
    global __glProgramUniform4ui_impl
    if not __glProgramUniform4ui_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform4ui')
        if not fptr:
            raise RuntimeError('The function glProgramUniform4ui is not available')
        __glProgramUniform4ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_uint, c_uint, c_uint)(fptr)
    glProgramUniform4ui = __glProgramUniform4ui_impl
    return glProgramUniform4ui(program, location, v0, v1, v2, v3)
# <command>
#            <proto>void <name>glProgramUniform4uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="4">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniform4uiv_impl=None
def glProgramUniform4uiv (program, location, count, value):
    global __glProgramUniform4uiv_impl
    if not __glProgramUniform4uiv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniform4uiv')
        if not fptr:
            raise RuntimeError('The function glProgramUniform4uiv is not available')
        __glProgramUniform4uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_void_p)(fptr)
    glProgramUniform4uiv = (lambda program,location,count,value:__glProgramUniform4uiv_impl(program,location,count,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniform4uiv(program, location, count, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix2dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="2">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix2dv_impl=None
def glProgramUniformMatrix2dv (program, location, count, transpose, value):
    global __glProgramUniformMatrix2dv_impl
    if not __glProgramUniformMatrix2dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix2dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix2dv is not available')
        __glProgramUniformMatrix2dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix2dv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix2dv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix2dv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix2fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="2">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix2fv_impl=None
def glProgramUniformMatrix2fv (program, location, count, transpose, value):
    global __glProgramUniformMatrix2fv_impl
    if not __glProgramUniformMatrix2fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix2fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix2fv is not available')
        __glProgramUniformMatrix2fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix2fv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix2fv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix2fv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix2x3dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix2x3dv_impl=None
def glProgramUniformMatrix2x3dv (program, location, count, transpose, value):
    global __glProgramUniformMatrix2x3dv_impl
    if not __glProgramUniformMatrix2x3dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix2x3dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix2x3dv is not available')
        __glProgramUniformMatrix2x3dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix2x3dv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix2x3dv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix2x3dv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix2x3fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix2x3fv_impl=None
def glProgramUniformMatrix2x3fv (program, location, count, transpose, value):
    global __glProgramUniformMatrix2x3fv_impl
    if not __glProgramUniformMatrix2x3fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix2x3fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix2x3fv is not available')
        __glProgramUniformMatrix2x3fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix2x3fv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix2x3fv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix2x3fv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix2x4dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix2x4dv_impl=None
def glProgramUniformMatrix2x4dv (program, location, count, transpose, value):
    global __glProgramUniformMatrix2x4dv_impl
    if not __glProgramUniformMatrix2x4dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix2x4dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix2x4dv is not available')
        __glProgramUniformMatrix2x4dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix2x4dv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix2x4dv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix2x4dv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix2x4fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix2x4fv_impl=None
def glProgramUniformMatrix2x4fv (program, location, count, transpose, value):
    global __glProgramUniformMatrix2x4fv_impl
    if not __glProgramUniformMatrix2x4fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix2x4fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix2x4fv is not available')
        __glProgramUniformMatrix2x4fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix2x4fv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix2x4fv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix2x4fv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix3dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="3">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix3dv_impl=None
def glProgramUniformMatrix3dv (program, location, count, transpose, value):
    global __glProgramUniformMatrix3dv_impl
    if not __glProgramUniformMatrix3dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix3dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix3dv is not available')
        __glProgramUniformMatrix3dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix3dv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix3dv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix3dv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix3fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="3">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix3fv_impl=None
def glProgramUniformMatrix3fv (program, location, count, transpose, value):
    global __glProgramUniformMatrix3fv_impl
    if not __glProgramUniformMatrix3fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix3fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix3fv is not available')
        __glProgramUniformMatrix3fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix3fv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix3fv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix3fv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix3x2dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix3x2dv_impl=None
def glProgramUniformMatrix3x2dv (program, location, count, transpose, value):
    global __glProgramUniformMatrix3x2dv_impl
    if not __glProgramUniformMatrix3x2dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix3x2dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix3x2dv is not available')
        __glProgramUniformMatrix3x2dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix3x2dv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix3x2dv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix3x2dv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix3x2fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix3x2fv_impl=None
def glProgramUniformMatrix3x2fv (program, location, count, transpose, value):
    global __glProgramUniformMatrix3x2fv_impl
    if not __glProgramUniformMatrix3x2fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix3x2fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix3x2fv is not available')
        __glProgramUniformMatrix3x2fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix3x2fv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix3x2fv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix3x2fv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix3x4dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix3x4dv_impl=None
def glProgramUniformMatrix3x4dv (program, location, count, transpose, value):
    global __glProgramUniformMatrix3x4dv_impl
    if not __glProgramUniformMatrix3x4dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix3x4dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix3x4dv is not available')
        __glProgramUniformMatrix3x4dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix3x4dv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix3x4dv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix3x4dv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix3x4fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix3x4fv_impl=None
def glProgramUniformMatrix3x4fv (program, location, count, transpose, value):
    global __glProgramUniformMatrix3x4fv_impl
    if not __glProgramUniformMatrix3x4fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix3x4fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix3x4fv is not available')
        __glProgramUniformMatrix3x4fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix3x4fv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix3x4fv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix3x4fv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix4dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="4">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix4dv_impl=None
def glProgramUniformMatrix4dv (program, location, count, transpose, value):
    global __glProgramUniformMatrix4dv_impl
    if not __glProgramUniformMatrix4dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix4dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix4dv is not available')
        __glProgramUniformMatrix4dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix4dv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix4dv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix4dv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix4fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="4">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix4fv_impl=None
def glProgramUniformMatrix4fv (program, location, count, transpose, value):
    global __glProgramUniformMatrix4fv_impl
    if not __glProgramUniformMatrix4fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix4fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix4fv is not available')
        __glProgramUniformMatrix4fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix4fv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix4fv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix4fv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix4x2dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix4x2dv_impl=None
def glProgramUniformMatrix4x2dv (program, location, count, transpose, value):
    global __glProgramUniformMatrix4x2dv_impl
    if not __glProgramUniformMatrix4x2dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix4x2dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix4x2dv is not available')
        __glProgramUniformMatrix4x2dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix4x2dv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix4x2dv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix4x2dv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix4x2fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix4x2fv_impl=None
def glProgramUniformMatrix4x2fv (program, location, count, transpose, value):
    global __glProgramUniformMatrix4x2fv_impl
    if not __glProgramUniformMatrix4x2fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix4x2fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix4x2fv is not available')
        __glProgramUniformMatrix4x2fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix4x2fv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix4x2fv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix4x2fv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix4x3dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix4x3dv_impl=None
def glProgramUniformMatrix4x3dv (program, location, count, transpose, value):
    global __glProgramUniformMatrix4x3dv_impl
    if not __glProgramUniformMatrix4x3dv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix4x3dv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix4x3dv is not available')
        __glProgramUniformMatrix4x3dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix4x3dv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix4x3dv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix4x3dv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProgramUniformMatrix4x3fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glProgramUniformMatrix4x3fv_impl=None
def glProgramUniformMatrix4x3fv (program, location, count, transpose, value):
    global __glProgramUniformMatrix4x3fv_impl
    if not __glProgramUniformMatrix4x3fv_impl:
        fptr = __pyglGetFuncAddress('glProgramUniformMatrix4x3fv')
        if not fptr:
            raise RuntimeError('The function glProgramUniformMatrix4x3fv is not available')
        __glProgramUniformMatrix4x3fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_char, c_void_p)(fptr)
    glProgramUniformMatrix4x3fv = (lambda program,location,count,transpose,value:__glProgramUniformMatrix4x3fv_impl(program,location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glProgramUniformMatrix4x3fv(program, location, count, transpose, value)
# <command>
#            <proto>void <name>glProvokingVertex</name></proto>
#            <param><ptype>GLenum</ptype> <name>mode</name></param>
#        </command>
#        
__glProvokingVertex_impl=None
def glProvokingVertex (mode):
    global __glProvokingVertex_impl
    if not __glProvokingVertex_impl:
        fptr = __pyglGetFuncAddress('glProvokingVertex')
        if not fptr:
            raise RuntimeError('The function glProvokingVertex is not available')
        __glProvokingVertex_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glProvokingVertex = __glProvokingVertex_impl
    return glProvokingVertex(mode)
# <command>
#            <proto>void <name>glPushDebugGroup</name></proto>
#            <param><ptype>GLenum</ptype> <name>source</name></param>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLsizei</ptype> <name>length</name></param>
#            <param len="COMPSIZE(message,length)">const <ptype>GLchar</ptype> *<name>message</name></param>
#        </command>
#        
__glPushDebugGroup_impl=None
def glPushDebugGroup (source, id, length, message):
    global __glPushDebugGroup_impl
    if not __glPushDebugGroup_impl:
        fptr = __pyglGetFuncAddress('glPushDebugGroup')
        if not fptr:
            raise RuntimeError('The function glPushDebugGroup is not available')
        __glPushDebugGroup_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p)(fptr)
    glPushDebugGroup = (lambda source,id,length,message:__glPushDebugGroup_impl(source,id,length,c_char_p( message .encode() )))
    return glPushDebugGroup(source, id, length, message)
# <command>
#            <proto>void <name>glQueryCounter</name></proto>
#            <param><ptype>GLuint</ptype> <name>id</name></param>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#        </command>
#        
__glQueryCounter_impl=None
def glQueryCounter (id, target):
    global __glQueryCounter_impl
    if not __glQueryCounter_impl:
        fptr = __pyglGetFuncAddress('glQueryCounter')
        if not fptr:
            raise RuntimeError('The function glQueryCounter is not available')
        __glQueryCounter_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glQueryCounter = __glQueryCounter_impl
    return glQueryCounter(id, target)
# <command>
#            <proto>void <name>glReadBuffer</name></proto>
#            <param group="ReadBufferMode"><ptype>GLenum</ptype> <name>src</name></param>
#            <glx opcode="171" type="render" />
#        </command>
#        
__glReadBuffer_impl=None
def glReadBuffer (src):
    global __glReadBuffer_impl
    if not __glReadBuffer_impl:
        fptr = __pyglGetFuncAddress('glReadBuffer')
        if not fptr:
            raise RuntimeError('The function glReadBuffer is not available')
        __glReadBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glReadBuffer = __glReadBuffer_impl
    return glReadBuffer(src)
# <command>
#            <proto>void <name>glReadPixels</name></proto>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>x</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param group="PixelType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type,width,height)">void *<name>pixels</name></param>
#            <glx opcode="111" type="single" />
#            <glx comment="PBO protocol" name="glReadPixelsPBO" opcode="345" type="render" />
#        </command>
#        
__glReadPixels_impl=None
def glReadPixels (x, y, width, height, format, type, pixels):
    global __glReadPixels_impl
    if not __glReadPixels_impl:
        fptr = __pyglGetFuncAddress('glReadPixels')
        if not fptr:
            raise RuntimeError('The function glReadPixels is not available')
        __glReadPixels_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glReadPixels = (lambda x,y,width,height,format,type,pixels:__glReadPixels_impl(x,y,width,height,format,type,(c_uint8*len( pixels )).from_buffer( pixels )))
    return glReadPixels(x, y, width, height, format, type, pixels)
# <command>
#            <proto>void <name>glReadnPixels</name></proto>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <param><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param><ptype>GLsizei</ptype> <name>bufSize</name></param>
#            <param>void *<name>data</name></param>
#        </command>
#        
__glReadnPixels_impl=None
def glReadnPixels (x, y, width, height, format, type, bufSize, data):
    global __glReadnPixels_impl
    if not __glReadnPixels_impl:
        fptr = __pyglGetFuncAddress('glReadnPixels')
        if not fptr:
            raise RuntimeError('The function glReadnPixels is not available')
        __glReadnPixels_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_int, c_int, c_uint, c_uint, c_int, c_void_p)(fptr)
    glReadnPixels = (lambda x,y,width,height,format,type,bufSize,data:__glReadnPixels_impl(x,y,width,height,format,type,bufSize,(c_uint8*len( data )).from_buffer( data )))
    return glReadnPixels(x, y, width, height, format, type, bufSize, data)
# <command>
#            <proto>void <name>glReleaseShaderCompiler</name></proto>
#        </command>
#        
__glReleaseShaderCompiler_impl=None
def glReleaseShaderCompiler ():
    global __glReleaseShaderCompiler_impl
    if not __glReleaseShaderCompiler_impl:
        fptr = __pyglGetFuncAddress('glReleaseShaderCompiler')
        if not fptr:
            raise RuntimeError('The function glReleaseShaderCompiler is not available')
        __glReleaseShaderCompiler_impl = __PYGL_FUNC_TYPE( None ,)(fptr)
    glReleaseShaderCompiler = __glReleaseShaderCompiler_impl
    return glReleaseShaderCompiler()
# <command>
#            <proto>void <name>glRenderbufferStorage</name></proto>
#            <param group="RenderbufferTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <glx opcode="4318" type="render" />
#        </command>
#        
__glRenderbufferStorage_impl=None
def glRenderbufferStorage (target, internalformat, width, height):
    global __glRenderbufferStorage_impl
    if not __glRenderbufferStorage_impl:
        fptr = __pyglGetFuncAddress('glRenderbufferStorage')
        if not fptr:
            raise RuntimeError('The function glRenderbufferStorage is not available')
        __glRenderbufferStorage_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_int)(fptr)
    glRenderbufferStorage = __glRenderbufferStorage_impl
    return glRenderbufferStorage(target, internalformat, width, height)
# <command>
#            <proto>void <name>glRenderbufferStorageMultisample</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLsizei</ptype> <name>samples</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <glx opcode="4331" type="render" />
#        </command>
#        
__glRenderbufferStorageMultisample_impl=None
def glRenderbufferStorageMultisample (target, samples, internalformat, width, height):
    global __glRenderbufferStorageMultisample_impl
    if not __glRenderbufferStorageMultisample_impl:
        fptr = __pyglGetFuncAddress('glRenderbufferStorageMultisample')
        if not fptr:
            raise RuntimeError('The function glRenderbufferStorageMultisample is not available')
        __glRenderbufferStorageMultisample_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int)(fptr)
    glRenderbufferStorageMultisample = __glRenderbufferStorageMultisample_impl
    return glRenderbufferStorageMultisample(target, samples, internalformat, width, height)
# <command>
#            <proto>void <name>glResumeTransformFeedback</name></proto>
#        </command>
#        
__glResumeTransformFeedback_impl=None
def glResumeTransformFeedback ():
    global __glResumeTransformFeedback_impl
    if not __glResumeTransformFeedback_impl:
        fptr = __pyglGetFuncAddress('glResumeTransformFeedback')
        if not fptr:
            raise RuntimeError('The function glResumeTransformFeedback is not available')
        __glResumeTransformFeedback_impl = __PYGL_FUNC_TYPE( None ,)(fptr)
    glResumeTransformFeedback = __glResumeTransformFeedback_impl
    return glResumeTransformFeedback()
# <command>
#            <proto>void <name>glSampleCoverage</name></proto>
#            <param><ptype>GLfloat</ptype> <name>value</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>invert</name></param>
#            <glx opcode="229" type="render" />
#        </command>
#        
__glSampleCoverage_impl=None
def glSampleCoverage (value, invert):
    global __glSampleCoverage_impl
    if not __glSampleCoverage_impl:
        fptr = __pyglGetFuncAddress('glSampleCoverage')
        if not fptr:
            raise RuntimeError('The function glSampleCoverage is not available')
        __glSampleCoverage_impl = __PYGL_FUNC_TYPE( None ,c_float, c_char)(fptr)
    glSampleCoverage = __glSampleCoverage_impl
    return glSampleCoverage(value, invert)
# <command>
#            <proto>void <name>glSampleMaski</name></proto>
#            <param><ptype>GLuint</ptype> <name>maskNumber</name></param>
#            <param><ptype>GLbitfield</ptype> <name>mask</name></param>
#        </command>
#        
__glSampleMaski_impl=None
def glSampleMaski (maskNumber, mask):
    global __glSampleMaski_impl
    if not __glSampleMaski_impl:
        fptr = __pyglGetFuncAddress('glSampleMaski')
        if not fptr:
            raise RuntimeError('The function glSampleMaski is not available')
        __glSampleMaski_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glSampleMaski = __glSampleMaski_impl
    return glSampleMaski(maskNumber, mask)
# <command>
#            <proto>void <name>glSamplerParameterIiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)">const <ptype>GLint</ptype> *<name>param</name></param>
#        </command>
#        
__glSamplerParameterIiv_impl=None
def glSamplerParameterIiv (sampler, pname, param):
    global __glSamplerParameterIiv_impl
    if not __glSamplerParameterIiv_impl:
        fptr = __pyglGetFuncAddress('glSamplerParameterIiv')
        if not fptr:
            raise RuntimeError('The function glSamplerParameterIiv is not available')
        __glSamplerParameterIiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glSamplerParameterIiv = (lambda sampler,pname,param:__glSamplerParameterIiv_impl(sampler,pname,__pyglGetAsConstVoidPointer( param )))
    return glSamplerParameterIiv(sampler, pname, param)
# <command>
#            <proto>void <name>glSamplerParameterIuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)">const <ptype>GLuint</ptype> *<name>param</name></param>
#        </command>
#        
__glSamplerParameterIuiv_impl=None
def glSamplerParameterIuiv (sampler, pname, param):
    global __glSamplerParameterIuiv_impl
    if not __glSamplerParameterIuiv_impl:
        fptr = __pyglGetFuncAddress('glSamplerParameterIuiv')
        if not fptr:
            raise RuntimeError('The function glSamplerParameterIuiv is not available')
        __glSamplerParameterIuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glSamplerParameterIuiv = (lambda sampler,pname,param:__glSamplerParameterIuiv_impl(sampler,pname,__pyglGetAsConstVoidPointer( param )))
    return glSamplerParameterIuiv(sampler, pname, param)
# <command>
#            <proto>void <name>glSamplerParameterf</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLfloat</ptype> <name>param</name></param>
#        </command>
#        
__glSamplerParameterf_impl=None
def glSamplerParameterf (sampler, pname, param):
    global __glSamplerParameterf_impl
    if not __glSamplerParameterf_impl:
        fptr = __pyglGetFuncAddress('glSamplerParameterf')
        if not fptr:
            raise RuntimeError('The function glSamplerParameterf is not available')
        __glSamplerParameterf_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_float)(fptr)
    glSamplerParameterf = __glSamplerParameterf_impl
    return glSamplerParameterf(sampler, pname, param)
# <command>
#            <proto>void <name>glSamplerParameterfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)">const <ptype>GLfloat</ptype> *<name>param</name></param>
#        </command>
#        
__glSamplerParameterfv_impl=None
def glSamplerParameterfv (sampler, pname, param):
    global __glSamplerParameterfv_impl
    if not __glSamplerParameterfv_impl:
        fptr = __pyglGetFuncAddress('glSamplerParameterfv')
        if not fptr:
            raise RuntimeError('The function glSamplerParameterfv is not available')
        __glSamplerParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glSamplerParameterfv = (lambda sampler,pname,param:__glSamplerParameterfv_impl(sampler,pname,__pyglGetAsConstVoidPointer( param )))
    return glSamplerParameterfv(sampler, pname, param)
# <command>
#            <proto>void <name>glSamplerParameteri</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> <name>param</name></param>
#        </command>
#        
__glSamplerParameteri_impl=None
def glSamplerParameteri (sampler, pname, param):
    global __glSamplerParameteri_impl
    if not __glSamplerParameteri_impl:
        fptr = __pyglGetFuncAddress('glSamplerParameteri')
        if not fptr:
            raise RuntimeError('The function glSamplerParameteri is not available')
        __glSamplerParameteri_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int)(fptr)
    glSamplerParameteri = __glSamplerParameteri_impl
    return glSamplerParameteri(sampler, pname, param)
# <command>
#            <proto>void <name>glSamplerParameteriv</name></proto>
#            <param><ptype>GLuint</ptype> <name>sampler</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)">const <ptype>GLint</ptype> *<name>param</name></param>
#        </command>
#        
__glSamplerParameteriv_impl=None
def glSamplerParameteriv (sampler, pname, param):
    global __glSamplerParameteriv_impl
    if not __glSamplerParameteriv_impl:
        fptr = __pyglGetFuncAddress('glSamplerParameteriv')
        if not fptr:
            raise RuntimeError('The function glSamplerParameteriv is not available')
        __glSamplerParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glSamplerParameteriv = (lambda sampler,pname,param:__glSamplerParameteriv_impl(sampler,pname,__pyglGetAsConstVoidPointer( param )))
    return glSamplerParameteriv(sampler, pname, param)
# <command>
#            <proto>void <name>glScissor</name></proto>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>x</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <glx opcode="103" type="render" />
#        </command>
#        
__glScissor_impl=None
def glScissor (x, y, width, height):
    global __glScissor_impl
    if not __glScissor_impl:
        fptr = __pyglGetFuncAddress('glScissor')
        if not fptr:
            raise RuntimeError('The function glScissor is not available')
        __glScissor_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_int, c_int)(fptr)
    glScissor = __glScissor_impl
    return glScissor(x, y, width, height)
# <command>
#            <proto>void <name>glScissorArrayv</name></proto>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="COMPSIZE(count)">const <ptype>GLint</ptype> *<name>v</name></param>
#        </command>
#        
__glScissorArrayv_impl=None
def glScissorArrayv (first, count, v):
    global __glScissorArrayv_impl
    if not __glScissorArrayv_impl:
        fptr = __pyglGetFuncAddress('glScissorArrayv')
        if not fptr:
            raise RuntimeError('The function glScissorArrayv is not available')
        __glScissorArrayv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glScissorArrayv = (lambda first,count,v:__glScissorArrayv_impl(first,count,__pyglGetAsConstVoidPointer( v )))
    return glScissorArrayv(first, count, v)
# <command>
#            <proto>void <name>glScissorIndexed</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLint</ptype> <name>left</name></param>
#            <param><ptype>GLint</ptype> <name>bottom</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#        </command>
#        
__glScissorIndexed_impl=None
def glScissorIndexed (index, left, bottom, width, height):
    global __glScissorIndexed_impl
    if not __glScissorIndexed_impl:
        fptr = __pyglGetFuncAddress('glScissorIndexed')
        if not fptr:
            raise RuntimeError('The function glScissorIndexed is not available')
        __glScissorIndexed_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int)(fptr)
    glScissorIndexed = __glScissorIndexed_impl
    return glScissorIndexed(index, left, bottom, width, height)
# <command>
#            <proto>void <name>glScissorIndexedv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLint</ptype> *<name>v</name></param>
#        </command>
#        
__glScissorIndexedv_impl=None
def glScissorIndexedv (index, v):
    global __glScissorIndexedv_impl
    if not __glScissorIndexedv_impl:
        fptr = __pyglGetFuncAddress('glScissorIndexedv')
        if not fptr:
            raise RuntimeError('The function glScissorIndexedv is not available')
        __glScissorIndexedv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glScissorIndexedv = (lambda index,v:__glScissorIndexedv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glScissorIndexedv(index, v)
# <command>
#            <proto>void <name>glShaderBinary</name></proto>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>shaders</name></param>
#            <param><ptype>GLenum</ptype> <name>binaryformat</name></param>
#            <param len="length">const void *<name>binary</name></param>
#            <param><ptype>GLsizei</ptype> <name>length</name></param>
#        </command>
#        
__glShaderBinary_impl=None
def glShaderBinary (count, shaders, binaryformat, binary, length):
    global __glShaderBinary_impl
    if not __glShaderBinary_impl:
        fptr = __pyglGetFuncAddress('glShaderBinary')
        if not fptr:
            raise RuntimeError('The function glShaderBinary is not available')
        __glShaderBinary_impl = __PYGL_FUNC_TYPE( None ,c_int, c_void_p, c_uint, c_void_p, c_int)(fptr)
    glShaderBinary = (lambda count,shaders,binaryformat,binary,length:__glShaderBinary_impl(count,__pyglGetAsConstVoidPointer( shaders ),binaryformat,__pyglGetAsConstVoidPointer( binary ),length))
    return glShaderBinary(count, shaders, binaryformat, binary, length)
# <command>
#            <proto>void <name>glShaderStorageBlockBinding</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>storageBlockIndex</name></param>
#            <param><ptype>GLuint</ptype> <name>storageBlockBinding</name></param>
#        </command>
#        
__glShaderStorageBlockBinding_impl=None
def glShaderStorageBlockBinding (program, storageBlockIndex, storageBlockBinding):
    global __glShaderStorageBlockBinding_impl
    if not __glShaderStorageBlockBinding_impl:
        fptr = __pyglGetFuncAddress('glShaderStorageBlockBinding')
        if not fptr:
            raise RuntimeError('The function glShaderStorageBlockBinding is not available')
        __glShaderStorageBlockBinding_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glShaderStorageBlockBinding = __glShaderStorageBlockBinding_impl
    return glShaderStorageBlockBinding(program, storageBlockIndex, storageBlockBinding)
# <command>
#            <proto>void <name>glStencilFunc</name></proto>
#            <param group="StencilFunction"><ptype>GLenum</ptype> <name>func</name></param>
#            <param group="StencilValue"><ptype>GLint</ptype> <name>ref</name></param>
#            <param group="MaskedStencilValue"><ptype>GLuint</ptype> <name>mask</name></param>
#            <glx opcode="162" type="render" />
#        </command>
#        
__glStencilFunc_impl=None
def glStencilFunc (func, ref, mask):
    global __glStencilFunc_impl
    if not __glStencilFunc_impl:
        fptr = __pyglGetFuncAddress('glStencilFunc')
        if not fptr:
            raise RuntimeError('The function glStencilFunc is not available')
        __glStencilFunc_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint)(fptr)
    glStencilFunc = __glStencilFunc_impl
    return glStencilFunc(func, ref, mask)
# <command>
#            <proto>void <name>glStencilFuncSeparate</name></proto>
#            <param group="StencilFaceDirection"><ptype>GLenum</ptype> <name>face</name></param>
#            <param group="StencilFunction"><ptype>GLenum</ptype> <name>func</name></param>
#            <param group="StencilValue"><ptype>GLint</ptype> <name>ref</name></param>
#            <param group="MaskedStencilValue"><ptype>GLuint</ptype> <name>mask</name></param>
#        </command>
#        
__glStencilFuncSeparate_impl=None
def glStencilFuncSeparate (face, func, ref, mask):
    global __glStencilFuncSeparate_impl
    if not __glStencilFuncSeparate_impl:
        fptr = __pyglGetFuncAddress('glStencilFuncSeparate')
        if not fptr:
            raise RuntimeError('The function glStencilFuncSeparate is not available')
        __glStencilFuncSeparate_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_uint)(fptr)
    glStencilFuncSeparate = __glStencilFuncSeparate_impl
    return glStencilFuncSeparate(face, func, ref, mask)
# <command>
#            <proto>void <name>glStencilMask</name></proto>
#            <param group="MaskedStencilValue"><ptype>GLuint</ptype> <name>mask</name></param>
#            <glx opcode="133" type="render" />
#        </command>
#        
__glStencilMask_impl=None
def glStencilMask (mask):
    global __glStencilMask_impl
    if not __glStencilMask_impl:
        fptr = __pyglGetFuncAddress('glStencilMask')
        if not fptr:
            raise RuntimeError('The function glStencilMask is not available')
        __glStencilMask_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glStencilMask = __glStencilMask_impl
    return glStencilMask(mask)
# <command>
#            <proto>void <name>glStencilMaskSeparate</name></proto>
#            <param group="StencilFaceDirection"><ptype>GLenum</ptype> <name>face</name></param>
#            <param group="MaskedStencilValue"><ptype>GLuint</ptype> <name>mask</name></param>
#        </command>
#        
__glStencilMaskSeparate_impl=None
def glStencilMaskSeparate (face, mask):
    global __glStencilMaskSeparate_impl
    if not __glStencilMaskSeparate_impl:
        fptr = __pyglGetFuncAddress('glStencilMaskSeparate')
        if not fptr:
            raise RuntimeError('The function glStencilMaskSeparate is not available')
        __glStencilMaskSeparate_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glStencilMaskSeparate = __glStencilMaskSeparate_impl
    return glStencilMaskSeparate(face, mask)
# <command>
#            <proto>void <name>glStencilOp</name></proto>
#            <param group="StencilOp"><ptype>GLenum</ptype> <name>fail</name></param>
#            <param group="StencilOp"><ptype>GLenum</ptype> <name>zfail</name></param>
#            <param group="StencilOp"><ptype>GLenum</ptype> <name>zpass</name></param>
#            <glx opcode="163" type="render" />
#        </command>
#        
__glStencilOp_impl=None
def glStencilOp (fail, zfail, zpass):
    global __glStencilOp_impl
    if not __glStencilOp_impl:
        fptr = __pyglGetFuncAddress('glStencilOp')
        if not fptr:
            raise RuntimeError('The function glStencilOp is not available')
        __glStencilOp_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glStencilOp = __glStencilOp_impl
    return glStencilOp(fail, zfail, zpass)
# <command>
#            <proto>void <name>glStencilOpSeparate</name></proto>
#            <param group="StencilFaceDirection"><ptype>GLenum</ptype> <name>face</name></param>
#            <param group="StencilOp"><ptype>GLenum</ptype> <name>sfail</name></param>
#            <param group="StencilOp"><ptype>GLenum</ptype> <name>dpfail</name></param>
#            <param group="StencilOp"><ptype>GLenum</ptype> <name>dppass</name></param>
#        </command>
#        
__glStencilOpSeparate_impl=None
def glStencilOpSeparate (face, sfail, dpfail, dppass):
    global __glStencilOpSeparate_impl
    if not __glStencilOpSeparate_impl:
        fptr = __pyglGetFuncAddress('glStencilOpSeparate')
        if not fptr:
            raise RuntimeError('The function glStencilOpSeparate is not available')
        __glStencilOpSeparate_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint)(fptr)
    glStencilOpSeparate = __glStencilOpSeparate_impl
    return glStencilOpSeparate(face, sfail, dpfail, dppass)
# <command>
#            <proto>void <name>glTexBuffer</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#        </command>
#        
__glTexBuffer_impl=None
def glTexBuffer (target, internalformat, buffer):
    global __glTexBuffer_impl
    if not __glTexBuffer_impl:
        fptr = __pyglGetFuncAddress('glTexBuffer')
        if not fptr:
            raise RuntimeError('The function glTexBuffer is not available')
        __glTexBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glTexBuffer = __glTexBuffer_impl
    return glTexBuffer(target, internalformat, buffer)
# <command>
#            <proto>void <name>glTexBufferRange</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param group="BufferOffset"><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#        </command>
#        
__glTexBufferRange_impl=None
def glTexBufferRange (target, internalformat, buffer, offset, size):
    global __glTexBufferRange_impl
    if not __glTexBufferRange_impl:
        fptr = __pyglGetFuncAddress('glTexBufferRange')
        if not fptr:
            raise RuntimeError('The function glTexBufferRange is not available')
        __glTexBufferRange_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_size_t, c_void_p)(fptr)
    glTexBufferRange = __glTexBufferRange_impl
    return glTexBufferRange(target, internalformat, buffer, offset, size)
# <command>
#            <proto>void <name>glTexImage1D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="TextureComponentCount"><ptype>GLint</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>border</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param group="PixelType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type,width)">const void *<name>pixels</name></param>
#            <glx opcode="109" type="render" />
#            <glx comment="PBO protocol" name="glTexImage1DPBO" opcode="328" type="render" />
#        </command>
#        
__glTexImage1D_impl=None
def glTexImage1D (target, level, internalformat, width, border, format, type, pixels):
    global __glTexImage1D_impl
    if not __glTexImage1D_impl:
        fptr = __pyglGetFuncAddress('glTexImage1D')
        if not fptr:
            raise RuntimeError('The function glTexImage1D is not available')
        __glTexImage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glTexImage1D = (lambda target,level,internalformat,width,border,format,type,pixels:__glTexImage1D_impl(target,level,internalformat,width,border,format,type,__pyglGetAsConstVoidPointer( pixels )))
    return glTexImage1D(target, level, internalformat, width, border, format, type, pixels)
# <command>
#            <proto>void <name>glTexImage2D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="TextureComponentCount"><ptype>GLint</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>border</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param group="PixelType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type,width,height)">const void *<name>pixels</name></param>
#            <glx opcode="110" type="render" />
#            <glx comment="PBO protocol" name="glTexImage2DPBO" opcode="329" type="render" />
#        </command>
#        
__glTexImage2D_impl=None
def glTexImage2D (target, level, internalformat, width, height, border, format, type, pixels):
    global __glTexImage2D_impl
    if not __glTexImage2D_impl:
        fptr = __pyglGetFuncAddress('glTexImage2D')
        if not fptr:
            raise RuntimeError('The function glTexImage2D is not available')
        __glTexImage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glTexImage2D = (lambda target,level,internalformat,width,height,border,format,type,pixels:__glTexImage2D_impl(target,level,internalformat,width,height,border,format,type,__pyglGetAsConstVoidPointer( pixels )))
    return glTexImage2D(target, level, internalformat, width, height, border, format, type, pixels)
# <command>
#            <proto>void <name>glTexImage3D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="TextureComponentCount"><ptype>GLint</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>border</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param group="PixelType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type,width,height,depth)">const void *<name>pixels</name></param>
#            <glx opcode="4114" type="render" />
#            <glx comment="PBO protocol" name="glTexImage3DPBO" opcode="330" type="render" />
#        </command>
#        
__glTexImage3D_impl=None
def glTexImage3D (target, level, internalformat, width, height, depth, border, format, type, pixels):
    global __glTexImage3D_impl
    if not __glTexImage3D_impl:
        fptr = __pyglGetFuncAddress('glTexImage3D')
        if not fptr:
            raise RuntimeError('The function glTexImage3D is not available')
        __glTexImage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glTexImage3D = (lambda target,level,internalformat,width,height,depth,border,format,type,pixels:__glTexImage3D_impl(target,level,internalformat,width,height,depth,border,format,type,__pyglGetAsConstVoidPointer( pixels )))
    return glTexImage3D(target, level, internalformat, width, height, depth, border, format, type, pixels)
# <command>
#            <proto>void <name>glTexParameterIiv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="TextureParameterName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)">const <ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="346" type="render" />
#        </command>
#        
__glTexParameterIiv_impl=None
def glTexParameterIiv (target, pname, params):
    global __glTexParameterIiv_impl
    if not __glTexParameterIiv_impl:
        fptr = __pyglGetFuncAddress('glTexParameterIiv')
        if not fptr:
            raise RuntimeError('The function glTexParameterIiv is not available')
        __glTexParameterIiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glTexParameterIiv = (lambda target,pname,params:__glTexParameterIiv_impl(target,pname,__pyglGetAsConstVoidPointer( params )))
    return glTexParameterIiv(target, pname, params)
# <command>
#            <proto>void <name>glTexParameterIuiv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="TextureParameterName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param len="COMPSIZE(pname)">const <ptype>GLuint</ptype> *<name>params</name></param>
#            <glx opcode="347" type="render" />
#        </command>
#        
__glTexParameterIuiv_impl=None
def glTexParameterIuiv (target, pname, params):
    global __glTexParameterIuiv_impl
    if not __glTexParameterIuiv_impl:
        fptr = __pyglGetFuncAddress('glTexParameterIuiv')
        if not fptr:
            raise RuntimeError('The function glTexParameterIuiv is not available')
        __glTexParameterIuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glTexParameterIuiv = (lambda target,pname,params:__glTexParameterIuiv_impl(target,pname,__pyglGetAsConstVoidPointer( params )))
    return glTexParameterIuiv(target, pname, params)
# <command>
#            <proto>void <name>glTexParameterf</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="TextureParameterName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param group="CheckedFloat32"><ptype>GLfloat</ptype> <name>param</name></param>
#            <glx opcode="105" type="render" />
#        </command>
#        
__glTexParameterf_impl=None
def glTexParameterf (target, pname, param):
    global __glTexParameterf_impl
    if not __glTexParameterf_impl:
        fptr = __pyglGetFuncAddress('glTexParameterf')
        if not fptr:
            raise RuntimeError('The function glTexParameterf is not available')
        __glTexParameterf_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_float)(fptr)
    glTexParameterf = __glTexParameterf_impl
    return glTexParameterf(target, pname, param)
# <command>
#            <proto>void <name>glTexParameterfv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="TextureParameterName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param group="CheckedFloat32" len="COMPSIZE(pname)">const <ptype>GLfloat</ptype> *<name>params</name></param>
#            <glx opcode="106" type="render" />
#        </command>
#        
__glTexParameterfv_impl=None
def glTexParameterfv (target, pname, params):
    global __glTexParameterfv_impl
    if not __glTexParameterfv_impl:
        fptr = __pyglGetFuncAddress('glTexParameterfv')
        if not fptr:
            raise RuntimeError('The function glTexParameterfv is not available')
        __glTexParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glTexParameterfv = (lambda target,pname,params:__glTexParameterfv_impl(target,pname,__pyglGetAsConstVoidPointer( params )))
    return glTexParameterfv(target, pname, params)
# <command>
#            <proto>void <name>glTexParameteri</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="TextureParameterName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>param</name></param>
#            <glx opcode="107" type="render" />
#        </command>
#        
__glTexParameteri_impl=None
def glTexParameteri (target, pname, param):
    global __glTexParameteri_impl
    if not __glTexParameteri_impl:
        fptr = __pyglGetFuncAddress('glTexParameteri')
        if not fptr:
            raise RuntimeError('The function glTexParameteri is not available')
        __glTexParameteri_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int)(fptr)
    glTexParameteri = __glTexParameteri_impl
    return glTexParameteri(target, pname, param)
# <command>
#            <proto>void <name>glTexParameteriv</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="TextureParameterName"><ptype>GLenum</ptype> <name>pname</name></param>
#            <param group="CheckedInt32" len="COMPSIZE(pname)">const <ptype>GLint</ptype> *<name>params</name></param>
#            <glx opcode="108" type="render" />
#        </command>
#        
__glTexParameteriv_impl=None
def glTexParameteriv (target, pname, params):
    global __glTexParameteriv_impl
    if not __glTexParameteriv_impl:
        fptr = __pyglGetFuncAddress('glTexParameteriv')
        if not fptr:
            raise RuntimeError('The function glTexParameteriv is not available')
        __glTexParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glTexParameteriv = (lambda target,pname,params:__glTexParameteriv_impl(target,pname,__pyglGetAsConstVoidPointer( params )))
    return glTexParameteriv(target, pname, params)
# <command>
#            <proto>void <name>glTexStorage1D</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLsizei</ptype> <name>levels</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#        </command>
#        
__glTexStorage1D_impl=None
def glTexStorage1D (target, levels, internalformat, width):
    global __glTexStorage1D_impl
    if not __glTexStorage1D_impl:
        fptr = __pyglGetFuncAddress('glTexStorage1D')
        if not fptr:
            raise RuntimeError('The function glTexStorage1D is not available')
        __glTexStorage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int)(fptr)
    glTexStorage1D = __glTexStorage1D_impl
    return glTexStorage1D(target, levels, internalformat, width)
# <command>
#            <proto>void <name>glTexStorage2D</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLsizei</ptype> <name>levels</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#        </command>
#        
__glTexStorage2D_impl=None
def glTexStorage2D (target, levels, internalformat, width, height):
    global __glTexStorage2D_impl
    if not __glTexStorage2D_impl:
        fptr = __pyglGetFuncAddress('glTexStorage2D')
        if not fptr:
            raise RuntimeError('The function glTexStorage2D is not available')
        __glTexStorage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int)(fptr)
    glTexStorage2D = __glTexStorage2D_impl
    return glTexStorage2D(target, levels, internalformat, width, height)
# <command>
#            <proto>void <name>glTexStorage3D</name></proto>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLsizei</ptype> <name>levels</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#        </command>
#        
__glTexStorage3D_impl=None
def glTexStorage3D (target, levels, internalformat, width, height, depth):
    global __glTexStorage3D_impl
    if not __glTexStorage3D_impl:
        fptr = __pyglGetFuncAddress('glTexStorage3D')
        if not fptr:
            raise RuntimeError('The function glTexStorage3D is not available')
        __glTexStorage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int, c_int)(fptr)
    glTexStorage3D = __glTexStorage3D_impl
    return glTexStorage3D(target, levels, internalformat, width, height, depth)
# <command>
#            <proto>void <name>glTexSubImage1D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param group="PixelType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type,width)">const void *<name>pixels</name></param>
#            <glx opcode="4099" type="render" />
#            <glx comment="PBO protocol" name="glTexSubImage1DPBO" opcode="331" type="render" />
#        </command>
#        
__glTexSubImage1D_impl=None
def glTexSubImage1D (target, level, xoffset, width, format, type, pixels):
    global __glTexSubImage1D_impl
    if not __glTexSubImage1D_impl:
        fptr = __pyglGetFuncAddress('glTexSubImage1D')
        if not fptr:
            raise RuntimeError('The function glTexSubImage1D is not available')
        __glTexSubImage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glTexSubImage1D = (lambda target,level,xoffset,width,format,type,pixels:__glTexSubImage1D_impl(target,level,xoffset,width,format,type,__pyglGetAsConstVoidPointer( pixels )))
    return glTexSubImage1D(target, level, xoffset, width, format, type, pixels)
# <command>
#            <proto>void <name>glTexSubImage2D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param group="PixelType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type,width,height)">const void *<name>pixels</name></param>
#            <glx opcode="4100" type="render" />
#            <glx comment="PBO protocol" name="glTexSubImage2DPBO" opcode="332" type="render" />
#        </command>
#        
__glTexSubImage2D_impl=None
def glTexSubImage2D (target, level, xoffset, yoffset, width, height, format, type, pixels):
    global __glTexSubImage2D_impl
    if not __glTexSubImage2D_impl:
        fptr = __pyglGetFuncAddress('glTexSubImage2D')
        if not fptr:
            raise RuntimeError('The function glTexSubImage2D is not available')
        __glTexSubImage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glTexSubImage2D = (lambda target,level,xoffset,yoffset,width,height,format,type,pixels:__glTexSubImage2D_impl(target,level,xoffset,yoffset,width,height,format,type,__pyglGetAsConstVoidPointer( pixels )))
    return glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, pixels)
# <command>
#            <proto>void <name>glTexSubImage3D</name></proto>
#            <param group="TextureTarget"><ptype>GLenum</ptype> <name>target</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>level</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param group="CheckedInt32"><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#            <param group="PixelFormat"><ptype>GLenum</ptype> <name>format</name></param>
#            <param group="PixelType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param len="COMPSIZE(format,type,width,height,depth)">const void *<name>pixels</name></param>
#            <glx opcode="4115" type="render" />
#            <glx comment="PBO protocol" name="glTexSubImage3DPBO" opcode="333" type="render" />
#        </command>
#        
__glTexSubImage3D_impl=None
def glTexSubImage3D (target, level, xoffset, yoffset, zoffset, width, height, depth, format, type, pixels):
    global __glTexSubImage3D_impl
    if not __glTexSubImage3D_impl:
        fptr = __pyglGetFuncAddress('glTexSubImage3D')
        if not fptr:
            raise RuntimeError('The function glTexSubImage3D is not available')
        __glTexSubImage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glTexSubImage3D = (lambda target,level,xoffset,yoffset,zoffset,width,height,depth,format,type,pixels:__glTexSubImage3D_impl(target,level,xoffset,yoffset,zoffset,width,height,depth,format,type,__pyglGetAsConstVoidPointer( pixels )))
    return glTexSubImage3D(target, level, xoffset, yoffset, zoffset, width, height, depth, format, type, pixels)
# <command>
#            <proto>void <name>glTextureBarrier</name></proto>
#        </command>
#        
__glTextureBarrier_impl=None
def glTextureBarrier ():
    global __glTextureBarrier_impl
    if not __glTextureBarrier_impl:
        fptr = __pyglGetFuncAddress('glTextureBarrier')
        if not fptr:
            raise RuntimeError('The function glTextureBarrier is not available')
        __glTextureBarrier_impl = __PYGL_FUNC_TYPE( None ,)(fptr)
    glTextureBarrier = __glTextureBarrier_impl
    return glTextureBarrier()
# <command>
#            <proto>void <name>glTextureBuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#        </command>
#        
__glTextureBuffer_impl=None
def glTextureBuffer (texture, internalformat, buffer):
    global __glTextureBuffer_impl
    if not __glTextureBuffer_impl:
        fptr = __pyglGetFuncAddress('glTextureBuffer')
        if not fptr:
            raise RuntimeError('The function glTextureBuffer is not available')
        __glTextureBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glTextureBuffer = __glTextureBuffer_impl
    return glTextureBuffer(texture, internalformat, buffer)
# <command>
#            <proto>void <name>glTextureBufferRange</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#        </command>
#        
__glTextureBufferRange_impl=None
def glTextureBufferRange (texture, internalformat, buffer, offset, size):
    global __glTextureBufferRange_impl
    if not __glTextureBufferRange_impl:
        fptr = __pyglGetFuncAddress('glTextureBufferRange')
        if not fptr:
            raise RuntimeError('The function glTextureBufferRange is not available')
        __glTextureBufferRange_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_size_t, c_void_p)(fptr)
    glTextureBufferRange = __glTextureBufferRange_impl
    return glTextureBufferRange(texture, internalformat, buffer, offset, size)
# <command>
#            <proto>void <name>glTextureParameterIiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param>const <ptype>GLint</ptype> *<name>params</name></param>
#        </command>
#        
__glTextureParameterIiv_impl=None
def glTextureParameterIiv (texture, pname, params):
    global __glTextureParameterIiv_impl
    if not __glTextureParameterIiv_impl:
        fptr = __pyglGetFuncAddress('glTextureParameterIiv')
        if not fptr:
            raise RuntimeError('The function glTextureParameterIiv is not available')
        __glTextureParameterIiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glTextureParameterIiv = (lambda texture,pname,params:__glTextureParameterIiv_impl(texture,pname,__pyglGetAsConstVoidPointer( params )))
    return glTextureParameterIiv(texture, pname, params)
# <command>
#            <proto>void <name>glTextureParameterIuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param>const <ptype>GLuint</ptype> *<name>params</name></param>
#        </command>
#        
__glTextureParameterIuiv_impl=None
def glTextureParameterIuiv (texture, pname, params):
    global __glTextureParameterIuiv_impl
    if not __glTextureParameterIuiv_impl:
        fptr = __pyglGetFuncAddress('glTextureParameterIuiv')
        if not fptr:
            raise RuntimeError('The function glTextureParameterIuiv is not available')
        __glTextureParameterIuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glTextureParameterIuiv = (lambda texture,pname,params:__glTextureParameterIuiv_impl(texture,pname,__pyglGetAsConstVoidPointer( params )))
    return glTextureParameterIuiv(texture, pname, params)
# <command>
#            <proto>void <name>glTextureParameterf</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLfloat</ptype> <name>param</name></param>
#        </command>
#        
__glTextureParameterf_impl=None
def glTextureParameterf (texture, pname, param):
    global __glTextureParameterf_impl
    if not __glTextureParameterf_impl:
        fptr = __pyglGetFuncAddress('glTextureParameterf')
        if not fptr:
            raise RuntimeError('The function glTextureParameterf is not available')
        __glTextureParameterf_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_float)(fptr)
    glTextureParameterf = __glTextureParameterf_impl
    return glTextureParameterf(texture, pname, param)
# <command>
#            <proto>void <name>glTextureParameterfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param>const <ptype>GLfloat</ptype> *<name>param</name></param>
#        </command>
#        
__glTextureParameterfv_impl=None
def glTextureParameterfv (texture, pname, param):
    global __glTextureParameterfv_impl
    if not __glTextureParameterfv_impl:
        fptr = __pyglGetFuncAddress('glTextureParameterfv')
        if not fptr:
            raise RuntimeError('The function glTextureParameterfv is not available')
        __glTextureParameterfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glTextureParameterfv = (lambda texture,pname,param:__glTextureParameterfv_impl(texture,pname,__pyglGetAsConstVoidPointer( param )))
    return glTextureParameterfv(texture, pname, param)
# <command>
#            <proto>void <name>glTextureParameteri</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param><ptype>GLint</ptype> <name>param</name></param>
#        </command>
#        
__glTextureParameteri_impl=None
def glTextureParameteri (texture, pname, param):
    global __glTextureParameteri_impl
    if not __glTextureParameteri_impl:
        fptr = __pyglGetFuncAddress('glTextureParameteri')
        if not fptr:
            raise RuntimeError('The function glTextureParameteri is not available')
        __glTextureParameteri_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int)(fptr)
    glTextureParameteri = __glTextureParameteri_impl
    return glTextureParameteri(texture, pname, param)
# <command>
#            <proto>void <name>glTextureParameteriv</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>pname</name></param>
#            <param>const <ptype>GLint</ptype> *<name>param</name></param>
#        </command>
#        
__glTextureParameteriv_impl=None
def glTextureParameteriv (texture, pname, param):
    global __glTextureParameteriv_impl
    if not __glTextureParameteriv_impl:
        fptr = __pyglGetFuncAddress('glTextureParameteriv')
        if not fptr:
            raise RuntimeError('The function glTextureParameteriv is not available')
        __glTextureParameteriv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_void_p)(fptr)
    glTextureParameteriv = (lambda texture,pname,param:__glTextureParameteriv_impl(texture,pname,__pyglGetAsConstVoidPointer( param )))
    return glTextureParameteriv(texture, pname, param)
# <command>
#            <proto>void <name>glTextureStorage1D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLsizei</ptype> <name>levels</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#        </command>
#        
__glTextureStorage1D_impl=None
def glTextureStorage1D (texture, levels, internalformat, width):
    global __glTextureStorage1D_impl
    if not __glTextureStorage1D_impl:
        fptr = __pyglGetFuncAddress('glTextureStorage1D')
        if not fptr:
            raise RuntimeError('The function glTextureStorage1D is not available')
        __glTextureStorage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int)(fptr)
    glTextureStorage1D = __glTextureStorage1D_impl
    return glTextureStorage1D(texture, levels, internalformat, width)
# <command>
#            <proto>void <name>glTextureStorage2D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLsizei</ptype> <name>levels</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#        </command>
#        
__glTextureStorage2D_impl=None
def glTextureStorage2D (texture, levels, internalformat, width, height):
    global __glTextureStorage2D_impl
    if not __glTextureStorage2D_impl:
        fptr = __pyglGetFuncAddress('glTextureStorage2D')
        if not fptr:
            raise RuntimeError('The function glTextureStorage2D is not available')
        __glTextureStorage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int)(fptr)
    glTextureStorage2D = __glTextureStorage2D_impl
    return glTextureStorage2D(texture, levels, internalformat, width, height)
# <command>
#            <proto>void <name>glTextureStorage3D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLsizei</ptype> <name>levels</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#        </command>
#        
__glTextureStorage3D_impl=None
def glTextureStorage3D (texture, levels, internalformat, width, height, depth):
    global __glTextureStorage3D_impl
    if not __glTextureStorage3D_impl:
        fptr = __pyglGetFuncAddress('glTextureStorage3D')
        if not fptr:
            raise RuntimeError('The function glTextureStorage3D is not available')
        __glTextureStorage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_int, c_int, c_int)(fptr)
    glTextureStorage3D = __glTextureStorage3D_impl
    return glTextureStorage3D(texture, levels, internalformat, width, height, depth)
# <command>
#            <proto>void <name>glTextureSubImage1D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param>const void *<name>pixels</name></param>
#        </command>
#        
__glTextureSubImage1D_impl=None
def glTextureSubImage1D (texture, level, xoffset, width, format, type, pixels):
    global __glTextureSubImage1D_impl
    if not __glTextureSubImage1D_impl:
        fptr = __pyglGetFuncAddress('glTextureSubImage1D')
        if not fptr:
            raise RuntimeError('The function glTextureSubImage1D is not available')
        __glTextureSubImage1D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glTextureSubImage1D = (lambda texture,level,xoffset,width,format,type,pixels:__glTextureSubImage1D_impl(texture,level,xoffset,width,format,type,__pyglGetAsConstVoidPointer( pixels )))
    return glTextureSubImage1D(texture, level, xoffset, width, format, type, pixels)
# <command>
#            <proto>void <name>glTextureSubImage2D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param>const void *<name>pixels</name></param>
#        </command>
#        
__glTextureSubImage2D_impl=None
def glTextureSubImage2D (texture, level, xoffset, yoffset, width, height, format, type, pixels):
    global __glTextureSubImage2D_impl
    if not __glTextureSubImage2D_impl:
        fptr = __pyglGetFuncAddress('glTextureSubImage2D')
        if not fptr:
            raise RuntimeError('The function glTextureSubImage2D is not available')
        __glTextureSubImage2D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glTextureSubImage2D = (lambda texture,level,xoffset,yoffset,width,height,format,type,pixels:__glTextureSubImage2D_impl(texture,level,xoffset,yoffset,width,height,format,type,__pyglGetAsConstVoidPointer( pixels )))
    return glTextureSubImage2D(texture, level, xoffset, yoffset, width, height, format, type, pixels)
# <command>
#            <proto>void <name>glTextureSubImage3D</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLint</ptype> <name>level</name></param>
#            <param><ptype>GLint</ptype> <name>xoffset</name></param>
#            <param><ptype>GLint</ptype> <name>yoffset</name></param>
#            <param><ptype>GLint</ptype> <name>zoffset</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <param><ptype>GLsizei</ptype> <name>depth</name></param>
#            <param><ptype>GLenum</ptype> <name>format</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param>const void *<name>pixels</name></param>
#        </command>
#        
__glTextureSubImage3D_impl=None
def glTextureSubImage3D (texture, level, xoffset, yoffset, zoffset, width, height, depth, format, type, pixels):
    global __glTextureSubImage3D_impl
    if not __glTextureSubImage3D_impl:
        fptr = __pyglGetFuncAddress('glTextureSubImage3D')
        if not fptr:
            raise RuntimeError('The function glTextureSubImage3D is not available')
        __glTextureSubImage3D_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_uint, c_uint, c_void_p)(fptr)
    glTextureSubImage3D = (lambda texture,level,xoffset,yoffset,zoffset,width,height,depth,format,type,pixels:__glTextureSubImage3D_impl(texture,level,xoffset,yoffset,zoffset,width,height,depth,format,type,__pyglGetAsConstVoidPointer( pixels )))
    return glTextureSubImage3D(texture, level, xoffset, yoffset, zoffset, width, height, depth, format, type, pixels)
# <command>
#            <proto>void <name>glTextureView</name></proto>
#            <param><ptype>GLuint</ptype> <name>texture</name></param>
#            <param><ptype>GLenum</ptype> <name>target</name></param>
#            <param><ptype>GLuint</ptype> <name>origtexture</name></param>
#            <param><ptype>GLenum</ptype> <name>internalformat</name></param>
#            <param><ptype>GLuint</ptype> <name>minlevel</name></param>
#            <param><ptype>GLuint</ptype> <name>numlevels</name></param>
#            <param><ptype>GLuint</ptype> <name>minlayer</name></param>
#            <param><ptype>GLuint</ptype> <name>numlayers</name></param>
#        </command>
#        
__glTextureView_impl=None
def glTextureView (texture, target, origtexture, internalformat, minlevel, numlevels, minlayer, numlayers):
    global __glTextureView_impl
    if not __glTextureView_impl:
        fptr = __pyglGetFuncAddress('glTextureView')
        if not fptr:
            raise RuntimeError('The function glTextureView is not available')
        __glTextureView_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_uint, c_uint, c_uint, c_uint)(fptr)
    glTextureView = __glTextureView_impl
    return glTextureView(texture, target, origtexture, internalformat, minlevel, numlevels, minlayer, numlayers)
# <command>
#            <proto>void <name>glTransformFeedbackBufferBase</name></proto>
#            <param><ptype>GLuint</ptype> <name>xfb</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#        </command>
#        
__glTransformFeedbackBufferBase_impl=None
def glTransformFeedbackBufferBase (xfb, index, buffer):
    global __glTransformFeedbackBufferBase_impl
    if not __glTransformFeedbackBufferBase_impl:
        fptr = __pyglGetFuncAddress('glTransformFeedbackBufferBase')
        if not fptr:
            raise RuntimeError('The function glTransformFeedbackBufferBase is not available')
        __glTransformFeedbackBufferBase_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glTransformFeedbackBufferBase = __glTransformFeedbackBufferBase_impl
    return glTransformFeedbackBufferBase(xfb, index, buffer)
# <command>
#            <proto>void <name>glTransformFeedbackBufferRange</name></proto>
#            <param><ptype>GLuint</ptype> <name>xfb</name></param>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param group="BufferSize"><ptype>GLsizeiptr</ptype> <name>size</name></param>
#        </command>
#        
__glTransformFeedbackBufferRange_impl=None
def glTransformFeedbackBufferRange (xfb, index, buffer, offset, size):
    global __glTransformFeedbackBufferRange_impl
    if not __glTransformFeedbackBufferRange_impl:
        fptr = __pyglGetFuncAddress('glTransformFeedbackBufferRange')
        if not fptr:
            raise RuntimeError('The function glTransformFeedbackBufferRange is not available')
        __glTransformFeedbackBufferRange_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_size_t, c_void_p)(fptr)
    glTransformFeedbackBufferRange = __glTransformFeedbackBufferRange_impl
    return glTransformFeedbackBufferRange(xfb, index, buffer, offset, size)
# <command>
#            <proto>void <name>glTransformFeedbackVaryings</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLchar</ptype> *const*<name>varyings</name></param>
#            <param><ptype>GLenum</ptype> <name>bufferMode</name></param>
#        </command>
#        
__glTransformFeedbackVaryings_impl=None
def glTransformFeedbackVaryings (program, count, varyings, bufferMode):
    global __glTransformFeedbackVaryings_impl
    if not __glTransformFeedbackVaryings_impl:
        fptr = __pyglGetFuncAddress('glTransformFeedbackVaryings')
        if not fptr:
            raise RuntimeError('The function glTransformFeedbackVaryings is not available')
        __glTransformFeedbackVaryings_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p, c_uint)(fptr)
    glTransformFeedbackVaryings = (lambda program,count,varyings,bufferMode:__glTransformFeedbackVaryings_impl(program,count,c_char_p( varyings .encode() ),bufferMode))
    return glTransformFeedbackVaryings(program, count, varyings, bufferMode)
# <command>
#            <proto>void <name>glUniform1d</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#        </command>
#        
__glUniform1d_impl=None
def glUniform1d (location, x):
    global __glUniform1d_impl
    if not __glUniform1d_impl:
        fptr = __pyglGetFuncAddress('glUniform1d')
        if not fptr:
            raise RuntimeError('The function glUniform1d is not available')
        __glUniform1d_impl = __PYGL_FUNC_TYPE( None ,c_int, c_double)(fptr)
    glUniform1d = __glUniform1d_impl
    return glUniform1d(location, x)
# <command>
#            <proto>void <name>glUniform1dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*1">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform1dv_impl=None
def glUniform1dv (location, count, value):
    global __glUniform1dv_impl
    if not __glUniform1dv_impl:
        fptr = __pyglGetFuncAddress('glUniform1dv')
        if not fptr:
            raise RuntimeError('The function glUniform1dv is not available')
        __glUniform1dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform1dv = (lambda location,count,value:__glUniform1dv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform1dv(location, count, value)
# <command>
#            <proto>void <name>glUniform1f</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLfloat</ptype> <name>v0</name></param>
#        </command>
#        
__glUniform1f_impl=None
def glUniform1f (location, v0):
    global __glUniform1f_impl
    if not __glUniform1f_impl:
        fptr = __pyglGetFuncAddress('glUniform1f')
        if not fptr:
            raise RuntimeError('The function glUniform1f is not available')
        __glUniform1f_impl = __PYGL_FUNC_TYPE( None ,c_int, c_float)(fptr)
    glUniform1f = __glUniform1f_impl
    return glUniform1f(location, v0)
# <command>
#            <proto>void <name>glUniform1fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*1">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform1fv_impl=None
def glUniform1fv (location, count, value):
    global __glUniform1fv_impl
    if not __glUniform1fv_impl:
        fptr = __pyglGetFuncAddress('glUniform1fv')
        if not fptr:
            raise RuntimeError('The function glUniform1fv is not available')
        __glUniform1fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform1fv = (lambda location,count,value:__glUniform1fv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform1fv(location, count, value)
# <command>
#            <proto>void <name>glUniform1i</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLint</ptype> <name>v0</name></param>
#        </command>
#        
__glUniform1i_impl=None
def glUniform1i (location, v0):
    global __glUniform1i_impl
    if not __glUniform1i_impl:
        fptr = __pyglGetFuncAddress('glUniform1i')
        if not fptr:
            raise RuntimeError('The function glUniform1i is not available')
        __glUniform1i_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int)(fptr)
    glUniform1i = __glUniform1i_impl
    return glUniform1i(location, v0)
# <command>
#            <proto>void <name>glUniform1iv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*1">const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform1iv_impl=None
def glUniform1iv (location, count, value):
    global __glUniform1iv_impl
    if not __glUniform1iv_impl:
        fptr = __pyglGetFuncAddress('glUniform1iv')
        if not fptr:
            raise RuntimeError('The function glUniform1iv is not available')
        __glUniform1iv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform1iv = (lambda location,count,value:__glUniform1iv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform1iv(location, count, value)
# <command>
#            <proto>void <name>glUniform1ui</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLuint</ptype> <name>v0</name></param>
#        </command>
#        
__glUniform1ui_impl=None
def glUniform1ui (location, v0):
    global __glUniform1ui_impl
    if not __glUniform1ui_impl:
        fptr = __pyglGetFuncAddress('glUniform1ui')
        if not fptr:
            raise RuntimeError('The function glUniform1ui is not available')
        __glUniform1ui_impl = __PYGL_FUNC_TYPE( None ,c_int, c_uint)(fptr)
    glUniform1ui = __glUniform1ui_impl
    return glUniform1ui(location, v0)
# <command>
#            <proto>void <name>glUniform1uiv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*1">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform1uiv_impl=None
def glUniform1uiv (location, count, value):
    global __glUniform1uiv_impl
    if not __glUniform1uiv_impl:
        fptr = __pyglGetFuncAddress('glUniform1uiv')
        if not fptr:
            raise RuntimeError('The function glUniform1uiv is not available')
        __glUniform1uiv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform1uiv = (lambda location,count,value:__glUniform1uiv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform1uiv(location, count, value)
# <command>
#            <proto>void <name>glUniform2d</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <param><ptype>GLdouble</ptype> <name>y</name></param>
#        </command>
#        
__glUniform2d_impl=None
def glUniform2d (location, x, y):
    global __glUniform2d_impl
    if not __glUniform2d_impl:
        fptr = __pyglGetFuncAddress('glUniform2d')
        if not fptr:
            raise RuntimeError('The function glUniform2d is not available')
        __glUniform2d_impl = __PYGL_FUNC_TYPE( None ,c_int, c_double, c_double)(fptr)
    glUniform2d = __glUniform2d_impl
    return glUniform2d(location, x, y)
# <command>
#            <proto>void <name>glUniform2dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*2">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform2dv_impl=None
def glUniform2dv (location, count, value):
    global __glUniform2dv_impl
    if not __glUniform2dv_impl:
        fptr = __pyglGetFuncAddress('glUniform2dv')
        if not fptr:
            raise RuntimeError('The function glUniform2dv is not available')
        __glUniform2dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform2dv = (lambda location,count,value:__glUniform2dv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform2dv(location, count, value)
# <command>
#            <proto>void <name>glUniform2f</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLfloat</ptype> <name>v0</name></param>
#            <param><ptype>GLfloat</ptype> <name>v1</name></param>
#        </command>
#        
__glUniform2f_impl=None
def glUniform2f (location, v0, v1):
    global __glUniform2f_impl
    if not __glUniform2f_impl:
        fptr = __pyglGetFuncAddress('glUniform2f')
        if not fptr:
            raise RuntimeError('The function glUniform2f is not available')
        __glUniform2f_impl = __PYGL_FUNC_TYPE( None ,c_int, c_float, c_float)(fptr)
    glUniform2f = __glUniform2f_impl
    return glUniform2f(location, v0, v1)
# <command>
#            <proto>void <name>glUniform2fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*2">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform2fv_impl=None
def glUniform2fv (location, count, value):
    global __glUniform2fv_impl
    if not __glUniform2fv_impl:
        fptr = __pyglGetFuncAddress('glUniform2fv')
        if not fptr:
            raise RuntimeError('The function glUniform2fv is not available')
        __glUniform2fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform2fv = (lambda location,count,value:__glUniform2fv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform2fv(location, count, value)
# <command>
#            <proto>void <name>glUniform2i</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLint</ptype> <name>v0</name></param>
#            <param><ptype>GLint</ptype> <name>v1</name></param>
#        </command>
#        
__glUniform2i_impl=None
def glUniform2i (location, v0, v1):
    global __glUniform2i_impl
    if not __glUniform2i_impl:
        fptr = __pyglGetFuncAddress('glUniform2i')
        if not fptr:
            raise RuntimeError('The function glUniform2i is not available')
        __glUniform2i_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_int)(fptr)
    glUniform2i = __glUniform2i_impl
    return glUniform2i(location, v0, v1)
# <command>
#            <proto>void <name>glUniform2iv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*2">const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform2iv_impl=None
def glUniform2iv (location, count, value):
    global __glUniform2iv_impl
    if not __glUniform2iv_impl:
        fptr = __pyglGetFuncAddress('glUniform2iv')
        if not fptr:
            raise RuntimeError('The function glUniform2iv is not available')
        __glUniform2iv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform2iv = (lambda location,count,value:__glUniform2iv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform2iv(location, count, value)
# <command>
#            <proto>void <name>glUniform2ui</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLuint</ptype> <name>v0</name></param>
#            <param><ptype>GLuint</ptype> <name>v1</name></param>
#        </command>
#        
__glUniform2ui_impl=None
def glUniform2ui (location, v0, v1):
    global __glUniform2ui_impl
    if not __glUniform2ui_impl:
        fptr = __pyglGetFuncAddress('glUniform2ui')
        if not fptr:
            raise RuntimeError('The function glUniform2ui is not available')
        __glUniform2ui_impl = __PYGL_FUNC_TYPE( None ,c_int, c_uint, c_uint)(fptr)
    glUniform2ui = __glUniform2ui_impl
    return glUniform2ui(location, v0, v1)
# <command>
#            <proto>void <name>glUniform2uiv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*2">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform2uiv_impl=None
def glUniform2uiv (location, count, value):
    global __glUniform2uiv_impl
    if not __glUniform2uiv_impl:
        fptr = __pyglGetFuncAddress('glUniform2uiv')
        if not fptr:
            raise RuntimeError('The function glUniform2uiv is not available')
        __glUniform2uiv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform2uiv = (lambda location,count,value:__glUniform2uiv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform2uiv(location, count, value)
# <command>
#            <proto>void <name>glUniform3d</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <param><ptype>GLdouble</ptype> <name>y</name></param>
#            <param><ptype>GLdouble</ptype> <name>z</name></param>
#        </command>
#        
__glUniform3d_impl=None
def glUniform3d (location, x, y, z):
    global __glUniform3d_impl
    if not __glUniform3d_impl:
        fptr = __pyglGetFuncAddress('glUniform3d')
        if not fptr:
            raise RuntimeError('The function glUniform3d is not available')
        __glUniform3d_impl = __PYGL_FUNC_TYPE( None ,c_int, c_double, c_double, c_double)(fptr)
    glUniform3d = __glUniform3d_impl
    return glUniform3d(location, x, y, z)
# <command>
#            <proto>void <name>glUniform3dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*3">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform3dv_impl=None
def glUniform3dv (location, count, value):
    global __glUniform3dv_impl
    if not __glUniform3dv_impl:
        fptr = __pyglGetFuncAddress('glUniform3dv')
        if not fptr:
            raise RuntimeError('The function glUniform3dv is not available')
        __glUniform3dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform3dv = (lambda location,count,value:__glUniform3dv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform3dv(location, count, value)
# <command>
#            <proto>void <name>glUniform3f</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLfloat</ptype> <name>v0</name></param>
#            <param><ptype>GLfloat</ptype> <name>v1</name></param>
#            <param><ptype>GLfloat</ptype> <name>v2</name></param>
#        </command>
#        
__glUniform3f_impl=None
def glUniform3f (location, v0, v1, v2):
    global __glUniform3f_impl
    if not __glUniform3f_impl:
        fptr = __pyglGetFuncAddress('glUniform3f')
        if not fptr:
            raise RuntimeError('The function glUniform3f is not available')
        __glUniform3f_impl = __PYGL_FUNC_TYPE( None ,c_int, c_float, c_float, c_float)(fptr)
    glUniform3f = __glUniform3f_impl
    return glUniform3f(location, v0, v1, v2)
# <command>
#            <proto>void <name>glUniform3fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*3">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform3fv_impl=None
def glUniform3fv (location, count, value):
    global __glUniform3fv_impl
    if not __glUniform3fv_impl:
        fptr = __pyglGetFuncAddress('glUniform3fv')
        if not fptr:
            raise RuntimeError('The function glUniform3fv is not available')
        __glUniform3fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform3fv = (lambda location,count,value:__glUniform3fv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform3fv(location, count, value)
# <command>
#            <proto>void <name>glUniform3i</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLint</ptype> <name>v0</name></param>
#            <param><ptype>GLint</ptype> <name>v1</name></param>
#            <param><ptype>GLint</ptype> <name>v2</name></param>
#        </command>
#        
__glUniform3i_impl=None
def glUniform3i (location, v0, v1, v2):
    global __glUniform3i_impl
    if not __glUniform3i_impl:
        fptr = __pyglGetFuncAddress('glUniform3i')
        if not fptr:
            raise RuntimeError('The function glUniform3i is not available')
        __glUniform3i_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_int, c_int)(fptr)
    glUniform3i = __glUniform3i_impl
    return glUniform3i(location, v0, v1, v2)
# <command>
#            <proto>void <name>glUniform3iv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*3">const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform3iv_impl=None
def glUniform3iv (location, count, value):
    global __glUniform3iv_impl
    if not __glUniform3iv_impl:
        fptr = __pyglGetFuncAddress('glUniform3iv')
        if not fptr:
            raise RuntimeError('The function glUniform3iv is not available')
        __glUniform3iv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform3iv = (lambda location,count,value:__glUniform3iv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform3iv(location, count, value)
# <command>
#            <proto>void <name>glUniform3ui</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLuint</ptype> <name>v0</name></param>
#            <param><ptype>GLuint</ptype> <name>v1</name></param>
#            <param><ptype>GLuint</ptype> <name>v2</name></param>
#        </command>
#        
__glUniform3ui_impl=None
def glUniform3ui (location, v0, v1, v2):
    global __glUniform3ui_impl
    if not __glUniform3ui_impl:
        fptr = __pyglGetFuncAddress('glUniform3ui')
        if not fptr:
            raise RuntimeError('The function glUniform3ui is not available')
        __glUniform3ui_impl = __PYGL_FUNC_TYPE( None ,c_int, c_uint, c_uint, c_uint)(fptr)
    glUniform3ui = __glUniform3ui_impl
    return glUniform3ui(location, v0, v1, v2)
# <command>
#            <proto>void <name>glUniform3uiv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*3">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform3uiv_impl=None
def glUniform3uiv (location, count, value):
    global __glUniform3uiv_impl
    if not __glUniform3uiv_impl:
        fptr = __pyglGetFuncAddress('glUniform3uiv')
        if not fptr:
            raise RuntimeError('The function glUniform3uiv is not available')
        __glUniform3uiv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform3uiv = (lambda location,count,value:__glUniform3uiv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform3uiv(location, count, value)
# <command>
#            <proto>void <name>glUniform4d</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <param><ptype>GLdouble</ptype> <name>y</name></param>
#            <param><ptype>GLdouble</ptype> <name>z</name></param>
#            <param><ptype>GLdouble</ptype> <name>w</name></param>
#        </command>
#        
__glUniform4d_impl=None
def glUniform4d (location, x, y, z, w):
    global __glUniform4d_impl
    if not __glUniform4d_impl:
        fptr = __pyglGetFuncAddress('glUniform4d')
        if not fptr:
            raise RuntimeError('The function glUniform4d is not available')
        __glUniform4d_impl = __PYGL_FUNC_TYPE( None ,c_int, c_double, c_double, c_double, c_double)(fptr)
    glUniform4d = __glUniform4d_impl
    return glUniform4d(location, x, y, z, w)
# <command>
#            <proto>void <name>glUniform4dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*4">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform4dv_impl=None
def glUniform4dv (location, count, value):
    global __glUniform4dv_impl
    if not __glUniform4dv_impl:
        fptr = __pyglGetFuncAddress('glUniform4dv')
        if not fptr:
            raise RuntimeError('The function glUniform4dv is not available')
        __glUniform4dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform4dv = (lambda location,count,value:__glUniform4dv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform4dv(location, count, value)
# <command>
#            <proto>void <name>glUniform4f</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLfloat</ptype> <name>v0</name></param>
#            <param><ptype>GLfloat</ptype> <name>v1</name></param>
#            <param><ptype>GLfloat</ptype> <name>v2</name></param>
#            <param><ptype>GLfloat</ptype> <name>v3</name></param>
#        </command>
#        
__glUniform4f_impl=None
def glUniform4f (location, v0, v1, v2, v3):
    global __glUniform4f_impl
    if not __glUniform4f_impl:
        fptr = __pyglGetFuncAddress('glUniform4f')
        if not fptr:
            raise RuntimeError('The function glUniform4f is not available')
        __glUniform4f_impl = __PYGL_FUNC_TYPE( None ,c_int, c_float, c_float, c_float, c_float)(fptr)
    glUniform4f = __glUniform4f_impl
    return glUniform4f(location, v0, v1, v2, v3)
# <command>
#            <proto>void <name>glUniform4fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*4">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform4fv_impl=None
def glUniform4fv (location, count, value):
    global __glUniform4fv_impl
    if not __glUniform4fv_impl:
        fptr = __pyglGetFuncAddress('glUniform4fv')
        if not fptr:
            raise RuntimeError('The function glUniform4fv is not available')
        __glUniform4fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform4fv = (lambda location,count,value:__glUniform4fv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform4fv(location, count, value)
# <command>
#            <proto>void <name>glUniform4i</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLint</ptype> <name>v0</name></param>
#            <param><ptype>GLint</ptype> <name>v1</name></param>
#            <param><ptype>GLint</ptype> <name>v2</name></param>
#            <param><ptype>GLint</ptype> <name>v3</name></param>
#        </command>
#        
__glUniform4i_impl=None
def glUniform4i (location, v0, v1, v2, v3):
    global __glUniform4i_impl
    if not __glUniform4i_impl:
        fptr = __pyglGetFuncAddress('glUniform4i')
        if not fptr:
            raise RuntimeError('The function glUniform4i is not available')
        __glUniform4i_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_int, c_int, c_int)(fptr)
    glUniform4i = __glUniform4i_impl
    return glUniform4i(location, v0, v1, v2, v3)
# <command>
#            <proto>void <name>glUniform4iv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*4">const <ptype>GLint</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform4iv_impl=None
def glUniform4iv (location, count, value):
    global __glUniform4iv_impl
    if not __glUniform4iv_impl:
        fptr = __pyglGetFuncAddress('glUniform4iv')
        if not fptr:
            raise RuntimeError('The function glUniform4iv is not available')
        __glUniform4iv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform4iv = (lambda location,count,value:__glUniform4iv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform4iv(location, count, value)
# <command>
#            <proto>void <name>glUniform4ui</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLuint</ptype> <name>v0</name></param>
#            <param><ptype>GLuint</ptype> <name>v1</name></param>
#            <param><ptype>GLuint</ptype> <name>v2</name></param>
#            <param><ptype>GLuint</ptype> <name>v3</name></param>
#        </command>
#        
__glUniform4ui_impl=None
def glUniform4ui (location, v0, v1, v2, v3):
    global __glUniform4ui_impl
    if not __glUniform4ui_impl:
        fptr = __pyglGetFuncAddress('glUniform4ui')
        if not fptr:
            raise RuntimeError('The function glUniform4ui is not available')
        __glUniform4ui_impl = __PYGL_FUNC_TYPE( None ,c_int, c_uint, c_uint, c_uint, c_uint)(fptr)
    glUniform4ui = __glUniform4ui_impl
    return glUniform4ui(location, v0, v1, v2, v3)
# <command>
#            <proto>void <name>glUniform4uiv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count*4">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glUniform4uiv_impl=None
def glUniform4uiv (location, count, value):
    global __glUniform4uiv_impl
    if not __glUniform4uiv_impl:
        fptr = __pyglGetFuncAddress('glUniform4uiv')
        if not fptr:
            raise RuntimeError('The function glUniform4uiv is not available')
        __glUniform4uiv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_void_p)(fptr)
    glUniform4uiv = (lambda location,count,value:__glUniform4uiv_impl(location,count,__pyglGetAsConstVoidPointer( value )))
    return glUniform4uiv(location, count, value)
# <command>
#            <proto>void <name>glUniformBlockBinding</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#            <param><ptype>GLuint</ptype> <name>uniformBlockIndex</name></param>
#            <param><ptype>GLuint</ptype> <name>uniformBlockBinding</name></param>
#        </command>
#        
__glUniformBlockBinding_impl=None
def glUniformBlockBinding (program, uniformBlockIndex, uniformBlockBinding):
    global __glUniformBlockBinding_impl
    if not __glUniformBlockBinding_impl:
        fptr = __pyglGetFuncAddress('glUniformBlockBinding')
        if not fptr:
            raise RuntimeError('The function glUniformBlockBinding is not available')
        __glUniformBlockBinding_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glUniformBlockBinding = __glUniformBlockBinding_impl
    return glUniformBlockBinding(program, uniformBlockIndex, uniformBlockBinding)
# <command>
#            <proto>void <name>glUniformMatrix2dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*4">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix2dv_impl=None
def glUniformMatrix2dv (location, count, transpose, value):
    global __glUniformMatrix2dv_impl
    if not __glUniformMatrix2dv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix2dv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix2dv is not available')
        __glUniformMatrix2dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix2dv = (lambda location,count,transpose,value:__glUniformMatrix2dv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix2dv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix2fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*4">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix2fv_impl=None
def glUniformMatrix2fv (location, count, transpose, value):
    global __glUniformMatrix2fv_impl
    if not __glUniformMatrix2fv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix2fv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix2fv is not available')
        __glUniformMatrix2fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix2fv = (lambda location,count,transpose,value:__glUniformMatrix2fv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix2fv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix2x3dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*6">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix2x3dv_impl=None
def glUniformMatrix2x3dv (location, count, transpose, value):
    global __glUniformMatrix2x3dv_impl
    if not __glUniformMatrix2x3dv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix2x3dv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix2x3dv is not available')
        __glUniformMatrix2x3dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix2x3dv = (lambda location,count,transpose,value:__glUniformMatrix2x3dv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix2x3dv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix2x3fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*6">const <ptype>GLfloat</ptype> *<name>value</name></param>
#            <glx opcode="305" type="render" />
#        </command>
#        
__glUniformMatrix2x3fv_impl=None
def glUniformMatrix2x3fv (location, count, transpose, value):
    global __glUniformMatrix2x3fv_impl
    if not __glUniformMatrix2x3fv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix2x3fv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix2x3fv is not available')
        __glUniformMatrix2x3fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix2x3fv = (lambda location,count,transpose,value:__glUniformMatrix2x3fv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix2x3fv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix2x4dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*8">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix2x4dv_impl=None
def glUniformMatrix2x4dv (location, count, transpose, value):
    global __glUniformMatrix2x4dv_impl
    if not __glUniformMatrix2x4dv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix2x4dv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix2x4dv is not available')
        __glUniformMatrix2x4dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix2x4dv = (lambda location,count,transpose,value:__glUniformMatrix2x4dv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix2x4dv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix2x4fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*8">const <ptype>GLfloat</ptype> *<name>value</name></param>
#            <glx opcode="307" type="render" />
#        </command>
#        
__glUniformMatrix2x4fv_impl=None
def glUniformMatrix2x4fv (location, count, transpose, value):
    global __glUniformMatrix2x4fv_impl
    if not __glUniformMatrix2x4fv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix2x4fv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix2x4fv is not available')
        __glUniformMatrix2x4fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix2x4fv = (lambda location,count,transpose,value:__glUniformMatrix2x4fv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix2x4fv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix3dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*9">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix3dv_impl=None
def glUniformMatrix3dv (location, count, transpose, value):
    global __glUniformMatrix3dv_impl
    if not __glUniformMatrix3dv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix3dv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix3dv is not available')
        __glUniformMatrix3dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix3dv = (lambda location,count,transpose,value:__glUniformMatrix3dv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix3dv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix3fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*9">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix3fv_impl=None
def glUniformMatrix3fv (location, count, transpose, value):
    global __glUniformMatrix3fv_impl
    if not __glUniformMatrix3fv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix3fv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix3fv is not available')
        __glUniformMatrix3fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix3fv = (lambda location,count,transpose,value:__glUniformMatrix3fv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix3fv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix3x2dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*6">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix3x2dv_impl=None
def glUniformMatrix3x2dv (location, count, transpose, value):
    global __glUniformMatrix3x2dv_impl
    if not __glUniformMatrix3x2dv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix3x2dv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix3x2dv is not available')
        __glUniformMatrix3x2dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix3x2dv = (lambda location,count,transpose,value:__glUniformMatrix3x2dv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix3x2dv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix3x2fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*6">const <ptype>GLfloat</ptype> *<name>value</name></param>
#            <glx opcode="306" type="render" />
#        </command>
#        
__glUniformMatrix3x2fv_impl=None
def glUniformMatrix3x2fv (location, count, transpose, value):
    global __glUniformMatrix3x2fv_impl
    if not __glUniformMatrix3x2fv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix3x2fv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix3x2fv is not available')
        __glUniformMatrix3x2fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix3x2fv = (lambda location,count,transpose,value:__glUniformMatrix3x2fv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix3x2fv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix3x4dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*12">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix3x4dv_impl=None
def glUniformMatrix3x4dv (location, count, transpose, value):
    global __glUniformMatrix3x4dv_impl
    if not __glUniformMatrix3x4dv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix3x4dv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix3x4dv is not available')
        __glUniformMatrix3x4dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix3x4dv = (lambda location,count,transpose,value:__glUniformMatrix3x4dv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix3x4dv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix3x4fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*12">const <ptype>GLfloat</ptype> *<name>value</name></param>
#            <glx opcode="309" type="render" />
#        </command>
#        
__glUniformMatrix3x4fv_impl=None
def glUniformMatrix3x4fv (location, count, transpose, value):
    global __glUniformMatrix3x4fv_impl
    if not __glUniformMatrix3x4fv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix3x4fv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix3x4fv is not available')
        __glUniformMatrix3x4fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix3x4fv = (lambda location,count,transpose,value:__glUniformMatrix3x4fv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix3x4fv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix4dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*16">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix4dv_impl=None
def glUniformMatrix4dv (location, count, transpose, value):
    global __glUniformMatrix4dv_impl
    if not __glUniformMatrix4dv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix4dv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix4dv is not available')
        __glUniformMatrix4dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix4dv = (lambda location,count,transpose,value:__glUniformMatrix4dv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix4dv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix4fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*16">const <ptype>GLfloat</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix4fv_impl=None
def glUniformMatrix4fv (location, count, transpose, value):
    global __glUniformMatrix4fv_impl
    if not __glUniformMatrix4fv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix4fv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix4fv is not available')
        __glUniformMatrix4fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix4fv = (lambda location,count,transpose,value:__glUniformMatrix4fv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix4fv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix4x2dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*8">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix4x2dv_impl=None
def glUniformMatrix4x2dv (location, count, transpose, value):
    global __glUniformMatrix4x2dv_impl
    if not __glUniformMatrix4x2dv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix4x2dv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix4x2dv is not available')
        __glUniformMatrix4x2dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix4x2dv = (lambda location,count,transpose,value:__glUniformMatrix4x2dv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix4x2dv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix4x2fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*8">const <ptype>GLfloat</ptype> *<name>value</name></param>
#            <glx opcode="308" type="render" />
#        </command>
#        
__glUniformMatrix4x2fv_impl=None
def glUniformMatrix4x2fv (location, count, transpose, value):
    global __glUniformMatrix4x2fv_impl
    if not __glUniformMatrix4x2fv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix4x2fv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix4x2fv is not available')
        __glUniformMatrix4x2fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix4x2fv = (lambda location,count,transpose,value:__glUniformMatrix4x2fv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix4x2fv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix4x3dv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*12">const <ptype>GLdouble</ptype> *<name>value</name></param>
#        </command>
#        
__glUniformMatrix4x3dv_impl=None
def glUniformMatrix4x3dv (location, count, transpose, value):
    global __glUniformMatrix4x3dv_impl
    if not __glUniformMatrix4x3dv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix4x3dv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix4x3dv is not available')
        __glUniformMatrix4x3dv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix4x3dv = (lambda location,count,transpose,value:__glUniformMatrix4x3dv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix4x3dv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformMatrix4x3fv</name></proto>
#            <param><ptype>GLint</ptype> <name>location</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>transpose</name></param>
#            <param len="count*12">const <ptype>GLfloat</ptype> *<name>value</name></param>
#            <glx opcode="310" type="render" />
#        </command>
#        
__glUniformMatrix4x3fv_impl=None
def glUniformMatrix4x3fv (location, count, transpose, value):
    global __glUniformMatrix4x3fv_impl
    if not __glUniformMatrix4x3fv_impl:
        fptr = __pyglGetFuncAddress('glUniformMatrix4x3fv')
        if not fptr:
            raise RuntimeError('The function glUniformMatrix4x3fv is not available')
        __glUniformMatrix4x3fv_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_char, c_void_p)(fptr)
    glUniformMatrix4x3fv = (lambda location,count,transpose,value:__glUniformMatrix4x3fv_impl(location,count,transpose,__pyglGetAsConstVoidPointer( value )))
    return glUniformMatrix4x3fv(location, count, transpose, value)
# <command>
#            <proto>void <name>glUniformSubroutinesuiv</name></proto>
#            <param><ptype>GLenum</ptype> <name>shadertype</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="count">const <ptype>GLuint</ptype> *<name>indices</name></param>
#        </command>
#        
__glUniformSubroutinesuiv_impl=None
def glUniformSubroutinesuiv (shadertype, count, indices):
    global __glUniformSubroutinesuiv_impl
    if not __glUniformSubroutinesuiv_impl:
        fptr = __pyglGetFuncAddress('glUniformSubroutinesuiv')
        if not fptr:
            raise RuntimeError('The function glUniformSubroutinesuiv is not available')
        __glUniformSubroutinesuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glUniformSubroutinesuiv = (lambda shadertype,count,indices:__glUniformSubroutinesuiv_impl(shadertype,count,__pyglGetAsConstVoidPointer( indices )))
    return glUniformSubroutinesuiv(shadertype, count, indices)
# <command>
#            <proto group="Boolean"><ptype>GLboolean</ptype> <name>glUnmapBuffer</name></proto>
#            <param group="BufferTargetARB"><ptype>GLenum</ptype> <name>target</name></param>
#        </command>
#        
__glUnmapBuffer_impl=None
def glUnmapBuffer (target):
    global __glUnmapBuffer_impl
    if not __glUnmapBuffer_impl:
        fptr = __pyglGetFuncAddress('glUnmapBuffer')
        if not fptr:
            raise RuntimeError('The function glUnmapBuffer is not available')
        __glUnmapBuffer_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glUnmapBuffer = __glUnmapBuffer_impl
    return glUnmapBuffer(target)
# <command>
#            <proto><ptype>GLboolean</ptype> <name>glUnmapNamedBuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#        </command>
#        
__glUnmapNamedBuffer_impl=None
def glUnmapNamedBuffer (buffer):
    global __glUnmapNamedBuffer_impl
    if not __glUnmapNamedBuffer_impl:
        fptr = __pyglGetFuncAddress('glUnmapNamedBuffer')
        if not fptr:
            raise RuntimeError('The function glUnmapNamedBuffer is not available')
        __glUnmapNamedBuffer_impl = __PYGL_FUNC_TYPE( c_char ,c_uint)(fptr)
    glUnmapNamedBuffer = __glUnmapNamedBuffer_impl
    return glUnmapNamedBuffer(buffer)
# <command>
#            <proto>void <name>glUseProgram</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#        </command>
#        
__glUseProgram_impl=None
def glUseProgram (program):
    global __glUseProgram_impl
    if not __glUseProgram_impl:
        fptr = __pyglGetFuncAddress('glUseProgram')
        if not fptr:
            raise RuntimeError('The function glUseProgram is not available')
        __glUseProgram_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glUseProgram = __glUseProgram_impl
    return glUseProgram(program)
# <command>
#            <proto>void <name>glUseProgramStages</name></proto>
#            <param><ptype>GLuint</ptype> <name>pipeline</name></param>
#            <param><ptype>GLbitfield</ptype> <name>stages</name></param>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#        </command>
#        
__glUseProgramStages_impl=None
def glUseProgramStages (pipeline, stages, program):
    global __glUseProgramStages_impl
    if not __glUseProgramStages_impl:
        fptr = __pyglGetFuncAddress('glUseProgramStages')
        if not fptr:
            raise RuntimeError('The function glUseProgramStages is not available')
        __glUseProgramStages_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glUseProgramStages = __glUseProgramStages_impl
    return glUseProgramStages(pipeline, stages, program)
# <command>
#            <proto>void <name>glValidateProgram</name></proto>
#            <param><ptype>GLuint</ptype> <name>program</name></param>
#        </command>
#        
__glValidateProgram_impl=None
def glValidateProgram (program):
    global __glValidateProgram_impl
    if not __glValidateProgram_impl:
        fptr = __pyglGetFuncAddress('glValidateProgram')
        if not fptr:
            raise RuntimeError('The function glValidateProgram is not available')
        __glValidateProgram_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glValidateProgram = __glValidateProgram_impl
    return glValidateProgram(program)
# <command>
#            <proto>void <name>glValidateProgramPipeline</name></proto>
#            <param><ptype>GLuint</ptype> <name>pipeline</name></param>
#        </command>
#        
__glValidateProgramPipeline_impl=None
def glValidateProgramPipeline (pipeline):
    global __glValidateProgramPipeline_impl
    if not __glValidateProgramPipeline_impl:
        fptr = __pyglGetFuncAddress('glValidateProgramPipeline')
        if not fptr:
            raise RuntimeError('The function glValidateProgramPipeline is not available')
        __glValidateProgramPipeline_impl = __PYGL_FUNC_TYPE( None ,c_uint)(fptr)
    glValidateProgramPipeline = __glValidateProgramPipeline_impl
    return glValidateProgramPipeline(pipeline)
# <command>
#            <proto>void <name>glVertexArrayAttribBinding</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>attribindex</name></param>
#            <param><ptype>GLuint</ptype> <name>bindingindex</name></param>
#        </command>
#        
__glVertexArrayAttribBinding_impl=None
def glVertexArrayAttribBinding (vaobj, attribindex, bindingindex):
    global __glVertexArrayAttribBinding_impl
    if not __glVertexArrayAttribBinding_impl:
        fptr = __pyglGetFuncAddress('glVertexArrayAttribBinding')
        if not fptr:
            raise RuntimeError('The function glVertexArrayAttribBinding is not available')
        __glVertexArrayAttribBinding_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glVertexArrayAttribBinding = __glVertexArrayAttribBinding_impl
    return glVertexArrayAttribBinding(vaobj, attribindex, bindingindex)
# <command>
#            <proto>void <name>glVertexArrayAttribFormat</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>attribindex</name></param>
#            <param><ptype>GLint</ptype> <name>size</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param><ptype>GLuint</ptype> <name>relativeoffset</name></param>
#        </command>
#        
__glVertexArrayAttribFormat_impl=None
def glVertexArrayAttribFormat (vaobj, attribindex, size, type, normalized, relativeoffset):
    global __glVertexArrayAttribFormat_impl
    if not __glVertexArrayAttribFormat_impl:
        fptr = __pyglGetFuncAddress('glVertexArrayAttribFormat')
        if not fptr:
            raise RuntimeError('The function glVertexArrayAttribFormat is not available')
        __glVertexArrayAttribFormat_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_uint, c_char, c_uint)(fptr)
    glVertexArrayAttribFormat = __glVertexArrayAttribFormat_impl
    return glVertexArrayAttribFormat(vaobj, attribindex, size, type, normalized, relativeoffset)
# <command>
#            <proto>void <name>glVertexArrayBindingDivisor</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>bindingindex</name></param>
#            <param><ptype>GLuint</ptype> <name>divisor</name></param>
#        </command>
#        
__glVertexArrayBindingDivisor_impl=None
def glVertexArrayBindingDivisor (vaobj, bindingindex, divisor):
    global __glVertexArrayBindingDivisor_impl
    if not __glVertexArrayBindingDivisor_impl:
        fptr = __pyglGetFuncAddress('glVertexArrayBindingDivisor')
        if not fptr:
            raise RuntimeError('The function glVertexArrayBindingDivisor is not available')
        __glVertexArrayBindingDivisor_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glVertexArrayBindingDivisor = __glVertexArrayBindingDivisor_impl
    return glVertexArrayBindingDivisor(vaobj, bindingindex, divisor)
# <command>
#            <proto>void <name>glVertexArrayElementBuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#        </command>
#        
__glVertexArrayElementBuffer_impl=None
def glVertexArrayElementBuffer (vaobj, buffer):
    global __glVertexArrayElementBuffer_impl
    if not __glVertexArrayElementBuffer_impl:
        fptr = __pyglGetFuncAddress('glVertexArrayElementBuffer')
        if not fptr:
            raise RuntimeError('The function glVertexArrayElementBuffer is not available')
        __glVertexArrayElementBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glVertexArrayElementBuffer = __glVertexArrayElementBuffer_impl
    return glVertexArrayElementBuffer(vaobj, buffer)
# <command>
#            <proto>void <name>glVertexArrayVertexBuffer</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>bindingindex</name></param>
#            <param><ptype>GLuint</ptype> <name>buffer</name></param>
#            <param><ptype>GLintptr</ptype> <name>offset</name></param>
#            <param><ptype>GLsizei</ptype> <name>stride</name></param>
#        </command>
#        
__glVertexArrayVertexBuffer_impl=None
def glVertexArrayVertexBuffer (vaobj, bindingindex, buffer, offset, stride):
    global __glVertexArrayVertexBuffer_impl
    if not __glVertexArrayVertexBuffer_impl:
        fptr = __pyglGetFuncAddress('glVertexArrayVertexBuffer')
        if not fptr:
            raise RuntimeError('The function glVertexArrayVertexBuffer is not available')
        __glVertexArrayVertexBuffer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_size_t, c_int)(fptr)
    glVertexArrayVertexBuffer = __glVertexArrayVertexBuffer_impl
    return glVertexArrayVertexBuffer(vaobj, bindingindex, buffer, offset, stride)
# <command>
#            <proto>void <name>glVertexArrayVertexBuffers</name></proto>
#            <param><ptype>GLuint</ptype> <name>vaobj</name></param>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param>const <ptype>GLuint</ptype> *<name>buffers</name></param>
#            <param>const <ptype>GLintptr</ptype> *<name>offsets</name></param>
#            <param>const <ptype>GLsizei</ptype> *<name>strides</name></param>
#        </command>
#        
__glVertexArrayVertexBuffers_impl=None
def glVertexArrayVertexBuffers (vaobj, first, count, buffers, offsets, strides):
    global __glVertexArrayVertexBuffers_impl
    if not __glVertexArrayVertexBuffers_impl:
        fptr = __pyglGetFuncAddress('glVertexArrayVertexBuffers')
        if not fptr:
            raise RuntimeError('The function glVertexArrayVertexBuffers is not available')
        __glVertexArrayVertexBuffers_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_int, c_void_p, c_void_p, c_void_p)(fptr)
    glVertexArrayVertexBuffers = (lambda vaobj,first,count,buffers,offsets,strides:__glVertexArrayVertexBuffers_impl(vaobj,first,count,__pyglGetAsConstVoidPointer( buffers ),__pyglGetAsConstVoidPointer( offsets ),__pyglGetAsConstVoidPointer( strides )))
    return glVertexArrayVertexBuffers(vaobj, first, count, buffers, offsets, strides)
# <command>
#            <proto>void <name>glVertexAttrib1d</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <vecequiv name="glVertexAttrib1dv" />
#        </command>
#        
__glVertexAttrib1d_impl=None
def glVertexAttrib1d (index, x):
    global __glVertexAttrib1d_impl
    if not __glVertexAttrib1d_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib1d')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib1d is not available')
        __glVertexAttrib1d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_double)(fptr)
    glVertexAttrib1d = __glVertexAttrib1d_impl
    return glVertexAttrib1d(index, x)
# <command>
#            <proto>void <name>glVertexAttrib1dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="1">const <ptype>GLdouble</ptype> *<name>v</name></param>
#            <glx opcode="4197" type="render" />
#        </command>
#        
__glVertexAttrib1dv_impl=None
def glVertexAttrib1dv (index, v):
    global __glVertexAttrib1dv_impl
    if not __glVertexAttrib1dv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib1dv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib1dv is not available')
        __glVertexAttrib1dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib1dv = (lambda index,v:__glVertexAttrib1dv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib1dv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib1f</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLfloat</ptype> <name>x</name></param>
#            <vecequiv name="glVertexAttrib1fv" />
#        </command>
#        
__glVertexAttrib1f_impl=None
def glVertexAttrib1f (index, x):
    global __glVertexAttrib1f_impl
    if not __glVertexAttrib1f_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib1f')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib1f is not available')
        __glVertexAttrib1f_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_float)(fptr)
    glVertexAttrib1f = __glVertexAttrib1f_impl
    return glVertexAttrib1f(index, x)
# <command>
#            <proto>void <name>glVertexAttrib1fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="1">const <ptype>GLfloat</ptype> *<name>v</name></param>
#            <glx opcode="4193" type="render" />
#        </command>
#        
__glVertexAttrib1fv_impl=None
def glVertexAttrib1fv (index, v):
    global __glVertexAttrib1fv_impl
    if not __glVertexAttrib1fv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib1fv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib1fv is not available')
        __glVertexAttrib1fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib1fv = (lambda index,v:__glVertexAttrib1fv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib1fv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib1s</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLshort</ptype> <name>x</name></param>
#            <vecequiv name="glVertexAttrib1sv" />
#        </command>
#        
__glVertexAttrib1s_impl=None
def glVertexAttrib1s (index, x):
    global __glVertexAttrib1s_impl
    if not __glVertexAttrib1s_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib1s')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib1s is not available')
        __glVertexAttrib1s_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_short)(fptr)
    glVertexAttrib1s = __glVertexAttrib1s_impl
    return glVertexAttrib1s(index, x)
# <command>
#            <proto>void <name>glVertexAttrib1sv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="1">const <ptype>GLshort</ptype> *<name>v</name></param>
#            <glx opcode="4189" type="render" />
#        </command>
#        
__glVertexAttrib1sv_impl=None
def glVertexAttrib1sv (index, v):
    global __glVertexAttrib1sv_impl
    if not __glVertexAttrib1sv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib1sv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib1sv is not available')
        __glVertexAttrib1sv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib1sv = (lambda index,v:__glVertexAttrib1sv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib1sv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib2d</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <param><ptype>GLdouble</ptype> <name>y</name></param>
#            <vecequiv name="glVertexAttrib2dv" />
#        </command>
#        
__glVertexAttrib2d_impl=None
def glVertexAttrib2d (index, x, y):
    global __glVertexAttrib2d_impl
    if not __glVertexAttrib2d_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib2d')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib2d is not available')
        __glVertexAttrib2d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_double, c_double)(fptr)
    glVertexAttrib2d = __glVertexAttrib2d_impl
    return glVertexAttrib2d(index, x, y)
# <command>
#            <proto>void <name>glVertexAttrib2dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="2">const <ptype>GLdouble</ptype> *<name>v</name></param>
#            <glx opcode="4198" type="render" />
#        </command>
#        
__glVertexAttrib2dv_impl=None
def glVertexAttrib2dv (index, v):
    global __glVertexAttrib2dv_impl
    if not __glVertexAttrib2dv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib2dv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib2dv is not available')
        __glVertexAttrib2dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib2dv = (lambda index,v:__glVertexAttrib2dv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib2dv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib2f</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLfloat</ptype> <name>x</name></param>
#            <param><ptype>GLfloat</ptype> <name>y</name></param>
#            <vecequiv name="glVertexAttrib2fv" />
#        </command>
#        
__glVertexAttrib2f_impl=None
def glVertexAttrib2f (index, x, y):
    global __glVertexAttrib2f_impl
    if not __glVertexAttrib2f_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib2f')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib2f is not available')
        __glVertexAttrib2f_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_float, c_float)(fptr)
    glVertexAttrib2f = __glVertexAttrib2f_impl
    return glVertexAttrib2f(index, x, y)
# <command>
#            <proto>void <name>glVertexAttrib2fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="2">const <ptype>GLfloat</ptype> *<name>v</name></param>
#            <glx opcode="4194" type="render" />
#        </command>
#        
__glVertexAttrib2fv_impl=None
def glVertexAttrib2fv (index, v):
    global __glVertexAttrib2fv_impl
    if not __glVertexAttrib2fv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib2fv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib2fv is not available')
        __glVertexAttrib2fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib2fv = (lambda index,v:__glVertexAttrib2fv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib2fv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib2s</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLshort</ptype> <name>x</name></param>
#            <param><ptype>GLshort</ptype> <name>y</name></param>
#            <vecequiv name="glVertexAttrib2sv" />
#        </command>
#        
__glVertexAttrib2s_impl=None
def glVertexAttrib2s (index, x, y):
    global __glVertexAttrib2s_impl
    if not __glVertexAttrib2s_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib2s')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib2s is not available')
        __glVertexAttrib2s_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_short, c_short)(fptr)
    glVertexAttrib2s = __glVertexAttrib2s_impl
    return glVertexAttrib2s(index, x, y)
# <command>
#            <proto>void <name>glVertexAttrib2sv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="2">const <ptype>GLshort</ptype> *<name>v</name></param>
#            <glx opcode="4190" type="render" />
#        </command>
#        
__glVertexAttrib2sv_impl=None
def glVertexAttrib2sv (index, v):
    global __glVertexAttrib2sv_impl
    if not __glVertexAttrib2sv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib2sv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib2sv is not available')
        __glVertexAttrib2sv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib2sv = (lambda index,v:__glVertexAttrib2sv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib2sv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib3d</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <param><ptype>GLdouble</ptype> <name>y</name></param>
#            <param><ptype>GLdouble</ptype> <name>z</name></param>
#            <vecequiv name="glVertexAttrib3dv" />
#        </command>
#        
__glVertexAttrib3d_impl=None
def glVertexAttrib3d (index, x, y, z):
    global __glVertexAttrib3d_impl
    if not __glVertexAttrib3d_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib3d')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib3d is not available')
        __glVertexAttrib3d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_double, c_double, c_double)(fptr)
    glVertexAttrib3d = __glVertexAttrib3d_impl
    return glVertexAttrib3d(index, x, y, z)
# <command>
#            <proto>void <name>glVertexAttrib3dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="3">const <ptype>GLdouble</ptype> *<name>v</name></param>
#            <glx opcode="4199" type="render" />
#        </command>
#        
__glVertexAttrib3dv_impl=None
def glVertexAttrib3dv (index, v):
    global __glVertexAttrib3dv_impl
    if not __glVertexAttrib3dv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib3dv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib3dv is not available')
        __glVertexAttrib3dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib3dv = (lambda index,v:__glVertexAttrib3dv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib3dv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib3f</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLfloat</ptype> <name>x</name></param>
#            <param><ptype>GLfloat</ptype> <name>y</name></param>
#            <param><ptype>GLfloat</ptype> <name>z</name></param>
#            <vecequiv name="glVertexAttrib3fv" />
#        </command>
#        
__glVertexAttrib3f_impl=None
def glVertexAttrib3f (index, x, y, z):
    global __glVertexAttrib3f_impl
    if not __glVertexAttrib3f_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib3f')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib3f is not available')
        __glVertexAttrib3f_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_float, c_float, c_float)(fptr)
    glVertexAttrib3f = __glVertexAttrib3f_impl
    return glVertexAttrib3f(index, x, y, z)
# <command>
#            <proto>void <name>glVertexAttrib3fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="3">const <ptype>GLfloat</ptype> *<name>v</name></param>
#            <glx opcode="4195" type="render" />
#        </command>
#        
__glVertexAttrib3fv_impl=None
def glVertexAttrib3fv (index, v):
    global __glVertexAttrib3fv_impl
    if not __glVertexAttrib3fv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib3fv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib3fv is not available')
        __glVertexAttrib3fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib3fv = (lambda index,v:__glVertexAttrib3fv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib3fv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib3s</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLshort</ptype> <name>x</name></param>
#            <param><ptype>GLshort</ptype> <name>y</name></param>
#            <param><ptype>GLshort</ptype> <name>z</name></param>
#            <vecequiv name="glVertexAttrib3sv" />
#        </command>
#        
__glVertexAttrib3s_impl=None
def glVertexAttrib3s (index, x, y, z):
    global __glVertexAttrib3s_impl
    if not __glVertexAttrib3s_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib3s')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib3s is not available')
        __glVertexAttrib3s_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_short, c_short, c_short)(fptr)
    glVertexAttrib3s = __glVertexAttrib3s_impl
    return glVertexAttrib3s(index, x, y, z)
# <command>
#            <proto>void <name>glVertexAttrib3sv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="3">const <ptype>GLshort</ptype> *<name>v</name></param>
#            <glx opcode="4191" type="render" />
#        </command>
#        
__glVertexAttrib3sv_impl=None
def glVertexAttrib3sv (index, v):
    global __glVertexAttrib3sv_impl
    if not __glVertexAttrib3sv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib3sv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib3sv is not available')
        __glVertexAttrib3sv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib3sv = (lambda index,v:__glVertexAttrib3sv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib3sv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4Nbv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLbyte</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4Nbv_impl=None
def glVertexAttrib4Nbv (index, v):
    global __glVertexAttrib4Nbv_impl
    if not __glVertexAttrib4Nbv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4Nbv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4Nbv is not available')
        __glVertexAttrib4Nbv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4Nbv = (lambda index,v:__glVertexAttrib4Nbv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4Nbv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4Niv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4Niv_impl=None
def glVertexAttrib4Niv (index, v):
    global __glVertexAttrib4Niv_impl
    if not __glVertexAttrib4Niv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4Niv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4Niv is not available')
        __glVertexAttrib4Niv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4Niv = (lambda index,v:__glVertexAttrib4Niv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4Niv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4Nsv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLshort</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4Nsv_impl=None
def glVertexAttrib4Nsv (index, v):
    global __glVertexAttrib4Nsv_impl
    if not __glVertexAttrib4Nsv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4Nsv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4Nsv is not available')
        __glVertexAttrib4Nsv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4Nsv = (lambda index,v:__glVertexAttrib4Nsv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4Nsv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4Nub</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLubyte</ptype> <name>x</name></param>
#            <param><ptype>GLubyte</ptype> <name>y</name></param>
#            <param><ptype>GLubyte</ptype> <name>z</name></param>
#            <param><ptype>GLubyte</ptype> <name>w</name></param>
#        </command>
#        
__glVertexAttrib4Nub_impl=None
def glVertexAttrib4Nub (index, x, y, z, w):
    global __glVertexAttrib4Nub_impl
    if not __glVertexAttrib4Nub_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4Nub')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4Nub is not available')
        __glVertexAttrib4Nub_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_ubyte, c_ubyte, c_ubyte, c_ubyte)(fptr)
    glVertexAttrib4Nub = __glVertexAttrib4Nub_impl
    return glVertexAttrib4Nub(index, x, y, z, w)
# <command>
#            <proto>void <name>glVertexAttrib4Nubv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLubyte</ptype> *<name>v</name></param>
#            <glx opcode="4201" type="render" />
#        </command>
#        
__glVertexAttrib4Nubv_impl=None
def glVertexAttrib4Nubv (index, v):
    global __glVertexAttrib4Nubv_impl
    if not __glVertexAttrib4Nubv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4Nubv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4Nubv is not available')
        __glVertexAttrib4Nubv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_char_p)(fptr)
    glVertexAttrib4Nubv = (lambda index,v:__glVertexAttrib4Nubv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4Nubv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4Nuiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLuint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4Nuiv_impl=None
def glVertexAttrib4Nuiv (index, v):
    global __glVertexAttrib4Nuiv_impl
    if not __glVertexAttrib4Nuiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4Nuiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4Nuiv is not available')
        __glVertexAttrib4Nuiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4Nuiv = (lambda index,v:__glVertexAttrib4Nuiv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4Nuiv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4Nusv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLushort</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4Nusv_impl=None
def glVertexAttrib4Nusv (index, v):
    global __glVertexAttrib4Nusv_impl
    if not __glVertexAttrib4Nusv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4Nusv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4Nusv is not available')
        __glVertexAttrib4Nusv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4Nusv = (lambda index,v:__glVertexAttrib4Nusv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4Nusv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4bv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLbyte</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4bv_impl=None
def glVertexAttrib4bv (index, v):
    global __glVertexAttrib4bv_impl
    if not __glVertexAttrib4bv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4bv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4bv is not available')
        __glVertexAttrib4bv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4bv = (lambda index,v:__glVertexAttrib4bv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4bv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4d</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <param><ptype>GLdouble</ptype> <name>y</name></param>
#            <param><ptype>GLdouble</ptype> <name>z</name></param>
#            <param><ptype>GLdouble</ptype> <name>w</name></param>
#            <vecequiv name="glVertexAttrib4dv" />
#        </command>
#        
__glVertexAttrib4d_impl=None
def glVertexAttrib4d (index, x, y, z, w):
    global __glVertexAttrib4d_impl
    if not __glVertexAttrib4d_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4d')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4d is not available')
        __glVertexAttrib4d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_double, c_double, c_double, c_double)(fptr)
    glVertexAttrib4d = __glVertexAttrib4d_impl
    return glVertexAttrib4d(index, x, y, z, w)
# <command>
#            <proto>void <name>glVertexAttrib4dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLdouble</ptype> *<name>v</name></param>
#            <glx opcode="4200" type="render" />
#        </command>
#        
__glVertexAttrib4dv_impl=None
def glVertexAttrib4dv (index, v):
    global __glVertexAttrib4dv_impl
    if not __glVertexAttrib4dv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4dv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4dv is not available')
        __glVertexAttrib4dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4dv = (lambda index,v:__glVertexAttrib4dv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4dv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4f</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLfloat</ptype> <name>x</name></param>
#            <param><ptype>GLfloat</ptype> <name>y</name></param>
#            <param><ptype>GLfloat</ptype> <name>z</name></param>
#            <param><ptype>GLfloat</ptype> <name>w</name></param>
#            <vecequiv name="glVertexAttrib4fv" />
#        </command>
#        
__glVertexAttrib4f_impl=None
def glVertexAttrib4f (index, x, y, z, w):
    global __glVertexAttrib4f_impl
    if not __glVertexAttrib4f_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4f')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4f is not available')
        __glVertexAttrib4f_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_float, c_float, c_float, c_float)(fptr)
    glVertexAttrib4f = __glVertexAttrib4f_impl
    return glVertexAttrib4f(index, x, y, z, w)
# <command>
#            <proto>void <name>glVertexAttrib4fv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLfloat</ptype> *<name>v</name></param>
#            <glx opcode="4196" type="render" />
#        </command>
#        
__glVertexAttrib4fv_impl=None
def glVertexAttrib4fv (index, v):
    global __glVertexAttrib4fv_impl
    if not __glVertexAttrib4fv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4fv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4fv is not available')
        __glVertexAttrib4fv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4fv = (lambda index,v:__glVertexAttrib4fv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4fv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4iv_impl=None
def glVertexAttrib4iv (index, v):
    global __glVertexAttrib4iv_impl
    if not __glVertexAttrib4iv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4iv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4iv is not available')
        __glVertexAttrib4iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4iv = (lambda index,v:__glVertexAttrib4iv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4iv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4s</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLshort</ptype> <name>x</name></param>
#            <param><ptype>GLshort</ptype> <name>y</name></param>
#            <param><ptype>GLshort</ptype> <name>z</name></param>
#            <param><ptype>GLshort</ptype> <name>w</name></param>
#            <vecequiv name="glVertexAttrib4sv" />
#        </command>
#        
__glVertexAttrib4s_impl=None
def glVertexAttrib4s (index, x, y, z, w):
    global __glVertexAttrib4s_impl
    if not __glVertexAttrib4s_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4s')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4s is not available')
        __glVertexAttrib4s_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_short, c_short, c_short, c_short)(fptr)
    glVertexAttrib4s = __glVertexAttrib4s_impl
    return glVertexAttrib4s(index, x, y, z, w)
# <command>
#            <proto>void <name>glVertexAttrib4sv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLshort</ptype> *<name>v</name></param>
#            <glx opcode="4192" type="render" />
#        </command>
#        
__glVertexAttrib4sv_impl=None
def glVertexAttrib4sv (index, v):
    global __glVertexAttrib4sv_impl
    if not __glVertexAttrib4sv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4sv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4sv is not available')
        __glVertexAttrib4sv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4sv = (lambda index,v:__glVertexAttrib4sv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4sv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4ubv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLubyte</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4ubv_impl=None
def glVertexAttrib4ubv (index, v):
    global __glVertexAttrib4ubv_impl
    if not __glVertexAttrib4ubv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4ubv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4ubv is not available')
        __glVertexAttrib4ubv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_char_p)(fptr)
    glVertexAttrib4ubv = (lambda index,v:__glVertexAttrib4ubv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4ubv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLuint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4uiv_impl=None
def glVertexAttrib4uiv (index, v):
    global __glVertexAttrib4uiv_impl
    if not __glVertexAttrib4uiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4uiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4uiv is not available')
        __glVertexAttrib4uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4uiv = (lambda index,v:__glVertexAttrib4uiv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4uiv(index, v)
# <command>
#            <proto>void <name>glVertexAttrib4usv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLushort</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttrib4usv_impl=None
def glVertexAttrib4usv (index, v):
    global __glVertexAttrib4usv_impl
    if not __glVertexAttrib4usv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttrib4usv')
        if not fptr:
            raise RuntimeError('The function glVertexAttrib4usv is not available')
        __glVertexAttrib4usv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttrib4usv = (lambda index,v:__glVertexAttrib4usv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttrib4usv(index, v)
# <command>
#            <proto>void <name>glVertexAttribBinding</name></proto>
#            <param><ptype>GLuint</ptype> <name>attribindex</name></param>
#            <param><ptype>GLuint</ptype> <name>bindingindex</name></param>
#        </command>
#        
__glVertexAttribBinding_impl=None
def glVertexAttribBinding (attribindex, bindingindex):
    global __glVertexAttribBinding_impl
    if not __glVertexAttribBinding_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribBinding')
        if not fptr:
            raise RuntimeError('The function glVertexAttribBinding is not available')
        __glVertexAttribBinding_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glVertexAttribBinding = __glVertexAttribBinding_impl
    return glVertexAttribBinding(attribindex, bindingindex)
# <command>
#            <proto>void <name>glVertexAttribDivisor</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>divisor</name></param>
#        </command>
#        
__glVertexAttribDivisor_impl=None
def glVertexAttribDivisor (index, divisor):
    global __glVertexAttribDivisor_impl
    if not __glVertexAttribDivisor_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribDivisor')
        if not fptr:
            raise RuntimeError('The function glVertexAttribDivisor is not available')
        __glVertexAttribDivisor_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glVertexAttribDivisor = __glVertexAttribDivisor_impl
    return glVertexAttribDivisor(index, divisor)
# <command>
#            <proto>void <name>glVertexAttribFormat</name></proto>
#            <param><ptype>GLuint</ptype> <name>attribindex</name></param>
#            <param><ptype>GLint</ptype> <name>size</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param><ptype>GLuint</ptype> <name>relativeoffset</name></param>
#        </command>
#        
__glVertexAttribFormat_impl=None
def glVertexAttribFormat (attribindex, size, type, normalized, relativeoffset):
    global __glVertexAttribFormat_impl
    if not __glVertexAttribFormat_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribFormat')
        if not fptr:
            raise RuntimeError('The function glVertexAttribFormat is not available')
        __glVertexAttribFormat_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_char, c_uint)(fptr)
    glVertexAttribFormat = __glVertexAttribFormat_impl
    return glVertexAttribFormat(attribindex, size, type, normalized, relativeoffset)
# <command>
#            <proto>void <name>glVertexAttribI1i</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <vecequiv name="glVertexAttribI1iv" />
#        </command>
#        
__glVertexAttribI1i_impl=None
def glVertexAttribI1i (index, x):
    global __glVertexAttribI1i_impl
    if not __glVertexAttribI1i_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI1i')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI1i is not available')
        __glVertexAttribI1i_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int)(fptr)
    glVertexAttribI1i = __glVertexAttribI1i_impl
    return glVertexAttribI1i(index, x)
# <command>
#            <proto>void <name>glVertexAttribI1iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="1">const <ptype>GLint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI1iv_impl=None
def glVertexAttribI1iv (index, v):
    global __glVertexAttribI1iv_impl
    if not __glVertexAttribI1iv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI1iv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI1iv is not available')
        __glVertexAttribI1iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI1iv = (lambda index,v:__glVertexAttribI1iv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI1iv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI1ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>x</name></param>
#            <vecequiv name="glVertexAttribI1uiv" />
#        </command>
#        
__glVertexAttribI1ui_impl=None
def glVertexAttribI1ui (index, x):
    global __glVertexAttribI1ui_impl
    if not __glVertexAttribI1ui_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI1ui')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI1ui is not available')
        __glVertexAttribI1ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glVertexAttribI1ui = __glVertexAttribI1ui_impl
    return glVertexAttribI1ui(index, x)
# <command>
#            <proto>void <name>glVertexAttribI1uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="1">const <ptype>GLuint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI1uiv_impl=None
def glVertexAttribI1uiv (index, v):
    global __glVertexAttribI1uiv_impl
    if not __glVertexAttribI1uiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI1uiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI1uiv is not available')
        __glVertexAttribI1uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI1uiv = (lambda index,v:__glVertexAttribI1uiv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI1uiv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI2i</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <param><ptype>GLint</ptype> <name>y</name></param>
#            <vecequiv name="glVertexAttribI2iv" />
#        </command>
#        
__glVertexAttribI2i_impl=None
def glVertexAttribI2i (index, x, y):
    global __glVertexAttribI2i_impl
    if not __glVertexAttribI2i_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI2i')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI2i is not available')
        __glVertexAttribI2i_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int)(fptr)
    glVertexAttribI2i = __glVertexAttribI2i_impl
    return glVertexAttribI2i(index, x, y)
# <command>
#            <proto>void <name>glVertexAttribI2iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="2">const <ptype>GLint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI2iv_impl=None
def glVertexAttribI2iv (index, v):
    global __glVertexAttribI2iv_impl
    if not __glVertexAttribI2iv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI2iv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI2iv is not available')
        __glVertexAttribI2iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI2iv = (lambda index,v:__glVertexAttribI2iv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI2iv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI2ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>x</name></param>
#            <param><ptype>GLuint</ptype> <name>y</name></param>
#            <vecequiv name="glVertexAttribI2uiv" />
#        </command>
#        
__glVertexAttribI2ui_impl=None
def glVertexAttribI2ui (index, x, y):
    global __glVertexAttribI2ui_impl
    if not __glVertexAttribI2ui_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI2ui')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI2ui is not available')
        __glVertexAttribI2ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint)(fptr)
    glVertexAttribI2ui = __glVertexAttribI2ui_impl
    return glVertexAttribI2ui(index, x, y)
# <command>
#            <proto>void <name>glVertexAttribI2uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="2">const <ptype>GLuint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI2uiv_impl=None
def glVertexAttribI2uiv (index, v):
    global __glVertexAttribI2uiv_impl
    if not __glVertexAttribI2uiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI2uiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI2uiv is not available')
        __glVertexAttribI2uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI2uiv = (lambda index,v:__glVertexAttribI2uiv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI2uiv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI3i</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <param><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLint</ptype> <name>z</name></param>
#            <vecequiv name="glVertexAttribI3iv" />
#        </command>
#        
__glVertexAttribI3i_impl=None
def glVertexAttribI3i (index, x, y, z):
    global __glVertexAttribI3i_impl
    if not __glVertexAttribI3i_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI3i')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI3i is not available')
        __glVertexAttribI3i_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int)(fptr)
    glVertexAttribI3i = __glVertexAttribI3i_impl
    return glVertexAttribI3i(index, x, y, z)
# <command>
#            <proto>void <name>glVertexAttribI3iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="3">const <ptype>GLint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI3iv_impl=None
def glVertexAttribI3iv (index, v):
    global __glVertexAttribI3iv_impl
    if not __glVertexAttribI3iv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI3iv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI3iv is not available')
        __glVertexAttribI3iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI3iv = (lambda index,v:__glVertexAttribI3iv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI3iv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI3ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>x</name></param>
#            <param><ptype>GLuint</ptype> <name>y</name></param>
#            <param><ptype>GLuint</ptype> <name>z</name></param>
#            <vecequiv name="glVertexAttribI3uiv" />
#        </command>
#        
__glVertexAttribI3ui_impl=None
def glVertexAttribI3ui (index, x, y, z):
    global __glVertexAttribI3ui_impl
    if not __glVertexAttribI3ui_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI3ui')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI3ui is not available')
        __glVertexAttribI3ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint)(fptr)
    glVertexAttribI3ui = __glVertexAttribI3ui_impl
    return glVertexAttribI3ui(index, x, y, z)
# <command>
#            <proto>void <name>glVertexAttribI3uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="3">const <ptype>GLuint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI3uiv_impl=None
def glVertexAttribI3uiv (index, v):
    global __glVertexAttribI3uiv_impl
    if not __glVertexAttribI3uiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI3uiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI3uiv is not available')
        __glVertexAttribI3uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI3uiv = (lambda index,v:__glVertexAttribI3uiv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI3uiv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI4bv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLbyte</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI4bv_impl=None
def glVertexAttribI4bv (index, v):
    global __glVertexAttribI4bv_impl
    if not __glVertexAttribI4bv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI4bv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI4bv is not available')
        __glVertexAttribI4bv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI4bv = (lambda index,v:__glVertexAttribI4bv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI4bv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI4i</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLint</ptype> <name>x</name></param>
#            <param><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLint</ptype> <name>z</name></param>
#            <param><ptype>GLint</ptype> <name>w</name></param>
#            <vecequiv name="glVertexAttribI4iv" />
#        </command>
#        
__glVertexAttribI4i_impl=None
def glVertexAttribI4i (index, x, y, z, w):
    global __glVertexAttribI4i_impl
    if not __glVertexAttribI4i_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI4i')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI4i is not available')
        __glVertexAttribI4i_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_int, c_int, c_int)(fptr)
    glVertexAttribI4i = __glVertexAttribI4i_impl
    return glVertexAttribI4i(index, x, y, z, w)
# <command>
#            <proto>void <name>glVertexAttribI4iv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI4iv_impl=None
def glVertexAttribI4iv (index, v):
    global __glVertexAttribI4iv_impl
    if not __glVertexAttribI4iv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI4iv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI4iv is not available')
        __glVertexAttribI4iv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI4iv = (lambda index,v:__glVertexAttribI4iv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI4iv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI4sv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLshort</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI4sv_impl=None
def glVertexAttribI4sv (index, v):
    global __glVertexAttribI4sv_impl
    if not __glVertexAttribI4sv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI4sv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI4sv is not available')
        __glVertexAttribI4sv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI4sv = (lambda index,v:__glVertexAttribI4sv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI4sv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI4ubv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLubyte</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI4ubv_impl=None
def glVertexAttribI4ubv (index, v):
    global __glVertexAttribI4ubv_impl
    if not __glVertexAttribI4ubv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI4ubv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI4ubv is not available')
        __glVertexAttribI4ubv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_char_p)(fptr)
    glVertexAttribI4ubv = (lambda index,v:__glVertexAttribI4ubv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI4ubv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI4ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLuint</ptype> <name>x</name></param>
#            <param><ptype>GLuint</ptype> <name>y</name></param>
#            <param><ptype>GLuint</ptype> <name>z</name></param>
#            <param><ptype>GLuint</ptype> <name>w</name></param>
#            <vecequiv name="glVertexAttribI4uiv" />
#        </command>
#        
__glVertexAttribI4ui_impl=None
def glVertexAttribI4ui (index, x, y, z, w):
    global __glVertexAttribI4ui_impl
    if not __glVertexAttribI4ui_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI4ui')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI4ui is not available')
        __glVertexAttribI4ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_uint, c_uint, c_uint)(fptr)
    glVertexAttribI4ui = __glVertexAttribI4ui_impl
    return glVertexAttribI4ui(index, x, y, z, w)
# <command>
#            <proto>void <name>glVertexAttribI4uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLuint</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI4uiv_impl=None
def glVertexAttribI4uiv (index, v):
    global __glVertexAttribI4uiv_impl
    if not __glVertexAttribI4uiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI4uiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI4uiv is not available')
        __glVertexAttribI4uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI4uiv = (lambda index,v:__glVertexAttribI4uiv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI4uiv(index, v)
# <command>
#            <proto>void <name>glVertexAttribI4usv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLushort</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribI4usv_impl=None
def glVertexAttribI4usv (index, v):
    global __glVertexAttribI4usv_impl
    if not __glVertexAttribI4usv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribI4usv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribI4usv is not available')
        __glVertexAttribI4usv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribI4usv = (lambda index,v:__glVertexAttribI4usv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribI4usv(index, v)
# <command>
#            <proto>void <name>glVertexAttribL1d</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#        </command>
#        
__glVertexAttribL1d_impl=None
def glVertexAttribL1d (index, x):
    global __glVertexAttribL1d_impl
    if not __glVertexAttribL1d_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribL1d')
        if not fptr:
            raise RuntimeError('The function glVertexAttribL1d is not available')
        __glVertexAttribL1d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_double)(fptr)
    glVertexAttribL1d = __glVertexAttribL1d_impl
    return glVertexAttribL1d(index, x)
# <command>
#            <proto>void <name>glVertexAttribL1dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="1">const <ptype>GLdouble</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribL1dv_impl=None
def glVertexAttribL1dv (index, v):
    global __glVertexAttribL1dv_impl
    if not __glVertexAttribL1dv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribL1dv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribL1dv is not available')
        __glVertexAttribL1dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribL1dv = (lambda index,v:__glVertexAttribL1dv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribL1dv(index, v)
# <command>
#            <proto>void <name>glVertexAttribL2d</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <param><ptype>GLdouble</ptype> <name>y</name></param>
#        </command>
#        
__glVertexAttribL2d_impl=None
def glVertexAttribL2d (index, x, y):
    global __glVertexAttribL2d_impl
    if not __glVertexAttribL2d_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribL2d')
        if not fptr:
            raise RuntimeError('The function glVertexAttribL2d is not available')
        __glVertexAttribL2d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_double, c_double)(fptr)
    glVertexAttribL2d = __glVertexAttribL2d_impl
    return glVertexAttribL2d(index, x, y)
# <command>
#            <proto>void <name>glVertexAttribL2dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="2">const <ptype>GLdouble</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribL2dv_impl=None
def glVertexAttribL2dv (index, v):
    global __glVertexAttribL2dv_impl
    if not __glVertexAttribL2dv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribL2dv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribL2dv is not available')
        __glVertexAttribL2dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribL2dv = (lambda index,v:__glVertexAttribL2dv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribL2dv(index, v)
# <command>
#            <proto>void <name>glVertexAttribL3d</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <param><ptype>GLdouble</ptype> <name>y</name></param>
#            <param><ptype>GLdouble</ptype> <name>z</name></param>
#        </command>
#        
__glVertexAttribL3d_impl=None
def glVertexAttribL3d (index, x, y, z):
    global __glVertexAttribL3d_impl
    if not __glVertexAttribL3d_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribL3d')
        if not fptr:
            raise RuntimeError('The function glVertexAttribL3d is not available')
        __glVertexAttribL3d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_double, c_double, c_double)(fptr)
    glVertexAttribL3d = __glVertexAttribL3d_impl
    return glVertexAttribL3d(index, x, y, z)
# <command>
#            <proto>void <name>glVertexAttribL3dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="3">const <ptype>GLdouble</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribL3dv_impl=None
def glVertexAttribL3dv (index, v):
    global __glVertexAttribL3dv_impl
    if not __glVertexAttribL3dv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribL3dv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribL3dv is not available')
        __glVertexAttribL3dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribL3dv = (lambda index,v:__glVertexAttribL3dv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribL3dv(index, v)
# <command>
#            <proto>void <name>glVertexAttribL4d</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLdouble</ptype> <name>x</name></param>
#            <param><ptype>GLdouble</ptype> <name>y</name></param>
#            <param><ptype>GLdouble</ptype> <name>z</name></param>
#            <param><ptype>GLdouble</ptype> <name>w</name></param>
#        </command>
#        
__glVertexAttribL4d_impl=None
def glVertexAttribL4d (index, x, y, z, w):
    global __glVertexAttribL4d_impl
    if not __glVertexAttribL4d_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribL4d')
        if not fptr:
            raise RuntimeError('The function glVertexAttribL4d is not available')
        __glVertexAttribL4d_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_double, c_double, c_double, c_double)(fptr)
    glVertexAttribL4d = __glVertexAttribL4d_impl
    return glVertexAttribL4d(index, x, y, z, w)
# <command>
#            <proto>void <name>glVertexAttribL4dv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLdouble</ptype> *<name>v</name></param>
#        </command>
#        
__glVertexAttribL4dv_impl=None
def glVertexAttribL4dv (index, v):
    global __glVertexAttribL4dv_impl
    if not __glVertexAttribL4dv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribL4dv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribL4dv is not available')
        __glVertexAttribL4dv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glVertexAttribL4dv = (lambda index,v:__glVertexAttribL4dv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glVertexAttribL4dv(index, v)
# <command>
#            <proto>void <name>glVertexAttribP1ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param><ptype>GLuint</ptype> <name>value</name></param>
#        </command>
#        
__glVertexAttribP1ui_impl=None
def glVertexAttribP1ui (index, type, normalized, value):
    global __glVertexAttribP1ui_impl
    if not __glVertexAttribP1ui_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribP1ui')
        if not fptr:
            raise RuntimeError('The function glVertexAttribP1ui is not available')
        __glVertexAttribP1ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_char, c_uint)(fptr)
    glVertexAttribP1ui = __glVertexAttribP1ui_impl
    return glVertexAttribP1ui(index, type, normalized, value)
# <command>
#            <proto>void <name>glVertexAttribP1uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param len="1">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glVertexAttribP1uiv_impl=None
def glVertexAttribP1uiv (index, type, normalized, value):
    global __glVertexAttribP1uiv_impl
    if not __glVertexAttribP1uiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribP1uiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribP1uiv is not available')
        __glVertexAttribP1uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_char, c_void_p)(fptr)
    glVertexAttribP1uiv = (lambda index,type,normalized,value:__glVertexAttribP1uiv_impl(index,type,normalized,__pyglGetAsConstVoidPointer( value )))
    return glVertexAttribP1uiv(index, type, normalized, value)
# <command>
#            <proto>void <name>glVertexAttribP2ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param><ptype>GLuint</ptype> <name>value</name></param>
#        </command>
#        
__glVertexAttribP2ui_impl=None
def glVertexAttribP2ui (index, type, normalized, value):
    global __glVertexAttribP2ui_impl
    if not __glVertexAttribP2ui_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribP2ui')
        if not fptr:
            raise RuntimeError('The function glVertexAttribP2ui is not available')
        __glVertexAttribP2ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_char, c_uint)(fptr)
    glVertexAttribP2ui = __glVertexAttribP2ui_impl
    return glVertexAttribP2ui(index, type, normalized, value)
# <command>
#            <proto>void <name>glVertexAttribP2uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param len="1">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glVertexAttribP2uiv_impl=None
def glVertexAttribP2uiv (index, type, normalized, value):
    global __glVertexAttribP2uiv_impl
    if not __glVertexAttribP2uiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribP2uiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribP2uiv is not available')
        __glVertexAttribP2uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_char, c_void_p)(fptr)
    glVertexAttribP2uiv = (lambda index,type,normalized,value:__glVertexAttribP2uiv_impl(index,type,normalized,__pyglGetAsConstVoidPointer( value )))
    return glVertexAttribP2uiv(index, type, normalized, value)
# <command>
#            <proto>void <name>glVertexAttribP3ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param><ptype>GLuint</ptype> <name>value</name></param>
#        </command>
#        
__glVertexAttribP3ui_impl=None
def glVertexAttribP3ui (index, type, normalized, value):
    global __glVertexAttribP3ui_impl
    if not __glVertexAttribP3ui_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribP3ui')
        if not fptr:
            raise RuntimeError('The function glVertexAttribP3ui is not available')
        __glVertexAttribP3ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_char, c_uint)(fptr)
    glVertexAttribP3ui = __glVertexAttribP3ui_impl
    return glVertexAttribP3ui(index, type, normalized, value)
# <command>
#            <proto>void <name>glVertexAttribP3uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param len="1">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glVertexAttribP3uiv_impl=None
def glVertexAttribP3uiv (index, type, normalized, value):
    global __glVertexAttribP3uiv_impl
    if not __glVertexAttribP3uiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribP3uiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribP3uiv is not available')
        __glVertexAttribP3uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_char, c_void_p)(fptr)
    glVertexAttribP3uiv = (lambda index,type,normalized,value:__glVertexAttribP3uiv_impl(index,type,normalized,__pyglGetAsConstVoidPointer( value )))
    return glVertexAttribP3uiv(index, type, normalized, value)
# <command>
#            <proto>void <name>glVertexAttribP4ui</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param><ptype>GLuint</ptype> <name>value</name></param>
#        </command>
#        
__glVertexAttribP4ui_impl=None
def glVertexAttribP4ui (index, type, normalized, value):
    global __glVertexAttribP4ui_impl
    if not __glVertexAttribP4ui_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribP4ui')
        if not fptr:
            raise RuntimeError('The function glVertexAttribP4ui is not available')
        __glVertexAttribP4ui_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_char, c_uint)(fptr)
    glVertexAttribP4ui = __glVertexAttribP4ui_impl
    return glVertexAttribP4ui(index, type, normalized, value)
# <command>
#            <proto>void <name>glVertexAttribP4uiv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param len="1">const <ptype>GLuint</ptype> *<name>value</name></param>
#        </command>
#        
__glVertexAttribP4uiv_impl=None
def glVertexAttribP4uiv (index, type, normalized, value):
    global __glVertexAttribP4uiv_impl
    if not __glVertexAttribP4uiv_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribP4uiv')
        if not fptr:
            raise RuntimeError('The function glVertexAttribP4uiv is not available')
        __glVertexAttribP4uiv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint, c_char, c_void_p)(fptr)
    glVertexAttribP4uiv = (lambda index,type,normalized,value:__glVertexAttribP4uiv_impl(index,type,normalized,__pyglGetAsConstVoidPointer( value )))
    return glVertexAttribP4uiv(index, type, normalized, value)
# <command>
#            <proto>void <name>glVertexAttribPointer</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLint</ptype> <name>size</name></param>
#            <param group="VertexAttribPointerType"><ptype>GLenum</ptype> <name>type</name></param>
#            <param group="Boolean"><ptype>GLboolean</ptype> <name>normalized</name></param>
#            <param><ptype>GLsizei</ptype> <name>stride</name></param>
#            <param len="COMPSIZE(size,type,stride)">const void *<name>pointer</name></param>
#        </command>
#        
__glVertexAttribPointer_impl=None
def glVertexAttribPointer (index, size, type, normalized, stride, pointer):
    global __glVertexAttribPointer_impl
    if not __glVertexAttribPointer_impl:
        fptr = __pyglGetFuncAddress('glVertexAttribPointer')
        if not fptr:
            raise RuntimeError('The function glVertexAttribPointer is not available')
        __glVertexAttribPointer_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_uint, c_char, c_int, c_void_p)(fptr)
    glVertexAttribPointer = __glVertexAttribPointer_impl
    return glVertexAttribPointer(index, size, type, normalized, stride, pointer)
# <command>
#            <proto>void <name>glVertexBindingDivisor</name></proto>
#            <param><ptype>GLuint</ptype> <name>bindingindex</name></param>
#            <param><ptype>GLuint</ptype> <name>divisor</name></param>
#        </command>
#        
__glVertexBindingDivisor_impl=None
def glVertexBindingDivisor (bindingindex, divisor):
    global __glVertexBindingDivisor_impl
    if not __glVertexBindingDivisor_impl:
        fptr = __pyglGetFuncAddress('glVertexBindingDivisor')
        if not fptr:
            raise RuntimeError('The function glVertexBindingDivisor is not available')
        __glVertexBindingDivisor_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_uint)(fptr)
    glVertexBindingDivisor = __glVertexBindingDivisor_impl
    return glVertexBindingDivisor(bindingindex, divisor)
# <command>
#            <proto>void <name>glViewport</name></proto>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>x</name></param>
#            <param group="WinCoord"><ptype>GLint</ptype> <name>y</name></param>
#            <param><ptype>GLsizei</ptype> <name>width</name></param>
#            <param><ptype>GLsizei</ptype> <name>height</name></param>
#            <glx opcode="191" type="render" />
#        </command>
#        
__glViewport_impl=None
def glViewport (x, y, width, height):
    global __glViewport_impl
    if not __glViewport_impl:
        fptr = __pyglGetFuncAddress('glViewport')
        if not fptr:
            raise RuntimeError('The function glViewport is not available')
        __glViewport_impl = __PYGL_FUNC_TYPE( None ,c_int, c_int, c_int, c_int)(fptr)
    glViewport = __glViewport_impl
    return glViewport(x, y, width, height)
# <command>
#            <proto>void <name>glViewportArrayv</name></proto>
#            <param><ptype>GLuint</ptype> <name>first</name></param>
#            <param><ptype>GLsizei</ptype> <name>count</name></param>
#            <param len="COMPSIZE(count)">const <ptype>GLfloat</ptype> *<name>v</name></param>
#        </command>
#        
__glViewportArrayv_impl=None
def glViewportArrayv (first, count, v):
    global __glViewportArrayv_impl
    if not __glViewportArrayv_impl:
        fptr = __pyglGetFuncAddress('glViewportArrayv')
        if not fptr:
            raise RuntimeError('The function glViewportArrayv is not available')
        __glViewportArrayv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_int, c_void_p)(fptr)
    glViewportArrayv = (lambda first,count,v:__glViewportArrayv_impl(first,count,__pyglGetAsConstVoidPointer( v )))
    return glViewportArrayv(first, count, v)
# <command>
#            <proto>void <name>glViewportIndexedf</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param><ptype>GLfloat</ptype> <name>x</name></param>
#            <param><ptype>GLfloat</ptype> <name>y</name></param>
#            <param><ptype>GLfloat</ptype> <name>w</name></param>
#            <param><ptype>GLfloat</ptype> <name>h</name></param>
#        </command>
#        
__glViewportIndexedf_impl=None
def glViewportIndexedf (index, x, y, w, h):
    global __glViewportIndexedf_impl
    if not __glViewportIndexedf_impl:
        fptr = __pyglGetFuncAddress('glViewportIndexedf')
        if not fptr:
            raise RuntimeError('The function glViewportIndexedf is not available')
        __glViewportIndexedf_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_float, c_float, c_float, c_float)(fptr)
    glViewportIndexedf = __glViewportIndexedf_impl
    return glViewportIndexedf(index, x, y, w, h)
# <command>
#            <proto>void <name>glViewportIndexedfv</name></proto>
#            <param><ptype>GLuint</ptype> <name>index</name></param>
#            <param len="4">const <ptype>GLfloat</ptype> *<name>v</name></param>
#        </command>
#        
__glViewportIndexedfv_impl=None
def glViewportIndexedfv (index, v):
    global __glViewportIndexedfv_impl
    if not __glViewportIndexedfv_impl:
        fptr = __pyglGetFuncAddress('glViewportIndexedfv')
        if not fptr:
            raise RuntimeError('The function glViewportIndexedfv is not available')
        __glViewportIndexedfv_impl = __PYGL_FUNC_TYPE( None ,c_uint, c_void_p)(fptr)
    glViewportIndexedfv = (lambda index,v:__glViewportIndexedfv_impl(index,__pyglGetAsConstVoidPointer( v )))
    return glViewportIndexedfv(index, v)
# <command>
#            <proto>void <name>glWaitSync</name></proto>
#            <param group="sync"><ptype>GLsync</ptype> <name>sync</name></param>
#            <param><ptype>GLbitfield</ptype> <name>flags</name></param>
#            <param><ptype>GLuint64</ptype> <name>timeout</name></param>
#        </command>
#        
__glWaitSync_impl=None
def glWaitSync (sync, flags, timeout):
    global __glWaitSync_impl
    if not __glWaitSync_impl:
        fptr = __pyglGetFuncAddress('glWaitSync')
        if not fptr:
            raise RuntimeError('The function glWaitSync is not available')
        __glWaitSync_impl = __PYGL_FUNC_TYPE( None ,c_void_p, c_uint, c_ulonglong)(fptr)
    glWaitSync = __glWaitSync_impl
    return glWaitSync(sync, flags, timeout)

__glShaderSource_impl = None
def glShaderSource(shader,count,list_of_strings,list_of_lengths):
    global __glShaderSource_impl
    if __glShaderSource_impl == None:
        __glShaderSource_impl = __PYGL_FUNC_TYPE(None,c_uint,c_size_t,POINTER(c_char_p),
            POINTER(c_uint))(__pyglGetFuncAddress("glShaderSource"))
    
    if list_of_lengths == None:
        list_of_lengths = [len(q) for q in list_of_strings]
        
    if len(list_of_strings) != len(list_of_lengths):
        raise RuntimeError("List length mismatch")
        
    sarray = (c_char_p * len(list_of_strings))()
    iarray = (c_uint * len(list_of_lengths))()

    for i in range(len(list_of_strings)):
        sarray[i] = list_of_strings[i].encode()
        iarray[i] = list_of_lengths[i]
    
    return __glShaderSource_impl( shader, count, sarray, iarray )

__pyglDebugMessageCallbackFunc=None
__pyglDebugMessageCallbackArg=None
def __pyglDebugMessageCallback(src,typ,id_,sev,le,msg,p):
    if __pyglDebugMessageCallbackFunc:
        __pyglDebugMessageCallbackFunc( src,typ,id_,sev,le,msg.decode(),__pyglDebugMessageCallbackArg)

__glDebugMessageCallback_impl = None
def glDebugMessageCallback(func,parm):
    global __pyglDebugMessageCallbackFunc
    global __pyglDebugMessageCallbackArg
    global __pyglDebugMessageCallbackRef
    global __glDebugMessageCallback_impl
    
    #source,type,id,severity,length,mesg,parm)
    if sys.platform.lower().find("win32") != -1:
        FT = WINFUNCTYPE
    else:
        FT = CFUNCTYPE
        
    __pyglDebugMessageCallbackFunc = func
    __pyglDebugMessageCallbackArg = parm
    
    tmp = FT(None,c_uint,c_uint,c_uint,c_uint,c_uint,c_char_p,c_void_p)
    tmp2 = tmp(__pyglDebugMessageCallback)
    
    #need to hold a reference to the variable
    #to prevent garbage collection
    __pyglDebugMessageCallbackRef = tmp2
    
    if __glDebugMessageCallback_impl == None:
        __glDebugMessageCallback_impl = __PYGL_FUNC_TYPE(None,c_void_p,c_void_p)(
            __pyglGetFuncAddress("glDebugMessageCallback")
        )
    return __glDebugMessageCallback_impl( tmp2, None )
    
