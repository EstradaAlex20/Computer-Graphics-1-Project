
"""Classes for 2D and 3D matrix/vector math."""

# ~ Some of these functions (individually noted) are based on code from TDL.
# ~ The TDL copyright is as follows:
 
# ~ Copyright 2009, Google Inc.
# ~ All rights reserved.

# ~ Redistribution and use in source and binary forms, with or without
# ~ modification, are permitted provided that the following conditions are
# ~ met:

# ~ *  Redistributions of source code must retain the above copyright
# ~ notice, this list of conditions and the following disclaimer.
# ~ *  Redistributions in binary form must reproduce the above
# ~ copyright notice, this list of conditions and the following disclaimer
# ~ in the documentation and/or other materials provided with the
# ~ distribution.
# ~ *  Neither the name of Google Inc. nor the names of its
# ~ contributors may be used to endorse or promote products derived from
# ~ this software without specific prior written permission.

# ~ THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ~ "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# ~ LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# ~ A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# ~ OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# ~ SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# ~ LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# ~ DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# ~ THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# ~ (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# ~ OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import array,math

__all__ = ["vec2","vec3","vec4","mat2","mat3","mat4",
    "dot","cross","length","normalize","transpose",
    "inverse","axisRotation","scaling", "rotation",
    "translation","Matrix","Vector","Vector2","Vector3","Vector4",
    "rotation2","scaling2","translation2",
    "rotation3","scaling3","translation3",
    
]

class Matrix:
    """Contains functionality common to all matrices"""
    
    def __add__(self,m2):
        """Return the sum of two matrices.
        @param m2: matrix
        @rtype: matrix
        @return: The matrix sum."""
        if type(self) != type(m2):
            return NotImplemented
        r = type(self)()
        for i in range(len(self._M)):
            r._M[i] = self._M[i] + m2._M[i]
        return r
        
    def __sub__(self,m2):
        """Return the difference between two matrices.
        @param m2: matrix
        @rtype: matrix
        @return: The matrix difference."""
        if type(self) != type(m2):
            return NotImplemented
        r = type(self)()
        for i in range(len(self._M)):
            r._M[i] = self._M[i] - m2._M[i]
        return r
        
    def __mul__(self,o):
        """Return matrix-matrix, matrix-vector, or matrix-scalar product.
        @param o: matrix, vector, or scalar
        @rtype: matrix or vector, depending on type of o
        @return: The product
        """
        if type(o) == type(self):
            #mat * mat
            R=type(self)()
            for i in range(self.nr):
                for j in range(o.nc):
                    total=0
                    for k in range(self.nc):
                        total += self[i][k] * o[k][j]
                    #all matrices are padded to 4 columns
                    R._M[i*4+j] = total
            return R
        
        if type(o) == float or type(o) == int:
            #mat * scalar
            R = type(self)()
            for i in range(len(self._M)):
                R._M[i] = self._M[i] * o
            return R
        
        #mat * vector or mat*list
        if self.nc != len(o):
            return NotImplemented
        if self.nc == 4:
            R=vec4()
        elif self.nc == 3:
            R=vec3()
        else:
            R=vec2()
        for i in range(self.nr):
            total=0
            for j in range(self.nc):
                total += self[i][j] * o[j]
            R[i]=total
        return R
        
    def __rmul__(self,o):
        """Return matrix-scalar product.
        @param o: scalar
        @rtype: matrix 
        @return: The product
        """
        if type(o) == float or type(o) == int:
            return self*o
        else:
            return transpose(self)*o

    def __neg__(self):
        """Return negated matrix.
        @rtype: matrix
        """
        return -1*self

    def __pos__(self):
        """Return a copy of the matrix.
        @rtype: matrix"""
        #make a copy
        return 1*self
        
    def tobytes(self):
        """Return byte array for underlying matrix data.
        @rtype: bytes"""
        return self._M.tobytes()
        
    def __bytes__(self):
        return self.tobytes()
        
    class MatRow:
        def __init__(self,m,i):
            self.m=m
            self.i=i
        def __getitem__(self,j):
            #each row is padded out to be a vec4
            assert j < self.m.nc
            return self.m._M[self.i*4 + j]
        def __setitem__(self,j,v):
            #each row is padded out to be a vec4
            assert j < self.m.nc
            assert type(v) == int or type(v) == float
            self.m._M[self.i*4+j]=v

    def __getitem__(self,i):
        """Used to get or set matrix items.
            Example use: tmp = M[i][j]  or  M[i][j] = 42
            or tmp = M[i,j] or M[i,j] = 42"""
        if type(i) == int or type(i) == float:
            return Matrix.MatRow(self,i)
        else:
            r,c = i
            return self._M[r*4+c]
    
    def __setitem__(self,tpl,v):
        """Used to get or set matrix items.
            Example use: tmp = M[i][j]  or  M[i][j] = 42
            or tmp = M[i,j] or M[i,j] = 42"""
        r,c = tpl
        assert type(v) == int or type(v) == float
        self._M[r*4+c] = v
        
    def __eq__(self,o):
        """Return true if two matrices are equal.
        @rtype: boolean
        """
        if type(o) != type(self):
            return False
        for i in range(len(self._M)):
            if self._M[i] != o._M[i]:
                return False
        return True
        
    def __ne__(self,o):
        """Return true if two matrices are not equal.
        @rtype: boolean
        """
        return not self==o
        
    def __str__(self):
        """Return printable representation of matrix.
        @rtype: string
        """
        s=""
        for i in range(self.nr):
            s += "["
            for j in range(self.nc):
                s += "%-4.6f" % self[i][j]
                s += "   "
            s += "]\n"
        return s
        
    def __repr__(self):
        """Return printable representation of matrix.
        @rtype: string"""
        return str(self)
       
    def transpose(self):
        """Return transposed matrix.
        @rtype: matrix
        """
        R=type(self)()
        for i in range(self.nr):
            for j in range(self.nc):
                R[i][j] = self[j][i]
        return R
        
    def inverse(self):
        """Return matrix inverse. From TDL.
        @rtype: matrix
        """
        m=self
        if type(m) == mat2:
            d = 1.0 / (m[0][0] * m[1][1] - m[0][1] * m[1][0])
            return mat2(d * m[1][1], -d * m[0][1], -d * m[1][0], d * m[0][0])
        elif type(m) == mat3:
            t00 = m[1][1] * m[2][2] - m[1][2] * m[2][1]
            t10 = m[0][1] * m[2][2] - m[0][2] * m[2][1]
            t20 = m[0][1] * m[1][2] - m[0][2] * m[1][1]
            d = 1.0 / (m[0][0] * t00 - m[1][0] * t10 + m[2][0] * t20)
            return mat3( d * t00, -d * t10, d * t20,
                  -d * (m[1][0] * m[2][2] - m[1][2] * m[2][0]),
                   d * (m[0][0] * m[2][2] - m[0][2] * m[2][0]),
                  -d * (m[0][0] * m[1][2] - m[0][2] * m[1][0]),
                   d * (m[1][0] * m[2][1] - m[1][1] * m[2][0]),
                  -d * (m[0][0] * m[2][1] - m[0][1] * m[2][0]),
                   d * (m[0][0] * m[1][1] - m[0][1] * m[1][0]) )
        elif type(m) == mat4:
            tmp_0 = m[2][2] * m[3][3]
            tmp_1 = m[3][2] * m[2][3]
            tmp_2 = m[1][2] * m[3][3]
            tmp_3 = m[3][2] * m[1][3]
            tmp_4 = m[1][2] * m[2][3]
            tmp_5 = m[2][2] * m[1][3]
            tmp_6 = m[0][2] * m[3][3]
            tmp_7 = m[3][2] * m[0][3]
            tmp_8 = m[0][2] * m[2][3]
            tmp_9 = m[2][2] * m[0][3]
            tmp_10 = m[0][2] * m[1][3]
            tmp_11 = m[1][2] * m[0][3]
            tmp_12 = m[2][0] * m[3][1]
            tmp_13 = m[3][0] * m[2][1]
            tmp_14 = m[1][0] * m[3][1]
            tmp_15 = m[3][0] * m[1][1]
            tmp_16 = m[1][0] * m[2][1]
            tmp_17 = m[2][0] * m[1][1]
            tmp_18 = m[0][0] * m[3][1]
            tmp_19 = m[3][0] * m[0][1]
            tmp_20 = m[0][0] * m[2][1]
            tmp_21 = m[2][0] * m[0][1]
            tmp_22 = m[0][0] * m[1][1]
            tmp_23 = m[1][0] * m[0][1]

            t0 = (tmp_0 * m[1][1] + tmp_3 * m[2][1] + tmp_4 * m[3][1]) -        (tmp_1 * m[1][1] + tmp_2 * m[2][1] + tmp_5 * m[3][1])
            t1 = (tmp_1 * m[0][1] + tmp_6 * m[2][1] + tmp_9 * m[3][1]) -        (tmp_0 * m[0][1] + tmp_7 * m[2][1] + tmp_8 * m[3][1])
            t2 = (tmp_2 * m[0][1] + tmp_7 * m[1][1] + tmp_10 * m[3][1]) -        (tmp_3 * m[0][1] + tmp_6 * m[1][1] + tmp_11 * m[3][1])
            t3 = (tmp_5 * m[0][1] + tmp_8 * m[1][1] + tmp_11 * m[2][1]) -        (tmp_4 * m[0][1] + tmp_9 * m[1][1] + tmp_10 * m[2][1])
            d = 1.0 / (m[0][0] * t0 + m[1][0] * t1 + m[2][0] * t2 + m[3][0] * t3)

            return mat4(d * t0, d * t1, d * t2, d * t3,
               d * ((tmp_1 * m[1][0] + tmp_2 * m[2][0] + tmp_5 * m[3][0]) -
                  (tmp_0 * m[1][0] + tmp_3 * m[2][0] + tmp_4 * m[3][0])),
               d * ((tmp_0 * m[0][0] + tmp_7 * m[2][0] + tmp_8 * m[3][0]) -
                  (tmp_1 * m[0][0] + tmp_6 * m[2][0] + tmp_9 * m[3][0])),
               d * ((tmp_3 * m[0][0] + tmp_6 * m[1][0] + tmp_11 * m[3][0]) -
                  (tmp_2 * m[0][0] + tmp_7 * m[1][0] + tmp_10 * m[3][0])),
               d * ((tmp_4 * m[0][0] + tmp_9 * m[1][0] + tmp_10 * m[2][0]) -
                  (tmp_5 * m[0][0] + tmp_8 * m[1][0] + tmp_11 * m[2][0])),
               d * ((tmp_12 * m[1][3] + tmp_15 * m[2][3] + tmp_16 * m[3][3]) -
                  (tmp_13 * m[1][3] + tmp_14 * m[2][3] + tmp_17 * m[3][3])),
               d * ((tmp_13 * m[0][3] + tmp_18 * m[2][3] + tmp_21 * m[3][3]) -
                  (tmp_12 * m[0][3] + tmp_19 * m[2][3] + tmp_20 * m[3][3])),
               d * ((tmp_14 * m[0][3] + tmp_19 * m[1][3] + tmp_22 * m[3][3]) -
                  (tmp_15 * m[0][3] + tmp_18 * m[1][3] + tmp_23 * m[3][3])),
               d * ((tmp_17 * m[0][3] + tmp_20 * m[1][3] + tmp_23 * m[2][3]) -
                  (tmp_16 * m[0][3] + tmp_21 * m[1][3] + tmp_22 * m[2][3])),
               d * ((tmp_14 * m[2][2] + tmp_17 * m[3][2] + tmp_13 * m[1][2]) -
                  (tmp_16 * m[3][2] + tmp_12 * m[1][2] + tmp_15 * m[2][2])),
               d * ((tmp_20 * m[3][2] + tmp_12 * m[0][2] + tmp_19 * m[2][2]) -
                  (tmp_18 * m[2][2] + tmp_21 * m[3][2] + tmp_13 * m[0][2])),
               d * ((tmp_18 * m[1][2] + tmp_23 * m[3][2] + tmp_15 * m[0][2]) -
                  (tmp_22 * m[3][2] + tmp_14 * m[0][2] + tmp_19 * m[1][2])),
               d * ((tmp_22 * m[2][2] + tmp_16 * m[0][2] + tmp_21 * m[1][2]) -
                  (tmp_20 * m[1][2] + tmp_23 * m[2][2] + tmp_17 * m[0][2])))



class mat4 (Matrix):
    """4x4 matrix"""
    def __init__(self,*args):
        """Initialize the mat4. If called with no arguments,
        initialize matrix to all zeros. If called with
        arguments, there must be 16 scalars. They are will
        be loaded into the matrix, in row-major order."""
        self.nr=4
        self.nc=4
        if len(args) == 0:
            self._M = array.array("f",[0]*16)
        elif len(args) == 16:
            self._M = array.array("f",args)
        else:
            raise RuntimeError("Bad number of arguments")
            
    @staticmethod
    def identity():
        """Return identity matrix.
        @rtype: mat4
        """
        return mat4(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1)
        
class mat3(Matrix):
    """3x3 matrix"""
    def __init__(self,*args):
        """Initialize the mat3. If called with no arguments,
        initialize matrix to all zeros. If called with
        arguments, there must be 9 scalars. They are will
        be loaded into the matrix, in row-major order."""
        self.nr=3
        self.nc=3
        if len(args) == 0:
            self._M = array.array("f",[0]*12)
        elif len(args) == 9:
            tmp = [ args[0], args[1], args[2], 0,
                    args[3], args[4], args[5], 0,
                    args[6], args[7], args[8], 0 ]
            self._M = array.array("f",tmp )
        else:
            raise RuntimeError("Bad number of arguments")
        
    @staticmethod
    def identity():
        """Return identity matrix.
        @rtype: mat3"""
        return mat3(1,0,0,0,1,0,0,0,1)

class mat2(Matrix):
    """2x2 matrix"""
    
    def __init__(self,*args):
        """Initialize the mat2. If called with no arguments,
        initialize matrix to all zeros. If called with
        arguments, there must be 4 scalars. They are will
        be loaded into the matrix, in row-major order."""
        self.nr=2
        self.nc=2
        if len(args) == 0:
            self._M = array.array("f",[0]*8)
        elif len(args) == 4:
            tmp = [args[0],args[1],0,0, args[2],args[3], 0,0 ]
            self._M = array.array("f",tmp)
        else:
            raise RuntimeError("Bad number of arguments")

    @staticmethod
    def identity():
        """Return identity matrix.
        @rtype:mat2"""
        return mat2(1,0,0,1)
        

class Vector:
    """Contains functionality common to all vector types."""
    
    def tobytes(self):
        """Return raw byte array for vector data.
        @rtype:bytes"""
        return self._v.tobytes()
    
    def __bytes__(self):
        return self.tobytes()
        
    def __getitem__(self,key):
        """Return item from vector.
        @type key: integer
        @param key: Zero-based index
        @return: number"""
        return self._v[key]
            
    def __setitem__(self,key,value):
        """Set vector item.
        @type key: integer
        @param key: index, zero-based.
        @param value: Value to set.
        @type value: number
        """
        self._v[key]=value
        
    def __str__(self):
        """Return printable representation of vector.
        @rtype: string"""
        return "vec"+str(len(self))+"("+",".join([str(q) for q in self._v])+")"
        
    def copy(self):
        """Return a copy of this vector.
        @rtype: vector"""
        return 1*self
        
    def __repr__(self):
        """Return printable representation of vector.
        @rtype: string"""
        return str(self)
      
    def __len__(self):
        """Return number of components in vector."""
        return len(self._v)

    def __radd__(self,o):
        """Vector addition.
        @type o: list of scalar
        @return: The sum.
        @rtype: vector"""
        return self + o
        
    def __add__(self,o):
        """Vector addition.
        @type o: vector or list of scalar
        @return: The sum.
        @rtype: vector"""
        if len(self) != len(o):
            return NotImplemented
        L=type(self)()
        for i in range(len(self._v)):
            L._v[i] =  self._v[i]+o[i]
        return L

    def __rsub__(self,o):
        """Vector subtraction.
        @type o: list of scalar
        @return: The difference.
        @rtype: vector"""
        return -self+o

    def __sub__(self,o):
        """Vector subtraction.
        @type o: vector or list of scalar
        @return: The difference.
        @rtype: vector"""
        L=type(self)()
        if len(self) != len(o):
            return NotImplemented
        for i in range(len(self._v)):
            L._v[i] =  self._v[i]-o[i]
        return L

    def __mul__(self,o):
        """Multiplies this vector by the argument.
        @param o: The item to multiply
        @type o: Vector, matrix, list of scalars, or scalar
        @rtype: vector
        @return: The product. If argument is vector or list of scalars, 
            do component-wise multiply
            (Hadamard product). If argument is scalar,
            multiply by each component of this vector.
            If argument is matrix, compute vector-matrix product.
        """
        if isinstance(o,Matrix):
            if len(self) != o.nr:
                return NotImplemented
            R=type(self)()
            for i in range(o.nc):
                total=0
                for j in range(len(self)):
                    total += self[j]*o[j][i]
                R[i]=total
            return R
        elif type(o) == float or type(o) == int:
            R=type(self)()
            for i in range(len(self)):
                R[i] = self._v[i]*o
            return R
        elif len(o) == len(self):
            #component-wise multiply (Hadamard product)
            R=type(self)()
            for i in range(len(self)):
                R[i] = self[i]*o[i]
            return R
        else:
            return NotImplemented
    
    def __rmul__(self,o):
        """Implements o*self: Same as self*o (see __mul__)
        """
        return self*o


    def __neg__(self):
        """Return copy of vector, negated.
        @rtype:vector"""
        return -1*self

    def __pos__(self):
        """Return copy of vector.
        @rtype:vector"""
        return 1*self
     
    def __iter__(self):
        return self._v.__iter__()
      
    def __eq__(self,o):
        """Test for equality.
        @rtype:boolean"""
        if not hasattr(o,"__len__"):
            return False
        if len(o) != len(self):
            return False
        for i in range(len(self._v)):
            if self._v[i] != o[i]:
                return False
        return True
        
    def __ne__(self,o):
        """Test for inequality."""
        return not self==o
    
    def _getmagnitude(self):       return length(self)
    magnitude = property( _getmagnitude, None )
    def _getmagnitudeSq(self):       return dot(self,self)
    magnitudeSq = property( _getmagnitudeSq, None )
    def _getnormalized(self):   return normalize(self)
    normalized = property(_getnormalized,None)
    def _isZero(self):
        return dot(self,self) == 0
    isZero = property(_isZero,None)
    
    def _getx(self):            return self._v[ 0 ]
    def _setx(self,v):          self._v[ 0 ]=v
    def _gety(self):            return self._v[ 1 ]
    def _sety(self,v):          self._v[ 1 ]=v
    def _getz(self):            return self._v[ 2 ]
    def _setz(self,v):          self._v[ 2 ]=v
    def _getw(self):            return self._v[ 3 ]
    def _setw(self,v):          self._v[ 3 ]=v
    def _getxyzw(self):         return vec4(self._v[0],self._v[1],self._v[2],self._v[3])
    def _setxyzw(self,v):       self._v[0]=v[0]; self._v[1]=v[1]; self._v[2]=v[2]; self._v[3]=v[3]
    def _getxyz(self):          return vec3(self._v[0],self._v[1],self._v[2])
    def _setxyz(self,v):        self._v[0]=v[0]; self._v[1]=v[1]; self._v[2]=v[2]
    def _getxy(self):           return vec2(self._v[0],self._v[1])
    def _setxy(self,v):         self._v[0]=v[0]; self._v[1]=v[1]
    x = property(_getx , _setx )
    y = property(_gety , _sety )
    z = property(_getz , _setz )
    w = property(_getw , _setw )
    xyzw = property(_getxyzw , _setxyzw )
    xyz = property(_getxyz , _setxyz )
    xy = property(_getxy , _setxy )
                       
class vec4(Vector):
    """4D vector"""
    def __init__(self,*args):
        if len(args)==0:
            args=[ 0,0,0,0 ]
        if len(args) != 4:
            raise RuntimeError("Bad number of arguments: Got "+str(len(args)))
        self._v = array.array("f",args)
                     
class vec3(Vector):
    """3D vector"""
    def __init__(self,*args):
        if len(args)==0:
            args=[ 0,0,0 ]
        if len(args) != 3:
            raise RuntimeError("Bad number of arguments")
        self._v = array.array("f",args)

class vec2(Vector):
    """2D vector"""
    def __init__(self,*args):
        if len(args)==0:
            args=[ 0,0 ]
        if len(args) != 2:
            raise RuntimeError("Bad number of arguments")
        self._v = array.array("f",args)
    def _radians(self):
        return math.atan2(self.y,self.x)
    def _degrees(self):
        return 180*math.atan2(self.y,self.x)/math.pi
    radians = property(_radians,None)
    degrees = property(_degrees,None)
        
        
        
def dot(v,w):
    """Return vector dot product.
    @rtype: number
    @type v: vector or list of scalar
    @type w: vector or list of scalar
    """
    assert len(v) == len(w)
    return sum( [v[i]*w[i] for i in range(len(v)) ] )
    
def cross(v,w):
    """Return vector cross product. 
    @type v: vec3, vec4 (w is ignored), or list of scalar
    @type w: vec3, vec4 (w is ignored), or list of scalar
    @rtype:vec3
    """
    return vec3(
        v[1]*w[2] - w[1]*v[2],
        w[0]*v[2] - v[0]*w[2],
        v[0]*w[1] - w[0]*v[1]
    )

def length(v):
    """Return length of vector.
    @rtype:number
    """
    return dot(v,v)**0.5
    
def normalize(v):
    """Return normalized copy of vector.
    @rtype: vector"""
    L=len(v)
    le=1/length(v)
    return le*v
    # ~ if L == 4:
        # ~ return vec4(le*v[0],le*v[1],le*v[2],le*v[3])
    # ~ if L == 3:
        # ~ return vec3(le*v[0],le*v[1],le*v[2])
    # ~ if L == 2:
        # ~ return vec2(le*v[0],le*v[1])
    # ~ assert 0

def transpose(m):
    """Return transposed matrix.
    @rtype: matrix
    @type m: matrix
    """
    return m.transpose()
    
# ~ def det(M):
    # ~ """Return matrix determinant. From TDL.
    # ~ @param M: matrix
    # ~ @rtype: number
    # ~ """
    # ~ if type(M) == mat2:
        # ~ return m[0][0]*m[1][1] - m[0][1]*m[1][0]
    # ~ elif type(M) == mat3:
        # ~ return m[2][2] * (m[0][0] * m[1][1] - m[0][1] * m[1][0]) -              m[2][1] * (m[0][0] * m[1][2] - m[0][2] * m[1][0]) +                m[2][0] * (m[0][1] * m[1][2] - m[0][2] * m[1][1])
    # ~ elif type(M) == mat4:
        # ~ t01 = m[0][0] * m[1][1] - m[0][1] * m[1][0]
        # ~ t02 = m[0][0] * m[1][2] - m[0][2] * m[1][0]
        # ~ t03 = m[0][0] * m[1][3] - m[0][3] * m[1][0]
        # ~ t12 = m[0][1] * m[1][2] - m[0][2] * m[1][1]
        # ~ t13 = m[0][1] * m[1][3] - m[0][3] * m[1][1]
        # ~ t23 = m[0][2] * m[1][3] - m[0][3] * m[1][2]
        # ~ return (m[3][3] * (m[2][2] * t01 - m[2][1] * t02 + m[2][0] * t12) -
             # ~ m[3][2] * (m[2][3] * t01 - m[2][1] * t03 + m[2][0] * t13) +
             # ~ m[3][1] * (m[2][3] * t02 - m[2][2] * t03 + m[2][0] * t23) -
             # ~ m[3][0] * (m[2][3] * t12 - m[2][2] * t13 + m[2][1] * t23) )
    # ~ else:
        # ~ assert 0

def inverse(m):
    """Return matrix inverse.
        @param m: matrix
        @rtype:matrix
    """
    return m.inverse()
    

def rotation3(axis,angle):
    """Compute rotation matrix.
    @param axis: The axis of rotation; must be unit length.
    @type axis: vec3, vec4, or list of at least three scalars
    @type angle: scalar
    @param angle: Angle, in radians
    @rtype: mat4
    """
    return axisRotation(axis,angle)
    
def rotation(axis,angle):
    """Compute rotation matrix.
    @param axis: The axis of rotation; must be unit length.
    @type axis: vec3, vec4, or list of at least three scalars
    @type angle: scalar
    @param angle: Angle, in radians
    @rtype: mat4
    """
    return axisRotation(axis,angle)
    
def axisRotation(axis,angle):
    """Compute rotation matrix. From TDL.
    @param axis: The axis of rotation; must be unit length.
    @type axis: vec3, vec4, or list of at least three scalars
    @type angle: scalar
    @param angle: Angle, in radians
    @rtype: mat4
    """
    #axis=normalize(axis)
    x = axis[0]
    y = axis[1]
    z = axis[2]
    xx = x * x
    yy = y * y
    zz = z * z
    c = math.cos(angle)
    s = math.sin(angle)
    oneMinusCosine = 1 - c
    zs = z*s
    xs = x*s
    ys = y*s
    xy = x*y
    xz = x*z
    yz = y*z
    return mat4(
        xx + (1 - xx) * c,
        xy * oneMinusCosine + zs,
        xz * oneMinusCosine - ys,
        0,
        xy * oneMinusCosine - zs,
        yy + (1 - yy) * c,
        yz * oneMinusCosine + xs,
        0,
        xz * oneMinusCosine + ys,
        yz * oneMinusCosine - xs,
        zz + (1 - zz) * c,
        0,
        0, 0, 0, 1
    )
    

def scaling3(v):
    """Return scaling matrix. From TDL.
    @type v: vec3, vec4, or list of
        at least 3 scalars. 
    @rtype: mat4"""
    return scaling(v)
    
def scaling(v):
    """Return scaling matrix. From TDL.
    @type v: vec3, vec4, or list of
        at least 3 scalars. 
    @rtype: mat4"""
    return mat4( 
        v[0], 0,0,0,
        0,v[1],0,0,
        0,0,v[2],0,
        0,0,0,1)

def translation3(v):
    """Return translation matrix. From TDL.
    @type v: vec3, vec4, or list of at least 3 scalars
    @rtype:mat4
        """
    return translation(v)
    
def translation(v):
    """Return translation matrix. From TDL.
    @type v: vec3, vec4, or list of at least 3 scalars
    @rtype:mat4
        """
    return mat4(
        1,0,0,0,
        0,1,0,0,
        0,0,1,0,
        v[0],v[1],v[2],1)

def translation2(v):
    """Return 2D translation matrix. 
    @type v: vec2 or list of at least 2 scalars
    @rtype:mat3
        """
    return mat3(
        1,0,0,
        0,1,0,
        v[0],v[1],1)

def scaling2(v):
    """Return 2D scaling matrix.
        @type v: vec2 or list of at least 2 scalars
        @rtype:mat3
    """
    return mat3(v[0],0,0,
                0,v[1],0,
                0,0,1)
                
def rotation2(angle):
    """Return 2D rotation matrix.
        @type angle: float
        @param angle: Angle in radians
        @rtype:mat3
    """
    c=math.cos(angle)
    s=math.sin(angle)
    return mat3( c,s,0,     -s,c,0,     0,0,1 )
    
class Vector2(vec2):
    """Alternate name for vec2"""
    pass
    
class Vector3(vec3):
    """Alternate name for vec3"""
    pass

class Vector4(vec4):
    """Alternate name for vec4"""
    pass
    

#name equivalents for D3D        
class float4(vec4):
    pass
    
class float3(vec3):
    pass
    
class float2(vec2):
    pass
    
class float4x4(mat4):
    pass
    
class float3x3(mat3):
    pass

class float2x2(mat2):
    pass
    
def mul(a,b):
    return a*b
    
if __name__ == "__main__":
    #test harness

    la = [3,-1,4,6]
    lb = [2,5,8,9]
    a = vec4(*la)
    b = vec4(*lb)
    assert a+b == vec4(5,4,12,15)
    assert a+lb == a+b
    assert la+b == a+b
    assert a-b == vec4(1,-6,-4,-3)
    assert a-lb == a-b
    assert la-b == a-b
    assert a != b
    assert a*b == [6,-5,32,54]
    assert a*lb == [6,-5,32,54]
    assert la*b == [6,-5,32,54]
    assert 2*a == vec4(6,-2,8,12)
    assert a*2 == 2*a
    assert -a == [-3,1,-4,-6]
    assert a == +a
    assert id(a) != id(+a)
    str(a)
    repr(a)
    assert a.copy() == a
    assert id(a.copy()) != a
    c=vec4()
    assert c.isZero
    assert c == vec4(0,0,0,0)
    assert c[0] == 0
    assert c[1] == 0
    assert c[2] == 0
    assert c[3] == 0
    assert not a.isZero
    c[0]=1
    c[1]=3
    c[2]=5
    c[3]=9
    assert c == vec4(1,3,5,9)
    assert c == [1,3,5,9]
    assert c != [2,4,6,8]
    assert c[0] == 1
    assert c.x == 1
    assert c[1] == 3
    assert c.y == 3
    assert c[2] == 5
    assert c.z == 5
    assert c[3] == 9
    assert c.w == 9
    assert c.xy == vec2(1,3)
    assert c.xyz == vec3(1,3,5)
    c.x = 8
    c.y = 9
    c.z= -8
    c.w = -7
    assert c == vec4(8,9,-8,-7)
    c.xy = vec2(3,2)
    assert c == vec4(3,2,-8,-7)
    c.xyz = vec3(13,12,11)
    assert c == vec4(13,12,11,-7)
    c.xyzw = vec4(13,12,11,10)
    assert c == vec4(13,12,11,10)
    assert len(a) == 4
    tmp=[]
    for x in a:
        tmp.append(x)
    assert tmp == la
    assert length(a) == a.magnitude
    a.tobytes()
    n=a.normalized
    n2=normalize(a)
    assert n==n2
    n3 = [0.381,-0.127, 0.508, 0.762]
    for i in range(len(n3)):
        assert abs(n3[i] - n[i]) < 0.001
    assert length(a) == a.magnitude
    assert abs(length(a)-7.874) < 0.001
    assert dot(a,b) == 87
 
    ###
    
    la = [3,-1,4]
    lb = [2,5,8]
    a = vec3(*la)
    b = vec3(*lb)
    assert a+b == vec3(5,4,12)
    assert a+lb == a+b
    assert la+b == a+b
    assert a-b == vec3(1,-6,-4)
    assert a-lb == a-b
    assert la-b == a-b
    assert a != b
    assert a*b == [6,-5,32]
    assert a*lb == [6,-5,32]
    assert la*b == [6,-5,32]
    assert 2*a == (6,-2,8)
    assert a*2 == 2*a
    assert -a == [-3,1,-4]
    assert a == +a
    assert id(a) != id(+a)
    str(a)
    repr(a)
    assert a.copy() == a
    assert id(a.copy()) != a
    c=vec3()
    assert c.isZero
    assert c == vec3(0,0,0)
    assert c[0] == 0
    assert c[1] == 0
    assert c[2] == 0
    assert not a.isZero
    c[0]=1
    c[1]=3
    c[2]=5
    assert c == vec3(1,3,5)
    assert c == [1,3,5]
    assert c != [2,4,6]
    assert c[0] == 1
    assert c.x == 1
    assert c[1] == 3
    assert c.y == 3
    assert c[2] == 5
    assert c.z == 5
    assert c.xy == vec2(1,3)
    assert c.xyz == vec3(1,3,5)
    c.x = 8
    c.y = 9
    c.z= -8
    assert c == (8,9,-8)
    c.xy = vec2(3,2)
    assert c == (3,2,-8)
    c.xyz = vec3(13,12,11)
    assert c == vec3(13,12,11)
    assert len(a) == 3
    tmp=[]
    for x in a:
        tmp.append(x)
    assert tmp == la
    assert length(a) == a.magnitude
    a.tobytes()
    n=a.normalized
    n2=normalize(a)
    assert n==n2
    n3 = [0.58834, -0.196116, 0.7844]
    for i in range(len(n3)):
        assert abs(n3[i] - n[i]) < 0.001
    assert abs(length(a)-5.099) < 0.001
    assert dot(a,b) == 33
    
    
    #############################
    la = [3,-1]
    lb = [2,5]
    a = vec2(*la)
    b = vec2(*lb)
    assert a+b == vec2(5,4)
    assert a+lb == a+b
    assert la+b == a+b
    assert a-b == vec2(1,-6)
    assert a-lb == a-b
    assert la-b == a-b
    assert a != b
    assert a*b == [6,-5]
    assert a*lb == [6,-5]
    assert la*b == [6,-5]
    assert 2*a == (6,-2)
    assert a*2 == 2*a
    assert -a == [-3,1,]
    assert a == +a
    assert id(a) != id(+a)
    str(a)
    repr(a)
    assert a.copy() == a
    assert id(a.copy()) != a
    c=vec2()
    assert c.isZero
    assert c == vec2(0,0)
    assert c[0] == 0
    assert c[1] == 0
    assert not a.isZero
    c[0]=1
    c[1]=3
    assert c == vec2(1,3)
    assert c == [1,3]
    assert c != [2,4]
    assert c[0] == 1
    assert c.x == 1
    assert c[1] == 3
    assert c.y == 3
    assert c.xy == vec2(1,3)
    c.x = 8
    c.y = 9
    assert c == (8,9)
    c.xy = vec2(3,2)
    assert c == (3,2)
    assert len(a) == 2
    tmp=[]
    for x in a:
        tmp.append(x)
    assert tmp == la
    assert length(a) == a.magnitude
    a.tobytes()
    n=a.normalized
    n2=normalize(a)
    assert n==n2
    n3 = [0.94868,-0.31622]
    for i in range(len(n3)):
        assert abs(n3[i] - n[i]) < 0.001
    assert abs(length(a)-3.162277) < 0.001
    assert dot(a,b) == 1
    
    ##################
    a = mat4( 3,1,4,5,
              9,2,6,7,
              8,-3,-1,-4,
              -5,-2,-7,-6)
              
    b = mat4( -2,-7,3,8,
              -1,-5,-10,12,
              -4,7,2,4,
              5,-8,1,-3)
    assert a*b == mat4(
        2,-38,12,37,
        -9,-87,26,99,
        -29,-16,48,36,
        10,44,-15,-74)
    assert a != b
    c=mat4()
    c2=mat4()
    for i in range(4):
        for j in range(4):
            assert c[i][j] == 0
            
    x=[     [3,1,4,5],
            [9,2,6,7],
            [8,-3,-1,-4],
            [-5,-2,-7,-6]
    ]
    for i in range(4):
        for j in range(4):
            c[i][j] = x[i][j]
            c2[i,j] = x[i][j]
    assert c == a
    assert c2 == a
    for i in range(4):
        for j in range(4):
            assert c[i][j] == x[i][j]
            assert c2[i,j] == x[i][j]
            
    assert a+b == mat4(1,-6,7,13,8,-3,-4,19,4,4,1,0,0,-10,-6,-9)
    assert a-b == a+-1*b
    assert 2*a == mat4(6,2,8,10,18,4,12,14,16,-6,-2,-8,-10,-4,-14,-12)
    assert 2*a == a*2        
    
    c=+a
    assert id(c) != id(a)
    assert c == a
    assert -a == -1*a
    c = -a
    assert c == mat4( 
                -3,-1,-4,-5,
                -9,-2,-6,-7,
                -8,3,1,4,
                5,2,7,6)
    a.tobytes()
    str(a)
    repr(a)
    assert transpose(a) == mat4( 3,9,8,-5, 1,2,-3,-2, 4,6,-1,-7, 5,7,-4,-6)
    
    x = inverse(a) * a 
    y = a * inverse(a)
    for i in range(4):
        for j in range(4):
            assert abs(x[i][j] - y[i][j] < 0.001)
            if i == j:
                assert abs(x[i][j] - 1) < 0.001
            else:
                assert abs(x[i][j]) < 0.001
                
    assert a*vec4(0.5,1.5,2.5,4.5) == vec4(35.5,54,-21,-50)
    assert vec4(0.5,1.5,2.5,4.5)*a == vec4(12.5,-13,-23,-24)
    assert a*(0.5,1.5,2.5,4.5) == vec4(35.5,54,-21,-50)
    assert (0.5,1.5,2.5,4.5)*a == vec4(12.5,-13,-23,-24)
    assert a*[0.5,1.5,2.5,4.5] == vec4(35.5,54,-21,-50)
    assert [0.5,1.5,2.5,4.5]*a == vec4(12.5,-13,-23,-24)
    
    
    ###################
    ##################
    a = mat3( 3,1,4,
              9,2,6,
              8,-3,-1)
    b = mat3( -2,-7,3,
              -1,-5,-10,
              -4,7,2)
    assert a*b == mat3(
        -23,2,7,  -44,-31,19,  -9,-48,52 )
    assert a != b
    c=mat3()
    c2=mat3()
    for i in range(3):
        for j in range(3):
            assert c[i][j] == 0
            
    x=[     [3,1,4],
            [9,2,6],
            [8,-3,-1] 
    ]
    for i in range(3):
        for j in range(3):
            c[i][j] = x[i][j]
            c2[i,j] = x[i][j]
    assert c == a
    assert c2 == a
    for i in range(3):
        for j in range(3):
            assert c[i][j] == x[i][j]
            assert c2[i,j] == x[i][j]
            
    assert a+b == mat3(1,-6,7,8,-3,-4,4,4,1)
    assert a-b == a+-1*b
    assert 2*a == mat3(6,2,8,   18,4,12,    16,-6,-2)
    assert 2*a == a*2        
    
    c=+a
    assert id(c) != id(a)
    assert c == a
    assert -a == -1*a
    c=-a
    assert c == mat3( 
                -3,-1,-4,
                -9,-2,-6,
                -8,3,1)
    a.tobytes()
    str(a)
    repr(a)
    assert transpose(a) == mat3( 3,9,8, 1,2,-3,   4,6,-1 )
    
    x = inverse(a) * a 
    y = a * inverse(a)
    for i in range(3):
        for j in range(3):
            assert abs(x[i][j] - y[i][j] < 0.001)
            if i == j:
                assert abs(x[i][j] - 1) < 0.001
            else:
                assert abs(x[i][j]) < 0.001
                
    assert a*vec3(0.5,1.5,2.5) == vec3(13,22.5,-3)
    assert vec3(0.5,1.5,2.5)*a == vec3(35,-4,8.5)
    assert a*(0.5,1.5,2.5) == vec3(13,22.5,-3)
    assert (0.5,1.5,2.5)*a == vec3(35,-4,8.5)
    
    #################################

    a = mat2( 3,1,
              9,2 )
    b = mat2( -2,-7,
              -1,-5 )
    assert a*b == mat2( -7,-26, -20, -73 )
    assert a != b
    c=mat2()
    c2=mat2()
    for i in range(2):
        for j in range(2):
            assert c[i][j] == 0
            
    x=[     [3,1],
            [9,2]
    ]
    for i in range(2):
        for j in range(2):
            c[i][j] = x[i][j]
            c2[i,j] = x[i][j]
    assert c == a
    assert c2 == a
    for i in range(2):
        for j in range(2):
            assert c[i][j] == x[i][j]
            assert c[i,j] == x[i][j]
    assert a+b == mat2(1,-6,    8,-3  )
    assert a-b == a+-1*b
    assert 2*a == mat2(6,2,  18,4  )
    assert 2*a == a*2        
    
    c=+a
    assert id(c) != id(a)
    assert c == a
    assert -a == -1*a
    c=-a
    assert c == mat2( -3,-1, -9,-2 )
    a.tobytes()
    str(a)
    repr(a)
    assert transpose(a) == mat2( 3,9, 1,2 )
    
    x = inverse(a) * a 
    y = a * inverse(a)
    for i in range(2):
        for j in range(2):
            assert abs(x[i][j] - y[i][j] < 0.001)
            if i == j:
                assert abs(x[i][j] - 1) < 0.001
            else:
                assert abs(x[i][j]) < 0.001
                
    assert a*vec2(0.5,1.5) == vec2(3,7.5)
    assert vec2(0.5,1.5)*a == vec2(15,3.5)
    assert a*(0.5,1.5) == vec2(3,7.5)
    assert (0.5,1.5)*a == vec2(15,3.5)
    
    ##################
    c = cross( vec3(2,5,9), vec3(0.5,1.5,3.5) )
    assert c == vec3(4,-2.5,.5)
    
    c = cross( vec4(2,5,9,0), vec4(0.5,1.5,3.5,0) )
    assert c == vec3(4,-2.5,.5)

    c = cross( (2,5,9,0), (0.5,1.5,3.5,0) )
    assert c == vec3(4,-2.5,.5)

    
    #axisRotation, scaling,
    #translation,
     
    v2a=vec2(2,4)
    v2b=vec2(10,11)
    
    assert v2a+v2b == vec2(12,15)
    assert v2a-v2b == vec2(-8,-7)
    assert v2a+v2b != vec2(12,3)
    assert v2a+v2b != vec2(3,15)
    assert v2a*v2b == vec2(20,44)
    assert 5*v2a == vec2(10,20)
    assert v2a*5 == vec2(10,20)
    
    assert v2a.xy == v2a
    
    v3a=vec3(2,4,6)
    v3b=vec3(10,11,12)
    
    assert v3a+v3b == vec3(12,15,18)
    assert v3a-v3b == vec3(-8,-7,-6)
    assert v3a+v3b != vec3(12,3,18)
    assert v3a+v3b != vec3(3,15,18)
    assert v3a+v3b != vec3(12,3,0)
    assert v3a*v3b == vec3(20,44,72)
    assert 5*v3a == vec3(10,20,30)
    assert v3a*5 == vec3(10,20,30)
    
    assert v3a.xyz == v3a
    
    m4=mat4(3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3)
    v4=vec4(2,4,6,7)
    va = v4*m4
    vb = m4*v4
    assert transpose(m4) != m4
    assert transpose(transpose(m4)) == m4
    
    m4i = inverse(m4)
    p=m4*m4i
    p2=m4i*m4
    
    for i in range(4):
        for j in range(4):
            if i == j:
                t=1
            else:
                t=0
            assert abs(p[i][j]-t) < 0.001
            assert abs(p2[i][j]-t) < 0.001
            assert abs(p2[i,j]-t) < 0.001
    
    M=axisRotation(vec3(0,1,0),math.radians(90))
    v=vec4(0,0,1,0)*M
    assert abs(dot(v,vec4(0,0,1,0))) < 0.01
    assert abs(dot(v,vec4(1,0,0,0))-1) < 0.01
    
    v1=vec3(3,1,4)
    v2=vec3(-5,2,9)
    v1=normalize(v1)
    v2=normalize(v2)
    v3 = cross(v1,v2)
    assert abs(dot(v1,v3)) < 0.01
    assert abs(dot(v2,v3)) < 0.01
    
    print("All tests OK")

