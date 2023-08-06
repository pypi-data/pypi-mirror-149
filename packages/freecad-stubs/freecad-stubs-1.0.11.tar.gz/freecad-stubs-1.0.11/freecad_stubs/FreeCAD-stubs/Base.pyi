import typing

import FreeCAD


class ReturnGetFormatDict(typing.TypedDict):
    Precision: int
    NumberFormat: str
    Denominator: int



# VectorPy.xml
class Vector(FreeCAD.PyObjectBase):
    """
    This class can be imported.
    This class represents a 3D float vector
    """

    @typing.overload
    def __init__(self, arg1: float = None, arg2: float = None, arg3: float = None, /): ...

    @typing.overload
    def __init__(self, arg1: FreeCAD.Vector, /): ...

    @typing.overload
    def __init__(self, arg1, /):
        """
        This class represents a 3D float vector
        Possible exceptions: (TypeError).
        """

    @property
    def Length(self) -> float:
        """
        Length([Float]) -> Float
        						  gets or sets the length of this vector
        """

    @Length.setter
    def Length(self, value: float): ...

    @property
    def x(self) -> float:
        """
        x([Float]) -> Float
        						  gets or sets the X component of this vector
        """

    @x.setter
    def x(self, value: float): ...

    @property
    def y(self) -> float:
        """
        y([Float]) -> Float
        						  gets or sets the Y component of this vector
        """

    @y.setter
    def y(self, value: float): ...

    @property
    def z(self) -> float:
        """
        z([Float]) -> Float
        						  gets or sets the Z component of this vector
        """

    @z.setter
    def z(self, value: float): ...

    def __reduce__(self) -> tuple[object, tuple[float, float, float]]:
        """
        __reduce__()
                              Serialization of Vector objects
        """

    def add(self, Vector: FreeCAD.Vector, /) -> FreeCAD.Vector:
        """
        add(Vector)
        					      returns the sum of this and another vector
        """

    def cross(self, Vector: FreeCAD.Vector, /) -> FreeCAD.Vector:
        """
        cross(Vector)
        					      returns the cross product between this and another vector
        """

    def distanceToLine(self, Vector, Vector2, /) -> float:
        """
        distanceToLine(Vector,Vector)
        						  returns the distance between this vector and a line defined by
        						  a base point and a direction
				
        Possible exceptions: (TypeError).
        """

    def distanceToLineSegment(self, Vector, Vector2, /) -> FreeCAD.Vector:
        """
        distanceToLineSegment(Vector,Vector)
        						  returns the distance between this vector and a line segment defined by
        						  a base point and a direction
				
        Possible exceptions: (TypeError).
        """

    def distanceToPlane(self, Vector, Vector2, /) -> float:
        """
        distanceToPlane(Vector,Vector)
        						  returns the distance between this vector and a plane defined by
        						  a base point and a normal
				
        Possible exceptions: (TypeError).
        """

    def distanceToPoint(self, Vector: FreeCAD.Vector, /) -> float:
        """
        distanceToPoint(Vector)
        					returns the distance to another point
        """

    def dot(self, Vector: FreeCAD.Vector, /) -> float:
        """
        dot(Vector)
        						  returns the dot product of the this vector with another one
        """

    def getAngle(self, Vector: FreeCAD.Vector, /) -> float:
        """
        getAngle(Vector)
        					      returns the angle in radians between this and another vector
        """

    def isEqual(self, Vector: FreeCAD.Vector, tolerance: float, /) -> bool:
        """
        isEqual(Vector, tolerance) -> Boolean
                                  If the distance to the given point is less or equal to the tolerance
                                  bith points are considered equal.
        """

    def isOnLineSegment(self, Vector, Vector2, /) -> bool:
        """
        isOnLineSegment(Vector, Vector)
        					      checks if Vector is on a line segment
				
        Possible exceptions: (TypeError).
        """

    def multiply(self, Float: float, /) -> FreeCAD.Vector:
        """
        multiply(Float)
        					      multiplies (scales) this vector by a single factor
        """

    def negative(self) -> FreeCAD.Vector:
        """
        negative()
        					      returns the negative (opposite) of this vector
        """

    def normalize(self) -> FreeCAD.Vector:
        """
        normalize()
        						  normalizes the vector to the length of 1.0
				
        Possible exceptions: (FreeCAD.Base.FreeCADError).
        """

    def projectToLine(self, Vector_pnt, Vector_vec, /) -> FreeCAD.Vector:
        """
        projectToLine(Vector pnt,Vector vec)
        						  Projects the point 'pnt' on a line that goes through the origin with the direction vector 'vec'.
        						  The result is the vector from point 'pnt' to the projected point.
        						  NOTE: The result does not depend on the vector instance 'self'.
        						  NOTE: This method modifies the vector instance 'self'.
				
        Possible exceptions: (TypeError).
        """

    def projectToPlane(self, Vector, Vector2, /) -> FreeCAD.Vector:
        """
        projectToPlane(Vector,Vector)
        						  projects the vector on a plane defined by a base point and a normal
				
        Possible exceptions: (TypeError).
        """

    def scale(self, Float: float, Float2: float, Float3: float, /) -> FreeCAD.Vector:
        """
        scale(Float,Float,Float)
        					      scales (multiplies) this vector by a factor
        """

    def sub(self, Vector: FreeCAD.Vector, /) -> FreeCAD.Vector:
        """
        sub(Vector)
        					      returns the difference of this and another vector
        """

    def __eq__(self, other) -> bool: ...

    def __ne__(self, other) -> bool: ...

    def __lt__(self, other) -> bool: ...

    def __le__(self, other) -> bool: ...

    def __ge__(self, other) -> bool: ...

    def __gt__(self, other) -> bool: ...

    def __add__(self, other) -> Vector: ...

    def __sub__(self, other) -> Vector: ...

    def __mul__(self, other) -> Vector: ...

    def __floordiv__(self, other): ...

    def __divmod__(self, other): ...

    def __truediv__(self, other) -> Vector: ...

    def __pow__(self, power, modulo=None): ...

    def __neg__(self) -> Vector: ...

    def __pos__(self) -> Vector: ...

    def __abs__(self) -> Vector: ...

    def __invert__(self): ...

    def __lshift__(self, other): ...

    def __rshift__(self, other): ...

    def __and__(self, other): ...

    def __xor__(self, other): ...

    def __or__(self, other): ...

    def __int__(self): ...

    def __float__(self): ...


# RotationPy.xml
class Rotation(FreeCAD.PyObjectBase):
    """
    This class can be imported.

    				A Rotation using a quaternion.
    				The Rotation object can be created by:
    				-- an empty parameter list
    				-- a Rotation object
    				-- a Vector (axis) and a float (angle)
    				-- two Vectors (rotation from/to vector)
    				-- three floats (Euler angles) as yaw-pitch-roll in XY'Z'' convention
                    -- one string and three floats (Euler angles) as euler rotation 
                       of a given type. Call toEulerSequence() for supported sequence types.
    				-- four floats (Quaternion) where the quaternion is specified as:
    				   q=xi+yj+zk+w, i.e. the last parameter is the real part
    				-- three vectors that define rotated axes directions + an optional
    				   3-characher string of capital letters 'X', 'Y', 'Z' that sets the
    				   order of importance of the axes (e.g., 'ZXY' means z direction is
    				   followed strictly, x is used but corrected if necessary, y is ignored).
    """

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, arg1: FreeCAD.Rotation, /): ...

    @typing.overload
    def __init__(self, arg1: FreeCAD.Matrix, /): ...

    @typing.overload
    def __init__(self, arg1: float, arg2: float, arg3: float, arg4: float, /): ...

    @typing.overload
    def __init__(self, arg1: float, arg2: float, arg3: float, /): ...

    @typing.overload
    def __init__(self, arg1: str, arg2: float, arg3: float, arg4: float, /): ...

    @typing.overload
    def __init__(self, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float, arg6: float, arg7: float, arg8: float, arg9: float, arg10: float, arg11: float, arg12: float, arg13: float, arg14: float, arg15: float, arg16: float, /): ...

    @typing.overload
    def __init__(self, arg1: float, arg2: float, arg3: float, arg4: float, arg5: float, arg6: float, arg7: float, arg8: float, arg9: float, /): ...

    @typing.overload
    def __init__(self, arg1: FreeCAD.Vector, arg2: FreeCAD.Vector, /): ...

    @typing.overload
    def __init__(self, arg1: FreeCAD.Vector, arg2: FreeCAD.Vector, arg3: FreeCAD.Vector, arg4: str = None, /): ...

    @typing.overload
    def __init__(self, Axis: FreeCAD.Vector, Degree: float): ...

    @typing.overload
    def __init__(self, Axis: FreeCAD.Vector, Radian: float):
        """
        A Rotation using a quaternion.
        				The Rotation object can be created by:
        				-- an empty parameter list
        				-- a Rotation object
        				-- a Vector (axis) and a float (angle)
        				-- two Vectors (rotation from/to vector)
        				-- three floats (Euler angles) as yaw-pitch-roll in XY'Z'' convention
                        -- one string and three floats (Euler angles) as euler rotation 
                           of a given type. Call toEulerSequence() for supported sequence types.
        				-- four floats (Quaternion) where the quaternion is specified as:
        				   q=xi+yj+zk+w, i.e. the last parameter is the real part
        				-- three vectors that define rotated axes directions + an optional
        				   3-characher string of capital letters 'X', 'Y', 'Z' that sets the
        				   order of importance of the axes (e.g., 'ZXY' means z direction is
        				   followed strictly, x is used but corrected if necessary, y is ignored).
			
        Possible exceptions: (FreeCAD.Base.FreeCADError, TypeError).
        """

    @property
    def Angle(self) -> float:
        """The rotation angle of the quaternion"""

    @Angle.setter
    def Angle(self, value: float): ...

    @property
    def Axis(self) -> FreeCAD.Vector:
        """The rotation axis of the quaternion"""

    @Axis.setter
    def Axis(self, value: FreeCAD.Vector): ...

    @property
    def Q(self) -> tuple[float, float, float, float]:
        """The rotation elements (as quaternion)"""

    @Q.setter
    def Q(self, value: tuple[float, float, float, float]): ...

    @property
    def RawAxis(self) -> FreeCAD.Vector:
        """The rotation axis without normalization"""

    def getYawPitchRoll(self) -> tuple[float, float, float]:
        """
        getYawPitchRoll() -> list
        					Get the Euler angles of this rotation
        					as yaw-pitch-roll in XY'Z'' convention
                            NOTE: The angles are in degree
        """

    def invert(self):
        """
        invert() -> None
                            Sets the rotation to its inverse
        """

    def inverted(self) -> FreeCAD.Rotation:
        """
        inverted() -> Rotation
                            Returns the inverse of the rotation
        """

    def isIdentity(self) -> bool:
        """
        isIdentity() -> Bool
                            returns True if the rotation equals the unity matrix
        """

    def isNull(self) -> bool:
        """
        isNull() -> Bool
                            returns True if all Q values are zero
        """

    def isSame(self, Rotation: FreeCAD.Rotation, tolerance: float = 0, /) -> bool:
        """
        isSame(Rotation, [tolerance=0])
                            Checks if the two quaternions perform the same rotation.
                            Optionally, a tolerance value greater than zero can be passed.
        """

    def multVec(self, Vector: FreeCAD.Vector, /) -> FreeCAD.Vector:
        """
        multVec(Vector) -> Vector
        					Compute the transformed vector using the rotation
        """

    def multiply(self, Rotation: FreeCAD.Rotation, /) -> FreeCAD.Rotation:
        """
        multiply(Rotation)
        					Multiply this quaternion with another quaternion
        """

    def setEulerAngles(self, seq: str, angle1: float, angle2: float, angle3: float, /):
        """
        setEulerAngles(seq, angle1, angle2, angle3)
                        Set the Euler angles in a given sequence for this rotation.
                        'seq' is the Euler sequence name. You get all possible values with toEulerAngles()
        """

    def setYawPitchRoll(self, angle1: float, angle2: float, angle3: float, /):
        """
        setYawPitchRoll(angle1, angle2, angle3)
                            Set the Euler angles of this rotation
                            as yaw-pitch-roll in XY'Z'' convention.

                            NOTE: The angles are in degree
        """

    def slerp(self, Rotation: FreeCAD.Rotation, Float: float, /) -> FreeCAD.Rotation:
        """
        slerp(Rotation, Float) -> Rotation
        					Spherical linear interpolation of this and a given rotation. The float must be in the range of 0 and 1
        """

    def toEulerAngles(self, seq: str = '', /) -> list[str] | tuple[float, float, float]:
        """
        toEulerAngles(seq='') -> list
                            Get the Euler angles in a given sequence for this rotation.
                            Call this function without arguments to output all possible values of 'seq'.
        """

    def toMatrix(self) -> FreeCAD.Matrix:
        """
        toMatrix()
        					convert the rotation to a matrix representation
        """

    def __eq__(self, other) -> bool: ...

    def __ne__(self, other) -> bool: ...

    def __lt__(self, other) -> bool: ...

    def __le__(self, other) -> bool: ...

    def __ge__(self, other) -> bool: ...

    def __gt__(self, other) -> bool: ...

    def __add__(self, other) -> Rotation: ...

    def __sub__(self, other) -> Rotation: ...

    def __mul__(self, other) -> Rotation: ...

    def __floordiv__(self, other): ...

    def __divmod__(self, other): ...

    def __truediv__(self, other) -> Rotation: ...

    def __pow__(self, power, modulo=None): ...

    def __neg__(self) -> Rotation: ...

    def __pos__(self) -> Rotation: ...

    def __abs__(self) -> Rotation: ...

    def __invert__(self): ...

    def __lshift__(self, other): ...

    def __rshift__(self, other): ...

    def __and__(self, other): ...

    def __xor__(self, other): ...

    def __or__(self, other): ...

    def __int__(self): ...

    def __float__(self): ...


# PersistencePy.xml
class Persistence(FreeCAD.BaseClass):
    """This is a persistence class"""

    @property
    def Content(self) -> str:
        """Content of the object in XML representation"""

    @property
    def MemSize(self) -> int:
        """Memory size of the object in byte"""

    def dumpContent(self, Compression: int = 1-9):
        """
        Dumps the content of the object, both the XML representation as well as the additional datafiles  
        required, into a byte representation. It will be returned as byte array.
        dumpContent() -- returns a byte array with full content
        dumpContent(Compression=1-9) -- Sets the data compression from 0 (no) to 9 (max)
                
        Possible exceptions: (NotImplementedError, IOError).
        """

    def restoreContent(self, buffer, /):
        """
        Restore the content of the object from a byte representation as stored by "dumpContent".
        It could be restored from any python object implementing the buffer protocol.
        restoreContent(buffer) -- restores from the given byte array
                
        Possible exceptions: (TypeError, IOError).
        """


# BoundBoxPy.xml
class BoundBox(FreeCAD.PyObjectBase):
    """
    This class can be imported.
    Bound box class
    A bounding box is an orthographic cube which is a way to describe outer boundaries.
    You get a bounding box from a lot of 3D types. It is often used to check if a 3D
    entity lies in the range of another object. Checking for bounding interference first
    can save a lot of computing time!

    Constructor:
    App.BoundBox([Xmin,Ymin,Zmin,Xmax,Ymax,Zmax])
    App.BoundBox(Tuple, Tuple)
    App.BoundBox(Vector, Vector)
    App.BoundBox(BoundBox)
    """

    @typing.overload
    def __init__(self, Xmin: float, Ymin: float = None, Zmin: float = None, Xmax: float = None, Ymax: float = None, Zmax: float = None, /): ...

    @typing.overload
    def __init__(self, Tuple: tuple, Tuple2: tuple, /): ...

    @typing.overload
    def __init__(self, Tuple: FreeCAD.Vector, Tuple2: FreeCAD.Vector, /): ...

    @typing.overload
    def __init__(self, Vector: tuple, Vector2: tuple, /): ...

    @typing.overload
    def __init__(self, Vector: FreeCAD.Vector, Vector2: FreeCAD.Vector, /): ...

    @typing.overload
    def __init__(self, BoundBox: FreeCAD.BoundBox, /):
        """
        Bound box class
        A bounding box is an orthographic cube which is a way to describe outer boundaries.
        You get a bounding box from a lot of 3D types. It is often used to check if a 3D
        entity lies in the range of another object. Checking for bounding interference first
        can save a lot of computing time!

        Constructor:
        App.BoundBox([Xmin,Ymin,Zmin,Xmax,Ymax,Zmax])
        App.BoundBox(Tuple, Tuple)
        App.BoundBox(Vector, Vector)
        App.BoundBox(BoundBox)
	  
        Possible exceptions: (TypeError).
        """

    @property
    def Center(self) -> FreeCAD.Vector:
        """Center point of the bounding box"""

    @property
    def DiagonalLength(self) -> float:
        """Diagonal length of the BoundBox"""

    @property
    def XLength(self) -> float:
        """Length of the BoundBox in x direction"""

    @property
    def XMax(self) -> float:
        """The maximum x boundary position"""

    @XMax.setter
    def XMax(self, value: float): ...

    @property
    def XMin(self) -> float:
        """The minimum x boundary position"""

    @XMin.setter
    def XMin(self, value: float): ...

    @property
    def YLength(self) -> float:
        """Length of the BoundBox in y direction"""

    @property
    def YMax(self) -> float:
        """The maximum y boundary position"""

    @YMax.setter
    def YMax(self, value: float): ...

    @property
    def YMin(self) -> float:
        """The minimum y boundary position"""

    @YMin.setter
    def YMin(self, value: float): ...

    @property
    def ZLength(self) -> float:
        """Length of the BoundBox in z direction"""

    @property
    def ZMax(self) -> float:
        """The maximum z boundary position"""

    @ZMax.setter
    def ZMax(self, value: float): ...

    @property
    def ZMin(self) -> float:
        """The minimum z boundary position"""

    @ZMin.setter
    def ZMin(self, value: float): ...

    @typing.overload
    def add(self, BoundBox: tuple, /): ...

    @typing.overload
    def add(self, BoundBox: FreeCAD.Vector, /): ...

    @typing.overload
    def add(self, BoundBox: FreeCAD.BoundBox, /):
        """
        method add(BoundBox)
        Add (enlarge) the given BoundBox
        Possible exceptions: (TypeError).
        """

    @typing.overload
    def closestPoint(self, Vector: tuple, /) -> FreeCAD.Vector: ...

    @typing.overload
    def closestPoint(self, Vector: FreeCAD.Vector, /) -> FreeCAD.Vector:
        """
        method closestPoint(Vector)
        Get the closest point of the bounding box to the given point
        
        Possible exceptions: (TypeError).
        """

    def enlarge(self, Float: float, /):
        """
        method enlarge(Float)
        Enlarge the BoundBox by the given value in each direction.
        A negative value shrinks the box.
        """

    def getEdge(self, Int: int, /) -> tuple[FreeCAD.Vector, FreeCAD.Vector]:
        """
        method getEdge(Int)
        Get the edge points of the given index. The index must be in the range of [0,11]
        """

    def getIntersectionPoint(self, Vector_Base: FreeCAD.Vector, Vector_Dir: FreeCAD.Vector, float_epsilon: float = 0.0001, /) -> FreeCAD.Vector:
        """
        method Vector getIntersectionPoint(Vector Base, Vector Dir, [float epsilon=0.0001])
        Calculate the intersection point of a line with the BoundBox
        The Base point must lie inside the bounding box, if not an
        exception is thrown.
			  
        Possible exceptions: (FreeCAD.Base.FreeCADError).
        """

    def getPoint(self, Int: int, /) -> FreeCAD.Vector:
        """
        method getPoint(Int)
        Get the point of the given index. The index must be in the range of [0,7]
        """

    def intersect(self, BoundBox_Vector_Base: FreeCAD.Vector, Vector_Dir: FreeCAD.Vector, /) -> bool:
        """
        method intersect(BoundBox|Vector Base, Vector Dir)
        Checks if the given object intersects with the BoundBox. That can be:
        - Another BoundBox
        - A line, specified by Base and Dir
		
        Possible exceptions: (TypeError).
        """

    def intersected(self, BoundBox: FreeCAD.BoundBox, /) -> FreeCAD.BoundBox:
        """
        method intersected(BoundBox)
        Returns the intersection of this and the given bounding box.
        """

    def isCutPlane(self, Vector_Base: FreeCAD.Vector, Vector_Normal: FreeCAD.Vector, /) -> bool:
        """
        method bool isCutPlane(Vector Base, Vector Normal)
        Check if the plane specified by Base and Normal intersects (cuts) the BoundBox
        """

    @typing.overload
    def isInside(self, Vector_Base_BoundBox_box: tuple, /) -> bool: ...

    @typing.overload
    def isInside(self, Vector_Base_BoundBox_box: FreeCAD.Vector, /) -> bool: ...

    @typing.overload
    def isInside(self, Vector_Base_BoundBox_box: FreeCAD.BoundBox, /) -> bool:
        """
        method bool isInside(Vector Base|BoundBox box)
        Check if the point or bounding box is inside this bounding box
				
        Possible exceptions: (TypeError).
        """

    def isValid(self) -> bool:
        """
        method isValid()
        Checks if the bounding box is valid
        """

    @typing.overload
    def move(self, Vector: tuple, /): ...

    @typing.overload
    def move(self, Vector: FreeCAD.Vector, /):
        """
        method move(Vector)
        Move the BoundBox by the given vector
			  
        Possible exceptions: (TypeError).
        """

    def scale(self, x: float, y: float, z: float, /):
        """
        method scale(x,y,z)
        Scale the BoundBox by the given values in x, y and z
			  
        Possible exceptions: (TypeError).
        """

    def setVoid(self):
        """
        method setVoid()
        Invalidate the bounding box
        """

    def transformed(self, Matrix: FreeCAD.Matrix, /) -> FreeCAD.BoundBox:
        """
        method transformed(Matrix)
        Return a new bounding box with the transformed corner of this bounding box
			  
        Possible exceptions: (FloatingPointError).
        """

    def united(self, BoundBox: FreeCAD.BoundBox, /) -> FreeCAD.BoundBox:
        """
        method united(BoundBox)
        Returns the union of this and the given bounding box.
        """


# PlacementPy.xml
class Placement(FreeCAD.PyObjectBase):
    """
    This class can be imported.
    Placement
    A placement defines an orientation (rotation) and a position (base) in 3D space.
    It is used when no scaling or other distortion is needed.

    The following constructors are supported:
    Placement() -- empty constructor
    Placement(Placement) -- copy constructor
    Placement(Matrix) -- 4D matrix consisting of rotation and translation
    Placement(Base, Rotation) -- define position and rotation
    Placement(Base, Rotation,Center) -- define position and rotation with center
    Placement(Base, Axis, Angle) -- define position and rotation
    """

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, Placement: FreeCAD.Matrix, /): ...

    @typing.overload
    def __init__(self, Placement: FreeCAD.Placement, /): ...

    @typing.overload
    def __init__(self, Matrix: FreeCAD.Matrix, /): ...

    @typing.overload
    def __init__(self, Matrix: FreeCAD.Placement, /): ...

    @typing.overload
    def __init__(self, Base: FreeCAD.Vector, Rotation: FreeCAD.Rotation, /): ...

    @typing.overload
    def __init__(self, Base: FreeCAD.Vector, Rotation: FreeCAD.Vector, Center: float, /): ...

    @typing.overload
    def __init__(self, Base: FreeCAD.Vector, Rotation: FreeCAD.Rotation, Center: FreeCAD.Vector, /): ...

    @typing.overload
    def __init__(self, Base: FreeCAD.Vector, Axis: FreeCAD.Vector, Angle: float, /): ...

    @typing.overload
    def __init__(self, Base: FreeCAD.Vector, Axis: FreeCAD.Rotation, Angle: FreeCAD.Vector, /):
        """
        Placement
        A placement defines an orientation (rotation) and a position (base) in 3D space.
        It is used when no scaling or other distortion is needed.

        The following constructors are supported:
        Placement() -- empty constructor
        Placement(Placement) -- copy constructor
        Placement(Matrix) -- 4D matrix consisting of rotation and translation
        Placement(Base, Rotation) -- define position and rotation
        Placement(Base, Rotation,Center) -- define position and rotation with center
        Placement(Base, Axis, Angle) -- define position and rotation
		
        Possible exceptions: (TypeError).
        """

    @property
    def Base(self) -> FreeCAD.Vector:
        """Vector to the Base Position of the Placement"""

    @Base.setter
    def Base(self, value: FreeCAD.Vector): ...

    @property
    def Matrix(self) -> FreeCAD.Matrix:
        """Set/get matrix representation of this placement"""

    @Matrix.setter
    def Matrix(self, value: FreeCAD.Matrix): ...

    @property
    def Rotation(self) -> FreeCAD.Rotation:
        """Orientation of the placement expressed as rotation"""

    @Rotation.setter
    def Rotation(self, value: FreeCAD.Rotation): ...

    def copy(self) -> FreeCAD.Placement:
        """
        copy()
                            Returns a copy of this Placement
        """

    def inverse(self) -> FreeCAD.Placement:
        """
        inverse() -> Placement
        					compute the inverse placement
        """

    def isIdentity(self) -> bool:
        """
        isIdentity() -> Bool
        					returns True if the placement has no displacement and no rotation
        """

    def move(self, Vector: FreeCAD.Vector, /):
        """
        move(Vector) 
        					Move the placement along the vector
        """

    def multVec(self, arg1: FreeCAD.Vector, /) -> FreeCAD.Vector:
        """
        multVector(Vector) -> Vector
        					Compute the transformed vector using the placement
        """

    def multiply(self, Placement: FreeCAD.Placement, /) -> FreeCAD.Placement:
        """
        multiply(Placement)
        					Multiply this placement with another placement
        """

    def pow(self, t: float, shorten: bool = True, /) -> FreeCAD.Placement:
        """
        pow(t, shorten = true): raise this placement to real power using ScLERP interpolation.
                            If 'shorten' is true, ensures rotation quaternion is net positive, to make the path shorter.
                            Also available as ** operator.
        """

    def rotate(self, center, axis, degree: float, /):
        """
        rotate(center,axis,degree) - rotate the current placement around center and axis with degree
                        This method is compatible with TopoShape.rotate()
        """

    def sclerp(self, placement2: FreeCAD.Placement, t: float, shorten: bool = True, /) -> FreeCAD.Placement:
        """
        sclerp(placement2, t, shorten = True): interpolate between self and placement2.
                            Interpolation is a continuous motion along a helical path, made of equal transforms if discretized.
                            t = 0.0 - return self. t = 1.0 - return placement2. t can also be outside of 0..1 range, for extrapolation.
                            If quaternions of rotations of the two placements differ in sign, the interpolation will 
                             take a long path. If 'shorten' is true, the signs are harmonized before interpolation, and the 
                             interpolation takes the shorter path.
        """

    def slerp(self, arg1: FreeCAD.Placement, arg2: float, /) -> FreeCAD.Placement:
        """
        slerp(placement2, t, shorten = True): interpolate between self and placement2.
                            This function performs independent interpolation of rotation and movement.
                            Result of such interpolation might be not what application expects, thus this
                            tool might be considered for simple cases or for interpolating between small intervals.
                    
                            For more complex cases you better use the advanced sclerp() function.
        """

    def toMatrix(self) -> FreeCAD.Matrix:
        """
        toMatrix()
        					convert the placement to a matrix representation
        """

    @typing.overload
    def translate(self, Vector, /): ...

    @typing.overload
    def translate(self):
        """
        translate(Vector) 
        					alias to move(), to be compatible with TopoShape.translate()
        """

    def __eq__(self, other) -> bool: ...

    def __ne__(self, other) -> bool: ...

    def __lt__(self, other) -> bool: ...

    def __le__(self, other) -> bool: ...

    def __ge__(self, other) -> bool: ...

    def __gt__(self, other) -> bool: ...

    def __add__(self, other) -> Placement: ...

    def __sub__(self, other) -> Placement: ...

    def __mul__(self, other) -> Placement: ...

    def __floordiv__(self, other): ...

    def __divmod__(self, other): ...

    def __truediv__(self, other) -> Placement: ...

    def __pow__(self, power, modulo=None): ...

    def __neg__(self) -> Placement: ...

    def __pos__(self) -> Placement: ...

    def __abs__(self) -> Placement: ...

    def __invert__(self): ...

    def __lshift__(self, other): ...

    def __rshift__(self, other): ...

    def __and__(self, other): ...

    def __xor__(self, other): ...

    def __or__(self, other): ...

    def __int__(self): ...

    def __float__(self): ...


# UnitPy.xml
class Unit(FreeCAD.PyObjectBase):
    """
    This class can be imported.

     Unit
     defines a unit type, calculate and compare.

     The following constructors are supported:
     Unit()                        -- empty constructor
     Unit(i1,i2,i3,i4,i5,i6,i7,i8) -- unit signature
     Unit(Quantity)                -- copy unit from Quantity
     Unit(Unit)                    -- copy constructor
     Unit(string)                  -- parse the string for units
    """

    @typing.overload
    def __init__(self, i1: int = None, i2: int = None, i3: int = None, i4: int = None, i5: int = None, i6: int = None, i7: int = None, i8: int = None, /): ...

    @typing.overload
    def __init__(self, Quantity: FreeCAD.Quantity, /): ...

    @typing.overload
    def __init__(self, Quantity: FreeCAD.Unit, /): ...

    @typing.overload
    def __init__(self, Quantity: str, /): ...

    @typing.overload
    def __init__(self, Unit: FreeCAD.Quantity, /): ...

    @typing.overload
    def __init__(self, Unit: FreeCAD.Unit, /): ...

    @typing.overload
    def __init__(self, Unit: str, /): ...

    @typing.overload
    def __init__(self, string: FreeCAD.Quantity, /): ...

    @typing.overload
    def __init__(self, string: FreeCAD.Unit, /): ...

    @typing.overload
    def __init__(self, string: str, /):
        """
        Unit
         defines a unit type, calculate and compare.

         The following constructors are supported:
         Unit()                        -- empty constructor
         Unit(i1,i2,i3,i4,i5,i6,i7,i8) -- unit signature
         Unit(Quantity)                -- copy unit from Quantity
         Unit(Unit)                    -- copy constructor
         Unit(string)                  -- parse the string for units
        
        Possible exceptions: (ValueError, OverflowError, TypeError).
        """

    @property
    def Signature(self) -> tuple[int, int, int, int, int, int, int, int]:
        """Returns the signature."""

    @property
    def Type(self) -> str:
        """holds the unit type as a string, e.g. 'Area'."""

    def __eq__(self, other) -> bool: ...

    def __ne__(self, other) -> bool: ...

    def __lt__(self, other) -> bool: ...

    def __le__(self, other) -> bool: ...

    def __ge__(self, other) -> bool: ...

    def __gt__(self, other) -> bool: ...

    def __add__(self, other) -> Unit: ...

    def __sub__(self, other) -> Unit: ...

    def __mul__(self, other) -> Unit: ...

    def __floordiv__(self, other): ...

    def __divmod__(self, other): ...

    def __truediv__(self, other) -> Unit: ...

    def __pow__(self, power, modulo=None): ...

    def __neg__(self) -> Unit: ...

    def __pos__(self) -> Unit: ...

    def __abs__(self) -> Unit: ...

    def __invert__(self): ...

    def __lshift__(self, other): ...

    def __rshift__(self, other): ...

    def __and__(self, other): ...

    def __xor__(self, other): ...

    def __or__(self, other): ...

    def __int__(self): ...

    def __float__(self): ...


# QuantityPy.xml
class Quantity(FreeCAD.PyObjectBase):
    """
    This class can be imported.
    Quantity
    defined by a value and a unit.

    The following constructors are supported:
    Quantity() -- empty constructor
    Quantity(Value) -- empty constructor
    Quantity(Value,Unit) -- empty constructor
    Quantity(Quantity) -- copy constructor
    Quantity(string) -- arbitrary mixture of numbers and chars defining a Quantity
    """

    @typing.overload
    def __init__(self, Value: FreeCAD.Quantity, /): ...

    @typing.overload
    def __init__(self, Value: str, /): ...

    @typing.overload
    def __init__(self, Value: float, Unit: FreeCAD.Unit, /): ...

    @typing.overload
    def __init__(self, Value: float, Unit: FreeCAD.Quantity, /): ...

    @typing.overload
    def __init__(self, Value: float, Unit: str, /): ...

    @typing.overload
    def __init__(self, Quantity: FreeCAD.Quantity, /): ...

    @typing.overload
    def __init__(self, Quantity: str, /): ...

    @typing.overload
    def __init__(self, string: FreeCAD.Quantity, /): ...

    @typing.overload
    def __init__(self, string: str, /):
        """
        Quantity
        defined by a value and a unit.

        The following constructors are supported:
        Quantity() -- empty constructor
        Quantity(Value) -- empty constructor
        Quantity(Value,Unit) -- empty constructor
        Quantity(Quantity) -- copy constructor
        Quantity(string) -- arbitrary mixture of numbers and chars defining a Quantity
		
        Possible exceptions: (TypeError, ValueError).
        """

    @property
    def Format(self) -> ReturnGetFormatDict:
        """Format of the Quantity"""

    @Format.setter
    def Format(self, value: dict): ...

    @property
    def Unit(self) -> FreeCAD.Unit:
        """Unit of the Quantity"""

    @Unit.setter
    def Unit(self, value: FreeCAD.Unit): ...

    @property
    def UserString(self) -> str:
        """Unit of the Quantity"""

    @property
    def Value(self) -> float:
        """Numeric Value of the Quantity (in internal system mm,kg,s)"""

    @Value.setter
    def Value(self, value: float): ...

    @typing.overload
    def getValueAs(self, arg1: FreeCAD.Quantity, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, arg1: FreeCAD.Unit, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, arg1: str, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, arg1: float, arg2: FreeCAD.Unit, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, FreeCAD_Units_Pascal: FreeCAD.Quantity, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, FreeCAD_Units_Pascal: FreeCAD.Unit, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, FreeCAD_Units_Pascal: str, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, Qantity_N_m_2_: FreeCAD.Quantity, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, Qantity_N_m_2_: FreeCAD.Unit, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, Qantity_N_m_2_: str, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, Unit_0_1_0_0_0_0_0_0_: FreeCAD.Quantity, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, Unit_0_1_0_0_0_0_0_0_: FreeCAD.Unit, /) -> FreeCAD.Quantity: ...

    @typing.overload
    def getValueAs(self, Unit_0_1_0_0_0_0_0_0_: str, /) -> FreeCAD.Quantity:
        """
        returns a floating point value as the provided unit

                  Following parameters are allowed:
                  getValueAs('m/s')  # unit string to parse
                  getValueAs(2.45,1) # translatrion value and unit signature
                  getValueAs(FreeCAD.Units.Pascal) # predefined standard units 
                  getValueAs(Qantity('N/m^2')) # a quantity
                  getValueAs(Unit(0,1,0,0,0,0,0,0)) # a unit
        
        Possible exceptions: (TypeError, ValueError).
        """

    def toStr(self, decimals: int = None, /) -> str:
        """
        toStr([decimals])
                  returns a string representation rounded to number of decimals. If no decimals are specified then
                  the internal precision is used
        """

    def __eq__(self, other) -> bool: ...

    def __ne__(self, other) -> bool: ...

    def __lt__(self, other) -> bool: ...

    def __le__(self, other) -> bool: ...

    def __ge__(self, other) -> bool: ...

    def __gt__(self, other) -> bool: ...

    def __add__(self, other) -> Quantity: ...

    def __sub__(self, other) -> Quantity: ...

    def __mul__(self, other) -> Quantity: ...

    def __floordiv__(self, other): ...

    def __divmod__(self, other): ...

    def __truediv__(self, other) -> Quantity: ...

    def __pow__(self, power, modulo=None): ...

    def __neg__(self) -> Quantity: ...

    def __pos__(self) -> Quantity: ...

    def __abs__(self) -> Quantity: ...

    def __invert__(self): ...

    def __lshift__(self, other): ...

    def __rshift__(self, other): ...

    def __and__(self, other): ...

    def __xor__(self, other): ...

    def __or__(self, other): ...

    def __int__(self): ...

    def __float__(self): ...


# BaseClassPy.xml
class BaseClass(FreeCAD.PyObjectBase):
    """This is the base class"""

    @property
    def Module(self) -> str:
        """Module in which this class is defined"""

    @property
    def TypeId(self) -> str:
        """Is the type of the FreeCAD object with module domain"""

    def getAllDerivedFrom(self) -> list[str]:
        """Returns all descendants"""

    def isDerivedFrom(self, arg1: str, /) -> bool:
        """Returns true if given type is a father"""


# MatrixPy.xml
class Matrix(FreeCAD.PyObjectBase):
    """
    This class can be imported.
    A 4x4 Matrix
    """

    @typing.overload
    def __init__(self, arg1: float = None, arg2: float = None, arg3: float = None, arg4: float = None, arg5: float = None, arg6: float = None, arg7: float = None, arg8: float = None, arg9: float = None, arg10: float = None, arg11: float = None, arg12: float = None, arg13: float = None, arg14: float = None, arg15: float = None, arg16: float = None, /): ...

    @typing.overload
    def __init__(self, arg1: FreeCAD.Matrix, /): ...

    @typing.overload
    def __init__(self, arg1: FreeCAD.Vector, arg2: FreeCAD.Vector, arg3: FreeCAD.Vector, arg4: FreeCAD.Vector = None, /):
        """
        A 4x4 Matrix
        Possible exceptions: (TypeError).
        """

    @property
    def A(self) -> typing.Sequence:
        """The matrix elements"""

    @A.setter
    def A(self, value: typing.Sequence): ...

    @property
    def A11(self) -> float:
        """The matrix elements"""

    @A11.setter
    def A11(self, value: float): ...

    @property
    def A12(self) -> float:
        """The matrix elements"""

    @A12.setter
    def A12(self, value: float): ...

    @property
    def A13(self) -> float:
        """The matrix elements"""

    @A13.setter
    def A13(self, value: float): ...

    @property
    def A14(self) -> float:
        """The matrix elements"""

    @A14.setter
    def A14(self, value: float): ...

    @property
    def A21(self) -> float:
        """The matrix elements"""

    @A21.setter
    def A21(self, value: float): ...

    @property
    def A22(self) -> float:
        """The matrix elements"""

    @A22.setter
    def A22(self, value: float): ...

    @property
    def A23(self) -> float:
        """The matrix elements"""

    @A23.setter
    def A23(self, value: float): ...

    @property
    def A24(self) -> float:
        """The matrix elements"""

    @A24.setter
    def A24(self, value: float): ...

    @property
    def A31(self) -> float:
        """The matrix elements"""

    @A31.setter
    def A31(self, value: float): ...

    @property
    def A32(self) -> float:
        """The matrix elements"""

    @A32.setter
    def A32(self, value: float): ...

    @property
    def A33(self) -> float:
        """The matrix elements"""

    @A33.setter
    def A33(self, value: float): ...

    @property
    def A34(self) -> float:
        """The matrix elements"""

    @A34.setter
    def A34(self, value: float): ...

    @property
    def A41(self) -> float:
        """The matrix elements"""

    @A41.setter
    def A41(self, value: float): ...

    @property
    def A42(self) -> float:
        """The matrix elements"""

    @A42.setter
    def A42(self, value: float): ...

    @property
    def A43(self) -> float:
        """The matrix elements"""

    @A43.setter
    def A43(self, value: float): ...

    @property
    def A44(self) -> float:
        """The matrix elements"""

    @A44.setter
    def A44(self, value: float): ...

    def analyze(self) -> str:
        """
        analyze() -> string
        Analyzes the type of transformation.
        """

    def col(self, index: int, /) -> FreeCAD.Vector:
        """
        col(index)
        Return the vector of a column
        
        Possible exceptions: (TypeError).
        """

    def determinant(self) -> float:
        """
        determinant() -> Float
        Compute the determinant of the matrix
        """

    def hasScale(self, tol: float = 0.0, /):
        """
        hasScale(tol=0.0)
        Return an enum value of ScaleType. Possible values are:
        Uniform, NonUniformLeft, NonUniformRight, NoScaling or Other
        if it's not a scale matrix
        """

    def inverse(self) -> FreeCAD.Matrix:
        """
        inverse() -> Matrix
        Compute the inverse matrix, if possible
        
        Possible exceptions: (FreeCAD.Base.FreeCADError).
        """

    def invert(self):
        """
        invert() -> None
        Compute the inverse matrix, if possible
        
        Possible exceptions: (FreeCAD.Base.FreeCADError).
        """

    def isNull(self) -> bool:
        """isNull() - check if this is the null matrix"""

    def isOrthogonal(self, Float: float = None, /) -> float:
        """
        isOrthogonal([Float]) -> Float
        Checks if the matrix is orthogonal, i.e. M * M^T = k*I and returns
        the multiple of the identity matrix. If it's not orthogonal 0 is returned.
        As argument you can set a tolerance which by default is 1.0e-6.
        """

    def isUnity(self) -> bool:
        """isUnity() - check if this is the unit matrix"""

    @typing.overload
    def move(self, Vector: tuple, /): ...

    @typing.overload
    def move(self, Vector: FreeCAD.Vector, /):
        """
        move(Vector)
        Move the matrix along the vector
        """

    def multVec(self, Vector: FreeCAD.Vector, /) -> FreeCAD.Vector:
        """
        multVec(Vector) -> Vector
        Compute the transformed vector using the matrix
        """

    @typing.overload
    def multiply(self, Matrix_Vector: FreeCAD.Matrix, /) -> FreeCAD.Matrix | FreeCAD.Vector: ...

    @typing.overload
    def multiply(self, Matrix_Vector: FreeCAD.Vector, /) -> FreeCAD.Matrix | FreeCAD.Vector:
        """
        multiply(Matrix|Vector)
        Multiply a matrix or vector with this matrix
        
        Possible exceptions: (TypeError).
        """

    def nullify(self):
        """nullify() - make this the null matrix"""

    @typing.overload
    def rotateX(self, float: FreeCAD.Quantity, /): ...

    @typing.overload
    def rotateX(self, float: float, /):
        """
        rotateX(float) - rotate around X
        Possible exceptions: (TypeError).
        """

    @typing.overload
    def rotateY(self, float: FreeCAD.Quantity, /): ...

    @typing.overload
    def rotateY(self, float: float, /):
        """
        rotateY(float) - rotate around Y
        Possible exceptions: (TypeError).
        """

    @typing.overload
    def rotateZ(self, float: FreeCAD.Quantity, /): ...

    @typing.overload
    def rotateZ(self, float: float, /):
        """
        rotateZ(float) - rotate around Z
        Possible exceptions: (TypeError).
        """

    def row(self, index: int, /) -> FreeCAD.Vector:
        """
        row(index)
        Return the vector of a row
        
        Possible exceptions: (TypeError).
        """

    @typing.overload
    def scale(self, Vector: float, /): ...

    @typing.overload
    def scale(self, Vector: tuple, /): ...

    @typing.overload
    def scale(self, Vector: FreeCAD.Vector, /):
        """
        scale(Vector)
        Scale the matrix with the vector
        """

    def setCol(self, index: int, Vector: FreeCAD.Vector, /):
        """
        setCol(index, Vector)
        Set the vector of a column
        
        Possible exceptions: (TypeError).
        """

    def setRow(self, index: int, Vector: FreeCAD.Vector, /):
        """
        setRow(index, Vector)
        Set the vector of a row
        
        Possible exceptions: (TypeError).
        """

    def setTrace(self, Vector: FreeCAD.Vector, /):
        """
        setTrace(Vector)
        Set the trace of the 3x3 sub-matrix
        
        Possible exceptions: (TypeError).
        """

    def submatrix(self, int: int, /) -> FreeCAD.Matrix:
        """
        submatrix(int) -> Matrix
        Get the sub-matrix. The parameter must be in the range [1,4].
        
        Possible exceptions: (IndexError).
        """

    def trace(self) -> FreeCAD.Vector:
        """
        trace()
        Return the trace of the 3x3 sub-matrix as vector
        """

    def transform(self, Vector: FreeCAD.Vector, Matrix: FreeCAD.Matrix, /):
        """transform(Vector,Matrix) - return the dot product of the two vectors"""

    def transpose(self):
        """
        transpose() -> None
        Transpose the matrix.
        """

    def transposed(self) -> FreeCAD.Matrix:
        """
        transposed() -> Matrix
        Returns a transposed copy of this matrix.
        """

    def unity(self):
        """unity() - make this matrix to unity"""

    def __eq__(self, other) -> bool: ...

    def __ne__(self, other) -> bool: ...

    def __lt__(self, other) -> bool: ...

    def __le__(self, other) -> bool: ...

    def __ge__(self, other) -> bool: ...

    def __gt__(self, other) -> bool: ...

    def __add__(self, other) -> Matrix: ...

    def __sub__(self, other) -> Matrix: ...

    def __mul__(self, other) -> Matrix: ...

    def __floordiv__(self, other): ...

    def __divmod__(self, other): ...

    def __truediv__(self, other) -> Matrix: ...

    def __pow__(self, power, modulo=None): ...

    def __neg__(self) -> Matrix: ...

    def __pos__(self) -> Matrix: ...

    def __abs__(self) -> Matrix: ...

    def __invert__(self): ...

    def __lshift__(self, other): ...

    def __rshift__(self, other): ...

    def __and__(self, other): ...

    def __xor__(self, other): ...

    def __or__(self, other): ...

    def __int__(self): ...

    def __float__(self): ...


# CoordinateSystemPy.xml
class CoordinateSystem(FreeCAD.PyObjectBase):
    """This class can be imported."""

    @property
    def Axis(self) -> FreeCAD.Axis:
        """Set or get axis"""

    @Axis.setter
    def Axis(self, value: FreeCAD.Axis): ...

    @property
    def Position(self) -> FreeCAD.Vector:
        """Set or get position"""

    @Position.setter
    def Position(self, value: FreeCAD.Vector): ...

    @property
    def XDirection(self) -> FreeCAD.Vector:
        """Set or get x direction"""

    @XDirection.setter
    def XDirection(self, value: FreeCAD.Vector): ...

    @property
    def YDirection(self) -> FreeCAD.Vector:
        """Set or get y direction"""

    @YDirection.setter
    def YDirection(self, value: FreeCAD.Vector): ...

    @property
    def ZDirection(self) -> FreeCAD.Vector:
        """Set or get z direction"""

    @ZDirection.setter
    def ZDirection(self, value: FreeCAD.Vector): ...

    def displacement(self, CoordinateSystem: FreeCAD.CoordinateSystem, /) -> FreeCAD.Placement:
        """
        displacement(CoordinateSystem)
        Computes the placement from this to the passed coordinate system
        """

    @typing.overload
    def setAxes(self, Axis_or_Vector_z: FreeCAD.Axis, Vector_x: FreeCAD.Vector, /): ...

    @typing.overload
    def setAxes(self, Axis_or_Vector_z: FreeCAD.Vector, Vector_x: FreeCAD.Vector, /):
        """
        setAxes(Axis or Vector z, Vector x)
        Set axis or z direction and x direction
        Possible exceptions: (TypeError).
        """

    def setPlacement(self, arg1: FreeCAD.Placement, /):
        """
        setPlacment(Placement)
        Set placement to the coordinate system.
        """

    @typing.overload
    def transform(self, Rotation_or_Placement: FreeCAD.Placement, /): ...

    @typing.overload
    def transform(self, Rotation_or_Placement: FreeCAD.Rotation, /):
        """
        transform(Rotation or Placement)
        Applies the rotation or placement on this coordinate system
        
        Possible exceptions: (TypeError).
        """

    def transformTo(self, Vector: FreeCAD.Vector, /) -> FreeCAD.Vector:
        """
        transformTo(Vector)
        Computes the coordinates of the point in coordinates of this system
        """


# TypePy.xml
class TypeId(FreeCAD.PyObjectBase):
    """
    This class can be imported.
    This is the Type class
    """

    @property
    def Key(self) -> int:
        """The key of the type id"""

    @property
    def Module(self) -> str:
        """Module in which this class is defined"""

    @property
    def Name(self) -> str:
        """The name of the type id"""

    def createInstance(self):
        """Creates an instance of this type"""

    @staticmethod
    def createInstanceByName(arg0: str, arg1: bool = None, /) -> FreeCAD.BaseClass:
        """Creates an instance of the named type"""

    @staticmethod
    def fromKey(arg0: int, /) -> FreeCAD.TypeId:
        """Returns a type object by key"""

    @staticmethod
    def fromName(arg0: str, /) -> FreeCAD.TypeId:
        """Returns a type object by name"""

    def getAllDerived(self) -> list[FreeCAD.TypeId]:
        """Returns all descendants"""

    @staticmethod
    @typing.overload
    def getAllDerivedFrom(arg0: str, /) -> list[FreeCAD.TypeId]: ...

    @staticmethod
    @typing.overload
    def getAllDerivedFrom(arg0: FreeCAD.TypeId, /) -> list[FreeCAD.TypeId]:
        """
        Returns all descendants
        Possible exceptions: (TypeError).
        """

    @staticmethod
    def getBadType() -> FreeCAD.TypeId:
        """Returns an invalid type id"""

    @staticmethod
    def getNumTypes() -> int:
        """Returns the number of type ids"""

    def getParent(self) -> FreeCAD.TypeId:
        """Returns the parent type id"""

    def isBad(self) -> bool:
        """Checks if the type id is invalid"""

    @typing.overload
    def isDerivedFrom(self, arg1: str, /) -> bool: ...

    @typing.overload
    def isDerivedFrom(self, arg1: FreeCAD.TypeId, /) -> bool:
        """
        Returns true if given type is a father
        Possible exceptions: (TypeError).
        """


# AxisPy.xml
class Axis(FreeCAD.PyObjectBase):
    """
    This class can be imported.
    Axis
    An defines a direction and a position (base) in 3D space.

    The following constructors are supported:
    Axis() -- empty constructor
    Axis(Axis) -- copy constructor
    Axis(Base, Direction) -- define position and direction
    """

    @typing.overload
    def __init__(self): ...

    @typing.overload
    def __init__(self, Axis: FreeCAD.Axis, /): ...

    @typing.overload
    def __init__(self, Base: FreeCAD.Vector, Direction, /):
        """
        Axis
        An defines a direction and a position (base) in 3D space.

        The following constructors are supported:
        Axis() -- empty constructor
        Axis(Axis) -- copy constructor
        Axis(Base, Direction) -- define position and direction
		
        Possible exceptions: (TypeError).
        """

    @property
    def Base(self) -> FreeCAD.Vector:
        """Vector to the Base position of the Axis"""

    @Base.setter
    def Base(self, value: FreeCAD.Vector): ...

    @property
    def Direction(self) -> FreeCAD.Vector:
        """Direction vector of the Axis"""

    @Direction.setter
    def Direction(self, value: FreeCAD.Vector): ...

    def copy(self) -> FreeCAD.Axis:
        """
        copy()
                            Returns a copy of this Axis
        """

    def move(self, Vector: FreeCAD.Vector, /):
        """
        move(Vector)
        					Move the axis base along the vector
        """

    def multiply(self, Placement: FreeCAD.Placement, /) -> FreeCAD.Axis:
        """
        multiply(Placement)
        					Multiply this axis with a placement
        """

    def reversed(self) -> FreeCAD.Axis:
        """
        reversed() -> Axis
        					compute the reversed axis
        """


# GeometryPyCXX.cpp
class Vector2d:
    """This class can be imported."""

    pass
# Sequencer.cpp
class ProgressIndicator:
    """
    This class can be imported.
    Progress indicator
    """

    def start(self, string: str, int: int, /) -> None:
        """start(string,int)"""

    def next(self, arg1: int = None, /) -> None:
        """next()"""

    def stop(self) -> None:
        """stop()"""
