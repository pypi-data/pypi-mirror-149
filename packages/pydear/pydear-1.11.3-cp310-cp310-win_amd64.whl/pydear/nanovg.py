from typing import Type, Tuple, Union, Any, Iterable
import ctypes
from enum import IntEnum
from .impl.nanovg import *
class _4020238307(ctypes.Structure):
    _fields_=[
        ("r", ctypes.c_float), # FloatType: float,
        ("g", ctypes.c_float), # FloatType: float,
        ("b", ctypes.c_float), # FloatType: float,
        ("a", ctypes.c_float), # FloatType: float,
    ]
class _2814254501(ctypes.Union):
    _anonymous_=[
       "_4020238307",
    ]

    _fields_=[
        ("rgba", ctypes.c_float * 4), # ArrayType: float[4],
        ("_4020238307", _4020238307), # StructType: ,
    ]
class NVGcolor(ctypes.Structure):
    _anonymous_=[
       "_2814254501",
    ]

    _fields_=[
        ("_2814254501", _2814254501), # StructType: ,
    ]
class NVGpaint(ctypes.Structure):
    _fields_=[
        ("xform", ctypes.c_float * 6), # ArrayType: float[6],
        ("extent", ctypes.c_float * 2), # ArrayType: float[2],
        ("radius", ctypes.c_float), # FloatType: float,
        ("feather", ctypes.c_float), # FloatType: float,
        ("innerColor", NVGcolor), # StructType: NVGcolor,
        ("outerColor", NVGcolor), # StructType: NVGcolor,
        ("image", ctypes.c_int32), # Int32Type: int,
    ]
class NVGtextRow(ctypes.Structure):
    _fields_=[
        ("start", ctypes.c_void_p), # CStringType: const char *,
        ("end", ctypes.c_void_p), # CStringType: const char *,
        ("next", ctypes.c_void_p), # CStringType: const char *,
        ("width", ctypes.c_float), # FloatType: float,
        ("minx", ctypes.c_float), # FloatType: float,
        ("maxx", ctypes.c_float), # FloatType: float,
    ]
class NVGglyphPosition(ctypes.Structure):
    _fields_=[
        ("str", ctypes.c_void_p), # CStringType: const char *,
        ("x", ctypes.c_float), # FloatType: float,
        ("minx", ctypes.c_float), # FloatType: float,
        ("maxx", ctypes.c_float), # FloatType: float,
    ]
class NVGdrawData(ctypes.Structure):
    _fields_=[
        ("view", ctypes.c_float * 2), # ArrayType: float[2],
        ("drawData", ctypes.c_void_p), # PointerToStructType: GLNVGcall*,
        ("drawCount", ctypes.c_uint64), # SizeType: size_t,
        ("pUniform", ctypes.c_void_p), # PointerType: void*,
        ("uniformByteSize", ctypes.c_int32), # Int32Type: int,
        ("pVertex", ctypes.c_void_p), # PointerToStructType: NVGvertex*,
        ("vertexCount", ctypes.c_int32), # Int32Type: int,
        ("pPath", ctypes.c_void_p), # PointerToStructType: GLNVGpath*,
    ]
class NVGparams(ctypes.Structure):
    _fields_=[
        ("userPtr", ctypes.c_void_p), # PointerType: void*,
        ("edgeAntiAlias", ctypes.c_int32), # Int32Type: int,
        ("renderCreateTexture", ctypes.c_void_p), # PointerType: void**,
        ("renderDeleteTexture", ctypes.c_void_p), # PointerType: void**,
        ("renderUpdateTexture", ctypes.c_void_p), # PointerType: void**,
        ("renderGetTexture", ctypes.c_void_p), # PointerType: void**,
        ("renderUniformSize", ctypes.c_void_p), # PointerType: void**,
        ("_flags", ctypes.c_int32), # Int32Type: int,
        ("_draw", ctypes.c_void_p), # PointerType: class NVGDrawImpl*,
    ]
class NVGvertex(ctypes.Structure):
    _fields_=[
        ("x", ctypes.c_float), # FloatType: float,
        ("y", ctypes.c_float), # FloatType: float,
        ("u", ctypes.c_float), # FloatType: float,
        ("v", ctypes.c_float), # FloatType: float,
    ]
class NVGtextureInfo(ctypes.Structure):
    _fields_=[
        ("_id", ctypes.c_int32), # Int32Type: int,
        ("_handle", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("_width", ctypes.c_int32), # Int32Type: int,
        ("_height", ctypes.c_int32), # Int32Type: int,
        ("_type", ctypes.c_int32), # Int32Type: int,
        ("_flags", ctypes.c_int32), # Int32Type: int,
    ]
class NVGcompositeOperationState(ctypes.Structure):
    _fields_=[
        ("srcRGB", ctypes.c_int), # EnumType: NVGblendFactor,
        ("dstRGB", ctypes.c_int), # EnumType: NVGblendFactor,
        ("srcAlpha", ctypes.c_int), # EnumType: NVGblendFactor,
        ("dstAlpha", ctypes.c_int), # EnumType: NVGblendFactor,
    ]
class GLNVGpath(ctypes.Structure):
    _fields_=[
        ("fillOffset", ctypes.c_int32), # Int32Type: int,
        ("fillCount", ctypes.c_int32), # Int32Type: int,
        ("strokeOffset", ctypes.c_int32), # Int32Type: int,
        ("strokeCount", ctypes.c_int32), # Int32Type: int,
    ]
class GLNVGcall(ctypes.Structure):
    _fields_=[
        ("type", ctypes.c_int32), # Int32Type: int,
        ("image", ctypes.c_int32), # Int32Type: int,
        ("pathOffset", ctypes.c_int32), # Int32Type: int,
        ("pathCount", ctypes.c_int32), # Int32Type: int,
        ("triangleOffset", ctypes.c_int32), # Int32Type: int,
        ("triangleCount", ctypes.c_int32), # Int32Type: int,
        ("uniformOffset", ctypes.c_int32), # Int32Type: int,
        ("blendFunc", NVGcompositeOperationState), # StructType: NVGcompositeOperationState,
    ]
class GLNVGfragUniforms(ctypes.Structure):
    _fields_=[
        ("scissorMat", ctypes.c_float * 12), # ArrayType: float[12],
        ("paintMat", ctypes.c_float * 12), # ArrayType: float[12],
        ("innerCol", NVGcolor), # StructType: NVGcolor,
        ("outerCol", NVGcolor), # StructType: NVGcolor,
        ("scissorExt", ctypes.c_float * 2), # ArrayType: float[2],
        ("scissorScale", ctypes.c_float * 2), # ArrayType: float[2],
        ("extent", ctypes.c_float * 2), # ArrayType: float[2],
        ("radius", ctypes.c_float), # FloatType: float,
        ("feather", ctypes.c_float), # FloatType: float,
        ("strokeMult", ctypes.c_float), # FloatType: float,
        ("strokeThr", ctypes.c_float), # FloatType: float,
        ("texType", ctypes.c_int32), # Int32Type: int,
        ("type", ctypes.c_int32), # Int32Type: int,
    ]
from enum import IntEnum

class NVGcreateFlags(IntEnum):
    NVG_ANTIALIAS = 0x1
    NVG_STENCIL_STROKES = 0x2
    NVG_DEBUG = 0x4

class NVGwinding(IntEnum):
    NVG_CCW = 0x1
    NVG_CW = 0x2

class NVGsolidity(IntEnum):
    NVG_SOLID = 0x1
    NVG_HOLE = 0x2

class NVGlineCap(IntEnum):
    NVG_BUTT = 0x0
    NVG_ROUND = 0x1
    NVG_SQUARE = 0x2
    NVG_BEVEL = 0x3
    NVG_MITER = 0x4

class NVGalign(IntEnum):
    NVG_ALIGN_LEFT = 0x1
    NVG_ALIGN_CENTER = 0x2
    NVG_ALIGN_RIGHT = 0x4
    NVG_ALIGN_TOP = 0x8
    NVG_ALIGN_MIDDLE = 0x10
    NVG_ALIGN_BOTTOM = 0x20
    NVG_ALIGN_BASELINE = 0x40

class NVGblendFactor(IntEnum):
    NVG_INVALID = 0x0
    NVG_ZERO = 0x1
    NVG_ONE = 0x2
    NVG_SRC_COLOR = 0x4
    NVG_ONE_MINUS_SRC_COLOR = 0x8
    NVG_DST_COLOR = 0x10
    NVG_ONE_MINUS_DST_COLOR = 0x20
    NVG_SRC_ALPHA = 0x40
    NVG_ONE_MINUS_SRC_ALPHA = 0x80
    NVG_DST_ALPHA = 0x100
    NVG_ONE_MINUS_DST_ALPHA = 0x200
    NVG_SRC_ALPHA_SATURATE = 0x400

class NVGcompositeOperation(IntEnum):
    NVG_SOURCE_OVER = 0x0
    NVG_SOURCE_IN = 0x1
    NVG_SOURCE_OUT = 0x2
    NVG_ATOP = 0x3
    NVG_DESTINATION_OVER = 0x4
    NVG_DESTINATION_IN = 0x5
    NVG_DESTINATION_OUT = 0x6
    NVG_DESTINATION_ATOP = 0x7
    NVG_LIGHTER = 0x8
    NVG_COPY = 0x9
    NVG_XOR = 0xa

class NVGimageFlags(IntEnum):
    NVG_IMAGE_GENERATE_MIPMAPS = 0x1
    NVG_IMAGE_REPEATX = 0x2
    NVG_IMAGE_REPEATY = 0x4
    NVG_IMAGE_FLIPY = 0x8
    NVG_IMAGE_PREMULTIPLIED = 0x10
    NVG_IMAGE_NEAREST = 0x20

class NVGtexture(IntEnum):
    NVG_TEXTURE_ALPHA = 0x1
    NVG_TEXTURE_RGBA = 0x2

class GLNVGcallType(IntEnum):
    GLNVG_NONE = 0x0
    GLNVG_FILL = 0x1
    GLNVG_CONVEXFILL = 0x2
    GLNVG_STROKE = 0x3
    GLNVG_TRIANGLES = 0x4

class GLNVGshaderType(IntEnum):
    NSVG_SHADER_FILLGRAD = 0x0
    NSVG_SHADER_FILLIMG = 0x1
    NSVG_SHADER_SIMPLE = 0x2
    NSVG_SHADER_IMG = 0x3

