from typing import Type, Tuple, Union, Any, Iterable
import ctypes
from enum import IntEnum
from .impl.imgui import *


def iterate(data: ctypes.c_void_p, t: Type[ctypes.Structure], count: int)->Iterable[ctypes.Structure]:
    p = ctypes.cast(data, ctypes.POINTER(t))
    for i in range(count):
        yield p[i]


class ImVector(ctypes.Structure):
    _fields_ = (
        ('Size', ctypes.c_int),
        ('Capacity', ctypes.c_int),
        ('Data', ctypes.c_void_p),
    )

    def each(self, t: Type[ctypes.Structure])->Iterable[ctypes.Structure]:
        return iterate(self.Data, t, self.Size)

class ImVec2(ctypes.Structure):
    _fields_=[
        ("x", ctypes.c_float), # FloatType: float,
        ("y", ctypes.c_float), # FloatType: float,
    ]

    def __iter__(self):
        yield self.x
        yield self.y
class ImVec4(ctypes.Structure):
    _fields_=[
        ("x", ctypes.c_float), # FloatType: float,
        ("y", ctypes.c_float), # FloatType: float,
        ("z", ctypes.c_float), # FloatType: float,
        ("w", ctypes.c_float), # FloatType: float,
    ]

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.w
        yield self.h
class ImFont(ctypes.Structure):
    pass
class ImFontConfig(ctypes.Structure):
    _fields_=[
        ("FontData", ctypes.c_void_p), # PointerType: void*,
        ("FontDataSize", ctypes.c_int32), # Int32Type: int,
        ("FontDataOwnedByAtlas", ctypes.c_bool), # BoolType: bool,
        ("FontNo", ctypes.c_int32), # Int32Type: int,
        ("SizePixels", ctypes.c_float), # FloatType: float,
        ("OversampleH", ctypes.c_int32), # Int32Type: int,
        ("OversampleV", ctypes.c_int32), # Int32Type: int,
        ("PixelSnapH", ctypes.c_bool), # BoolType: bool,
        ("GlyphExtraSpacing", ImVec2), # ImVec2WrapType: ImVec2,
        ("GlyphOffset", ImVec2), # ImVec2WrapType: ImVec2,
        ("GlyphRanges", ctypes.c_void_p), # PointerType: unsigned short*,
        ("GlyphMinAdvanceX", ctypes.c_float), # FloatType: float,
        ("GlyphMaxAdvanceX", ctypes.c_float), # FloatType: float,
        ("MergeMode", ctypes.c_bool), # BoolType: bool,
        ("FontBuilderFlags", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("RasterizerMultiply", ctypes.c_float), # FloatType: float,
        ("EllipsisChar", ctypes.c_uint16), # UInt16Type: unsigned short,
        ("Name", ctypes.c_int8 * 40), # ArrayType: char[40],
        ("DstFont", ctypes.c_void_p), # PointerToStructType: ImFont*,
    ]
class ImFontAtlasCustomRect(ctypes.Structure):
    _fields_=[
        ("Width", ctypes.c_uint16), # UInt16Type: unsigned short,
        ("Height", ctypes.c_uint16), # UInt16Type: unsigned short,
        ("X", ctypes.c_uint16), # UInt16Type: unsigned short,
        ("Y", ctypes.c_uint16), # UInt16Type: unsigned short,
        ("GlyphID", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("GlyphAdvanceX", ctypes.c_float), # FloatType: float,
        ("GlyphOffset", ImVec2), # ImVec2WrapType: ImVec2,
        ("Font", ctypes.c_void_p), # PointerToStructType: ImFont*,
    ]
class ImFontAtlas(ctypes.Structure):
    _fields_=[
        ("Flags", ctypes.c_int32), # Int32Type: int,
        ("TexID", ctypes.c_void_p), # PointerType: void*,
        ("TexDesiredWidth", ctypes.c_int32), # Int32Type: int,
        ("TexGlyphPadding", ctypes.c_int32), # Int32Type: int,
        ("Locked", ctypes.c_bool), # BoolType: bool,
        ("TexReady", ctypes.c_bool), # BoolType: bool,
        ("TexPixelsUseColors", ctypes.c_bool), # BoolType: bool,
        ("TexPixelsAlpha8", ctypes.c_void_p), # PointerType: unsigned char*,
        ("TexPixelsRGBA32", ctypes.c_void_p), # PointerType: unsigned int*,
        ("TexWidth", ctypes.c_int32), # Int32Type: int,
        ("TexHeight", ctypes.c_int32), # Int32Type: int,
        ("TexUvScale", ImVec2), # ImVec2WrapType: ImVec2,
        ("TexUvWhitePixel", ImVec2), # ImVec2WrapType: ImVec2,
        ("Fonts", ImVector), # ImVector: ImVector,
        ("CustomRects", ImVector), # ImVector: ImVector,
        ("ConfigData", ImVector), # ImVector: ImVector,
        ("TexUvLines", ImVec4 * 64), # ArrayType: ImVec4[64],
        ("FontBuilderIO", ctypes.c_void_p), # PointerType: ImFontBuilderIO*,
        ("FontBuilderFlags", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("PackIdMouseCursors", ctypes.c_int32), # Int32Type: int,
        ("PackIdLines", ctypes.c_int32), # Int32Type: int,
    ]

    def AddFont(self, *args)->ImFont:
        from .impl import imgui
        return imgui.ImFontAtlas_AddFont(self, *args)

    def AddFontDefault(self, *args)->ImFont:
        from .impl import imgui
        return imgui.ImFontAtlas_AddFontDefault(self, *args)

    def AddFontFromFileTTF(self, *args)->ImFont:
        from .impl import imgui
        return imgui.ImFontAtlas_AddFontFromFileTTF(self, *args)

    def AddFontFromMemoryTTF(self, *args)->ImFont:
        from .impl import imgui
        return imgui.ImFontAtlas_AddFontFromMemoryTTF(self, *args)

    def AddFontFromMemoryCompressedTTF(self, *args)->ImFont:
        from .impl import imgui
        return imgui.ImFontAtlas_AddFontFromMemoryCompressedTTF(self, *args)

    def AddFontFromMemoryCompressedBase85TTF(self, *args)->ImFont:
        from .impl import imgui
        return imgui.ImFontAtlas_AddFontFromMemoryCompressedBase85TTF(self, *args)

    def ClearInputData(self, *args)->None:
        from .impl import imgui
        return imgui.ImFontAtlas_ClearInputData(self, *args)

    def ClearTexData(self, *args)->None:
        from .impl import imgui
        return imgui.ImFontAtlas_ClearTexData(self, *args)

    def ClearFonts(self, *args)->None:
        from .impl import imgui
        return imgui.ImFontAtlas_ClearFonts(self, *args)

    def Clear(self, *args)->None:
        from .impl import imgui
        return imgui.ImFontAtlas_Clear(self, *args)

    def Build(self, *args)->bool:
        from .impl import imgui
        return imgui.ImFontAtlas_Build(self, *args)

    def GetTexDataAsAlpha8(self, *args)->None:
        from .impl import imgui
        return imgui.ImFontAtlas_GetTexDataAsAlpha8(self, *args)

    def GetTexDataAsRGBA32(self, *args)->None:
        from .impl import imgui
        return imgui.ImFontAtlas_GetTexDataAsRGBA32(self, *args)

    def IsBuilt(self, *args)->bool:
        from .impl import imgui
        return imgui.ImFontAtlas_IsBuilt(self, *args)

    def SetTexID(self, *args)->None:
        from .impl import imgui
        return imgui.ImFontAtlas_SetTexID(self, *args)

    def GetGlyphRangesDefault(self, *args)->ctypes.c_void_p:
        from .impl import imgui
        return imgui.ImFontAtlas_GetGlyphRangesDefault(self, *args)

    def GetGlyphRangesKorean(self, *args)->ctypes.c_void_p:
        from .impl import imgui
        return imgui.ImFontAtlas_GetGlyphRangesKorean(self, *args)

    def GetGlyphRangesJapanese(self, *args)->ctypes.c_void_p:
        from .impl import imgui
        return imgui.ImFontAtlas_GetGlyphRangesJapanese(self, *args)

    def GetGlyphRangesChineseFull(self, *args)->ctypes.c_void_p:
        from .impl import imgui
        return imgui.ImFontAtlas_GetGlyphRangesChineseFull(self, *args)

    def GetGlyphRangesChineseSimplifiedCommon(self, *args)->ctypes.c_void_p:
        from .impl import imgui
        return imgui.ImFontAtlas_GetGlyphRangesChineseSimplifiedCommon(self, *args)

    def GetGlyphRangesCyrillic(self, *args)->ctypes.c_void_p:
        from .impl import imgui
        return imgui.ImFontAtlas_GetGlyphRangesCyrillic(self, *args)

    def GetGlyphRangesThai(self, *args)->ctypes.c_void_p:
        from .impl import imgui
        return imgui.ImFontAtlas_GetGlyphRangesThai(self, *args)

    def GetGlyphRangesVietnamese(self, *args)->ctypes.c_void_p:
        from .impl import imgui
        return imgui.ImFontAtlas_GetGlyphRangesVietnamese(self, *args)

    def AddCustomRectRegular(self, *args)->int:
        from .impl import imgui
        return imgui.ImFontAtlas_AddCustomRectRegular(self, *args)

    def AddCustomRectFontGlyph(self, *args)->int:
        from .impl import imgui
        return imgui.ImFontAtlas_AddCustomRectFontGlyph(self, *args)

    def GetCustomRectByIndex(self, *args)->ImFontAtlasCustomRect:
        from .impl import imgui
        return imgui.ImFontAtlas_GetCustomRectByIndex(self, *args)

    def CalcCustomRectUV(self, *args)->None:
        from .impl import imgui
        return imgui.ImFontAtlas_CalcCustomRectUV(self, *args)

    def GetMouseCursorTexData(self, *args)->bool:
        from .impl import imgui
        return imgui.ImFontAtlas_GetMouseCursorTexData(self, *args)
class ImGuiKeyData(ctypes.Structure):
    _fields_=[
        ("Down", ctypes.c_bool), # BoolType: bool,
        ("DownDuration", ctypes.c_float), # FloatType: float,
        ("DownDurationPrev", ctypes.c_float), # FloatType: float,
        ("AnalogValue", ctypes.c_float), # FloatType: float,
    ]
class ImGuiIO(ctypes.Structure):
    _fields_=[
        ("ConfigFlags", ctypes.c_int32), # Int32Type: int,
        ("BackendFlags", ctypes.c_int32), # Int32Type: int,
        ("DisplaySize", ImVec2), # ImVec2WrapType: ImVec2,
        ("DeltaTime", ctypes.c_float), # FloatType: float,
        ("IniSavingRate", ctypes.c_float), # FloatType: float,
        ("IniFilename", ctypes.c_void_p), # CStringType: const char *,
        ("LogFilename", ctypes.c_void_p), # CStringType: const char *,
        ("MouseDoubleClickTime", ctypes.c_float), # FloatType: float,
        ("MouseDoubleClickMaxDist", ctypes.c_float), # FloatType: float,
        ("MouseDragThreshold", ctypes.c_float), # FloatType: float,
        ("KeyRepeatDelay", ctypes.c_float), # FloatType: float,
        ("KeyRepeatRate", ctypes.c_float), # FloatType: float,
        ("UserData", ctypes.c_void_p), # PointerType: void*,
        ("_Fonts", ctypes.c_void_p), # PointerToStructType: ImFontAtlas*,
        ("FontGlobalScale", ctypes.c_float), # FloatType: float,
        ("FontAllowUserScaling", ctypes.c_bool), # BoolType: bool,
        ("FontDefault", ctypes.c_void_p), # PointerToStructType: ImFont*,
        ("DisplayFramebufferScale", ImVec2), # ImVec2WrapType: ImVec2,
        ("ConfigDockingNoSplit", ctypes.c_bool), # BoolType: bool,
        ("ConfigDockingWithShift", ctypes.c_bool), # BoolType: bool,
        ("ConfigDockingAlwaysTabBar", ctypes.c_bool), # BoolType: bool,
        ("ConfigDockingTransparentPayload", ctypes.c_bool), # BoolType: bool,
        ("ConfigViewportsNoAutoMerge", ctypes.c_bool), # BoolType: bool,
        ("ConfigViewportsNoTaskBarIcon", ctypes.c_bool), # BoolType: bool,
        ("ConfigViewportsNoDecoration", ctypes.c_bool), # BoolType: bool,
        ("ConfigViewportsNoDefaultParent", ctypes.c_bool), # BoolType: bool,
        ("MouseDrawCursor", ctypes.c_bool), # BoolType: bool,
        ("ConfigMacOSXBehaviors", ctypes.c_bool), # BoolType: bool,
        ("ConfigInputTrickleEventQueue", ctypes.c_bool), # BoolType: bool,
        ("ConfigInputTextCursorBlink", ctypes.c_bool), # BoolType: bool,
        ("ConfigDragClickToInputText", ctypes.c_bool), # BoolType: bool,
        ("ConfigWindowsResizeFromEdges", ctypes.c_bool), # BoolType: bool,
        ("ConfigWindowsMoveFromTitleBarOnly", ctypes.c_bool), # BoolType: bool,
        ("ConfigMemoryCompactTimer", ctypes.c_float), # FloatType: float,
        ("BackendPlatformName", ctypes.c_void_p), # CStringType: const char *,
        ("BackendRendererName", ctypes.c_void_p), # CStringType: const char *,
        ("BackendPlatformUserData", ctypes.c_void_p), # PointerType: void*,
        ("BackendRendererUserData", ctypes.c_void_p), # PointerType: void*,
        ("BackendLanguageUserData", ctypes.c_void_p), # PointerType: void*,
        ("GetClipboardTextFn", ctypes.c_void_p), # PointerType: void**,
        ("SetClipboardTextFn", ctypes.c_void_p), # PointerType: void**,
        ("ClipboardUserData", ctypes.c_void_p), # PointerType: void*,
        ("SetPlatformImeDataFn", ctypes.c_void_p), # PointerType: void**,
        ("ImeWindowHandle", ctypes.c_void_p), # PointerType: void*,
        ("WantCaptureMouse", ctypes.c_bool), # BoolType: bool,
        ("WantCaptureKeyboard", ctypes.c_bool), # BoolType: bool,
        ("WantTextInput", ctypes.c_bool), # BoolType: bool,
        ("WantSetMousePos", ctypes.c_bool), # BoolType: bool,
        ("WantSaveIniSettings", ctypes.c_bool), # BoolType: bool,
        ("NavActive", ctypes.c_bool), # BoolType: bool,
        ("NavVisible", ctypes.c_bool), # BoolType: bool,
        ("Framerate", ctypes.c_float), # FloatType: float,
        ("MetricsRenderVertices", ctypes.c_int32), # Int32Type: int,
        ("MetricsRenderIndices", ctypes.c_int32), # Int32Type: int,
        ("MetricsRenderWindows", ctypes.c_int32), # Int32Type: int,
        ("MetricsActiveWindows", ctypes.c_int32), # Int32Type: int,
        ("MetricsActiveAllocations", ctypes.c_int32), # Int32Type: int,
        ("MouseDelta", ImVec2), # ImVec2WrapType: ImVec2,
        ("KeyMap", ctypes.c_int32 * 645), # ArrayType: int[645],
        ("KeysDown", ctypes.c_bool * 645), # ArrayType: bool[645],
        ("MousePos", ImVec2), # ImVec2WrapType: ImVec2,
        ("MouseDown", ctypes.c_bool * 5), # ArrayType: bool[5],
        ("MouseWheel", ctypes.c_float), # FloatType: float,
        ("MouseWheelH", ctypes.c_float), # FloatType: float,
        ("MouseHoveredViewport", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("KeyCtrl", ctypes.c_bool), # BoolType: bool,
        ("KeyShift", ctypes.c_bool), # BoolType: bool,
        ("KeyAlt", ctypes.c_bool), # BoolType: bool,
        ("KeySuper", ctypes.c_bool), # BoolType: bool,
        ("NavInputs", ctypes.c_float * 20), # ArrayType: float[20],
        ("KeyMods", ctypes.c_int32), # Int32Type: int,
        ("KeysData", ImGuiKeyData * 645), # ArrayType: ImGuiKeyData[645],
        ("WantCaptureMouseUnlessPopupClose", ctypes.c_bool), # BoolType: bool,
        ("MousePosPrev", ImVec2), # ImVec2WrapType: ImVec2,
        ("MouseClickedPos", ImVec2 * 5), # ArrayType: ImVec2[5],
        ("MouseClickedTime", ctypes.c_double * 5), # ArrayType: double[5],
        ("MouseClicked", ctypes.c_bool * 5), # ArrayType: bool[5],
        ("MouseDoubleClicked", ctypes.c_bool * 5), # ArrayType: bool[5],
        ("MouseClickedCount", ctypes.c_uint16 * 5), # ArrayType: unsigned short[5],
        ("MouseClickedLastCount", ctypes.c_uint16 * 5), # ArrayType: unsigned short[5],
        ("MouseReleased", ctypes.c_bool * 5), # ArrayType: bool[5],
        ("MouseDownOwned", ctypes.c_bool * 5), # ArrayType: bool[5],
        ("MouseDownOwnedUnlessPopupClose", ctypes.c_bool * 5), # ArrayType: bool[5],
        ("MouseDownDuration", ctypes.c_float * 5), # ArrayType: float[5],
        ("MouseDownDurationPrev", ctypes.c_float * 5), # ArrayType: float[5],
        ("MouseDragMaxDistanceAbs", ImVec2 * 5), # ArrayType: ImVec2[5],
        ("MouseDragMaxDistanceSqr", ctypes.c_float * 5), # ArrayType: float[5],
        ("NavInputsDownDuration", ctypes.c_float * 20), # ArrayType: float[20],
        ("NavInputsDownDurationPrev", ctypes.c_float * 20), # ArrayType: float[20],
        ("PenPressure", ctypes.c_float), # FloatType: float,
        ("AppFocusLost", ctypes.c_bool), # BoolType: bool,
        ("BackendUsingLegacyKeyArrays", ctypes.c_int8), # Int8Type: char,
        ("BackendUsingLegacyNavInputArray", ctypes.c_bool), # BoolType: bool,
        ("InputQueueSurrogate", ctypes.c_uint16), # UInt16Type: unsigned short,
        ("InputQueueCharacters", ImVector), # ImVector: ImVector,
    ]

    @property
    def Fonts(self)->'ImFontAtlas':
        return ctypes.cast(ctypes.c_void_p(self._Fonts), ctypes.POINTER(ImFontAtlas))[0]

    def AddKeyEvent(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddKeyEvent(self, *args)

    def AddKeyAnalogEvent(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddKeyAnalogEvent(self, *args)

    def AddMousePosEvent(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddMousePosEvent(self, *args)

    def AddMouseButtonEvent(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddMouseButtonEvent(self, *args)

    def AddMouseWheelEvent(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddMouseWheelEvent(self, *args)

    def AddMouseViewportEvent(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddMouseViewportEvent(self, *args)

    def AddFocusEvent(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddFocusEvent(self, *args)

    def AddInputCharacter(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddInputCharacter(self, *args)

    def AddInputCharacterUTF16(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddInputCharacterUTF16(self, *args)

    def AddInputCharactersUTF8(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_AddInputCharactersUTF8(self, *args)

    def ClearInputCharacters(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_ClearInputCharacters(self, *args)

    def ClearInputKeys(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_ClearInputKeys(self, *args)

    def SetKeyEventNativeData(self, *args)->None:
        from .impl import imgui
        return imgui.ImGuiIO_SetKeyEventNativeData(self, *args)
class ImDrawCmd(ctypes.Structure):
    _fields_=[
        ("ClipRect", ImVec4), # ImVec4WrapType: ImVec4,
        ("TextureId", ctypes.c_void_p), # PointerType: void*,
        ("VtxOffset", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("IdxOffset", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("ElemCount", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("UserCallback", ctypes.c_void_p), # PointerType: void**,
        ("UserCallbackData", ctypes.c_void_p), # PointerType: void*,
    ]
class ImDrawData(ctypes.Structure):
    _fields_=[
        ("Valid", ctypes.c_bool), # BoolType: bool,
        ("CmdListsCount", ctypes.c_int32), # Int32Type: int,
        ("TotalIdxCount", ctypes.c_int32), # Int32Type: int,
        ("TotalVtxCount", ctypes.c_int32), # Int32Type: int,
        ("CmdLists", ctypes.c_void_p), # PointerType: ImDrawList**,
        ("DisplayPos", ImVec2), # ImVec2WrapType: ImVec2,
        ("DisplaySize", ImVec2), # ImVec2WrapType: ImVec2,
        ("FramebufferScale", ImVec2), # ImVec2WrapType: ImVec2,
        ("OwnerViewport", ctypes.c_void_p), # PointerToStructType: ImGuiViewport*,
    ]
class ImDrawListSplitter(ctypes.Structure):
    _fields_=[
        ("_Current", ctypes.c_int32), # Int32Type: int,
        ("_Count", ctypes.c_int32), # Int32Type: int,
        ("_Channels", ImVector), # ImVector: ImVector,
    ]
class ImDrawCmdHeader(ctypes.Structure):
    _fields_=[
        ("ClipRect", ImVec4), # ImVec4WrapType: ImVec4,
        ("TextureId", ctypes.c_void_p), # PointerType: void*,
        ("VtxOffset", ctypes.c_uint32), # UInt32Type: unsigned int,
    ]
class ImDrawList(ctypes.Structure):
    _fields_=[
        ("CmdBuffer", ImVector), # ImVector: ImVector,
        ("IdxBuffer", ImVector), # ImVector: ImVector,
        ("VtxBuffer", ImVector), # ImVector: ImVector,
        ("Flags", ctypes.c_int32), # Int32Type: int,
        ("_VtxCurrentIdx", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("_Data", ctypes.c_void_p), # PointerType: ImDrawListSharedData*,
        ("_OwnerName", ctypes.c_void_p), # CStringType: const char *,
        ("_VtxWritePtr", ctypes.c_void_p), # PointerType: ImDrawVert*,
        ("_IdxWritePtr", ctypes.c_void_p), # PointerType: unsigned short*,
        ("_ClipRectStack", ImVector), # ImVector: ImVector,
        ("_TextureIdStack", ImVector), # ImVector: ImVector,
        ("_Path", ImVector), # ImVector: ImVector,
        ("_CmdHeader", ImDrawCmdHeader), # StructType: ImDrawCmdHeader,
        ("_Splitter", ImDrawListSplitter), # StructType: ImDrawListSplitter,
        ("_FringeScale", ctypes.c_float), # FloatType: float,
    ]
class ImGuiViewport(ctypes.Structure):
    _fields_=[
        ("ID", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("Flags", ctypes.c_int32), # Int32Type: int,
        ("Pos", ImVec2), # ImVec2WrapType: ImVec2,
        ("Size", ImVec2), # ImVec2WrapType: ImVec2,
        ("WorkPos", ImVec2), # ImVec2WrapType: ImVec2,
        ("WorkSize", ImVec2), # ImVec2WrapType: ImVec2,
        ("DpiScale", ctypes.c_float), # FloatType: float,
        ("ParentViewportId", ctypes.c_uint32), # UInt32Type: unsigned int,
        ("DrawData", ctypes.c_void_p), # PointerToStructType: ImDrawData*,
        ("RendererUserData", ctypes.c_void_p), # PointerType: void*,
        ("PlatformUserData", ctypes.c_void_p), # PointerType: void*,
        ("PlatformHandle", ctypes.c_void_p), # PointerType: void*,
        ("PlatformHandleRaw", ctypes.c_void_p), # PointerType: void*,
        ("PlatformRequestMove", ctypes.c_bool), # BoolType: bool,
        ("PlatformRequestResize", ctypes.c_bool), # BoolType: bool,
        ("PlatformRequestClose", ctypes.c_bool), # BoolType: bool,
    ]

    def GetCenter(self, *args)->ImVec2:
        from .impl import imgui
        return imgui.ImGuiViewport_GetCenter(self, *args)

    def GetWorkCenter(self, *args)->ImVec2:
        from .impl import imgui
        return imgui.ImGuiViewport_GetWorkCenter(self, *args)
class ImGuiStyle(ctypes.Structure):
    pass
class ImGuiWindowClass(ctypes.Structure):
    pass
from enum import IntEnum

class ImGuiWindowFlags_(IntEnum):
    NONE = 0x0
    NoTitleBar = 0x1
    NoResize = 0x2
    NoMove = 0x4
    NoScrollbar = 0x8
    NoScrollWithMouse = 0x10
    NoCollapse = 0x20
    AlwaysAutoResize = 0x40
    NoBackground = 0x80
    NoSavedSettings = 0x100
    NoMouseInputs = 0x200
    MenuBar = 0x400
    HorizontalScrollbar = 0x800
    NoFocusOnAppearing = 0x1000
    NoBringToFrontOnFocus = 0x2000
    AlwaysVerticalScrollbar = 0x4000
    AlwaysHorizontalScrollbar = 0x8000
    AlwaysUseWindowPadding = 0x10000
    NoNavInputs = 0x40000
    NoNavFocus = 0x80000
    UnsavedDocument = 0x100000
    NoDocking = 0x200000
    NoNav = 0xc0000
    NoDecoration = 0x2b
    NoInputs = 0xc0200
    NavFlattened = 0x800000
    ChildWindow = 0x1000000
    Tooltip = 0x2000000
    Popup = 0x4000000
    Modal = 0x8000000
    ChildMenu = 0x10000000
    DockNodeHost = 0x20000000

class ImGuiInputTextFlags_(IntEnum):
    NONE = 0x0
    CharsDecimal = 0x1
    CharsHexadecimal = 0x2
    CharsUppercase = 0x4
    CharsNoBlank = 0x8
    AutoSelectAll = 0x10
    EnterReturnsTrue = 0x20
    CallbackCompletion = 0x40
    CallbackHistory = 0x80
    CallbackAlways = 0x100
    CallbackCharFilter = 0x200
    AllowTabInput = 0x400
    CtrlEnterForNewLine = 0x800
    NoHorizontalScroll = 0x1000
    AlwaysOverwrite = 0x2000
    ReadOnly = 0x4000
    Password = 0x8000
    NoUndoRedo = 0x10000
    CharsScientific = 0x20000
    CallbackResize = 0x40000
    CallbackEdit = 0x80000
    AlwaysInsertMode = 0x2000

class ImGuiTreeNodeFlags_(IntEnum):
    NONE = 0x0
    Selected = 0x1
    Framed = 0x2
    AllowItemOverlap = 0x4
    NoTreePushOnOpen = 0x8
    NoAutoOpenOnLog = 0x10
    DefaultOpen = 0x20
    OpenOnDoubleClick = 0x40
    OpenOnArrow = 0x80
    Leaf = 0x100
    Bullet = 0x200
    FramePadding = 0x400
    SpanAvailWidth = 0x800
    SpanFullWidth = 0x1000
    NavLeftJumpsBackHere = 0x2000
    CollapsingHeader = 0x1a

class ImGuiPopupFlags_(IntEnum):
    NONE = 0x0
    MouseButtonLeft = 0x0
    MouseButtonRight = 0x1
    MouseButtonMiddle = 0x2
    MouseButtonMask_ = 0x1f
    MouseButtonDefault_ = 0x1
    NoOpenOverExistingPopup = 0x20
    NoOpenOverItems = 0x40
    AnyPopupId = 0x80
    AnyPopupLevel = 0x100
    AnyPopup = 0x180

class ImGuiSelectableFlags_(IntEnum):
    NONE = 0x0
    DontClosePopups = 0x1
    SpanAllColumns = 0x2
    AllowDoubleClick = 0x4
    Disabled = 0x8
    AllowItemOverlap = 0x10

class ImGuiComboFlags_(IntEnum):
    NONE = 0x0
    PopupAlignLeft = 0x1
    HeightSmall = 0x2
    HeightRegular = 0x4
    HeightLarge = 0x8
    HeightLargest = 0x10
    NoArrowButton = 0x20
    NoPreview = 0x40
    HeightMask_ = 0x1e

class ImGuiTabBarFlags_(IntEnum):
    NONE = 0x0
    Reorderable = 0x1
    AutoSelectNewTabs = 0x2
    TabListPopupButton = 0x4
    NoCloseWithMiddleMouseButton = 0x8
    NoTabListScrollingButtons = 0x10
    NoTooltip = 0x20
    FittingPolicyResizeDown = 0x40
    FittingPolicyScroll = 0x80
    FittingPolicyMask_ = 0xc0
    FittingPolicyDefault_ = 0x40

class ImGuiTabItemFlags_(IntEnum):
    NONE = 0x0
    UnsavedDocument = 0x1
    SetSelected = 0x2
    NoCloseWithMiddleMouseButton = 0x4
    NoPushId = 0x8
    NoTooltip = 0x10
    NoReorder = 0x20
    Leading = 0x40
    Trailing = 0x80

class ImGuiTableFlags_(IntEnum):
    NONE = 0x0
    Resizable = 0x1
    Reorderable = 0x2
    Hideable = 0x4
    Sortable = 0x8
    NoSavedSettings = 0x10
    ContextMenuInBody = 0x20
    RowBg = 0x40
    BordersInnerH = 0x80
    BordersOuterH = 0x100
    BordersInnerV = 0x200
    BordersOuterV = 0x400
    BordersH = 0x180
    BordersV = 0x600
    BordersInner = 0x280
    BordersOuter = 0x500
    Borders = 0x780
    NoBordersInBody = 0x800
    NoBordersInBodyUntilResize = 0x1000
    SizingFixedFit = 0x2000
    SizingFixedSame = 0x4000
    SizingStretchProp = 0x6000
    SizingStretchSame = 0x8000
    NoHostExtendX = 0x10000
    NoHostExtendY = 0x20000
    NoKeepColumnsVisible = 0x40000
    PreciseWidths = 0x80000
    NoClip = 0x100000
    PadOuterX = 0x200000
    NoPadOuterX = 0x400000
    NoPadInnerX = 0x800000
    ScrollX = 0x1000000
    ScrollY = 0x2000000
    SortMulti = 0x4000000
    SortTristate = 0x8000000
    SizingMask_ = 0xe000

class ImGuiTableColumnFlags_(IntEnum):
    NONE = 0x0
    Disabled = 0x1
    DefaultHide = 0x2
    DefaultSort = 0x4
    WidthStretch = 0x8
    WidthFixed = 0x10
    NoResize = 0x20
    NoReorder = 0x40
    NoHide = 0x80
    NoClip = 0x100
    NoSort = 0x200
    NoSortAscending = 0x400
    NoSortDescending = 0x800
    NoHeaderLabel = 0x1000
    NoHeaderWidth = 0x2000
    PreferSortAscending = 0x4000
    PreferSortDescending = 0x8000
    IndentEnable = 0x10000
    IndentDisable = 0x20000
    IsEnabled = 0x1000000
    IsVisible = 0x2000000
    IsSorted = 0x4000000
    IsHovered = 0x8000000
    WidthMask_ = 0x18
    IndentMask_ = 0x30000
    StatusMask_ = 0xf000000
    NoDirectResize_ = 0x40000000

class ImGuiTableRowFlags_(IntEnum):
    NONE = 0x0
    Headers = 0x1

class ImGuiTableBgTarget_(IntEnum):
    NONE = 0x0
    RowBg0 = 0x1
    RowBg1 = 0x2
    CellBg = 0x3

class ImGuiFocusedFlags_(IntEnum):
    NONE = 0x0
    ChildWindows = 0x1
    RootWindow = 0x2
    AnyWindow = 0x4
    NoPopupHierarchy = 0x8
    DockHierarchy = 0x10
    RootAndChildWindows = 0x3

class ImGuiHoveredFlags_(IntEnum):
    NONE = 0x0
    ChildWindows = 0x1
    RootWindow = 0x2
    AnyWindow = 0x4
    NoPopupHierarchy = 0x8
    DockHierarchy = 0x10
    AllowWhenBlockedByPopup = 0x20
    AllowWhenBlockedByActiveItem = 0x80
    AllowWhenOverlapped = 0x100
    AllowWhenDisabled = 0x200
    NoNavOverride = 0x400
    RectOnly = 0x1a0
    RootAndChildWindows = 0x3

class ImGuiDockNodeFlags_(IntEnum):
    NONE = 0x0
    KeepAliveOnly = 0x1
    NoDockingInCentralNode = 0x4
    PassthruCentralNode = 0x8
    NoSplit = 0x10
    NoResize = 0x20
    AutoHideTabBar = 0x40

class ImGuiDragDropFlags_(IntEnum):
    NONE = 0x0
    SourceNoPreviewTooltip = 0x1
    SourceNoDisableHover = 0x2
    SourceNoHoldToOpenOthers = 0x4
    SourceAllowNullID = 0x8
    SourceExtern = 0x10
    SourceAutoExpirePayload = 0x20
    AcceptBeforeDelivery = 0x400
    AcceptNoDrawDefaultRect = 0x800
    AcceptNoPreviewTooltip = 0x1000
    AcceptPeekOnly = 0xc00

class ImGuiDataType_(IntEnum):
    S8 = 0x0
    U8 = 0x1
    S16 = 0x2
    U16 = 0x3
    S32 = 0x4
    U32 = 0x5
    S64 = 0x6
    U64 = 0x7
    Float = 0x8
    Double = 0x9
    COUNT = 0xa

class ImGuiDir_(IntEnum):
    NONE = -0x1
    Left = 0x0
    Right = 0x1
    Up = 0x2
    Down = 0x3
    COUNT = 0x4

class ImGuiSortDirection_(IntEnum):
    NONE = 0x0
    Ascending = 0x1
    Descending = 0x2

class ImGuiKey_(IntEnum):
    NONE = 0x0
    Tab = 0x200
    LeftArrow = 0x201
    RightArrow = 0x202
    UpArrow = 0x203
    DownArrow = 0x204
    PageUp = 0x205
    PageDown = 0x206
    Home = 0x207
    End = 0x208
    Insert = 0x209
    Delete = 0x20a
    Backspace = 0x20b
    Space = 0x20c
    Enter = 0x20d
    Escape = 0x20e
    LeftCtrl = 0x20f
    LeftShift = 0x210
    LeftAlt = 0x211
    LeftSuper = 0x212
    RightCtrl = 0x213
    RightShift = 0x214
    RightAlt = 0x215
    RightSuper = 0x216
    Menu = 0x217
    _0 = 0x218
    _1 = 0x219
    _2 = 0x21a
    _3 = 0x21b
    _4 = 0x21c
    _5 = 0x21d
    _6 = 0x21e
    _7 = 0x21f
    _8 = 0x220
    _9 = 0x221
    A = 0x222
    B = 0x223
    C = 0x224
    D = 0x225
    E = 0x226
    F = 0x227
    G = 0x228
    H = 0x229
    I = 0x22a
    J = 0x22b
    K = 0x22c
    L = 0x22d
    M = 0x22e
    N = 0x22f
    O = 0x230
    P = 0x231
    Q = 0x232
    R = 0x233
    S = 0x234
    T = 0x235
    U = 0x236
    V = 0x237
    W = 0x238
    X = 0x239
    Y = 0x23a
    Z = 0x23b
    F1 = 0x23c
    F2 = 0x23d
    F3 = 0x23e
    F4 = 0x23f
    F5 = 0x240
    F6 = 0x241
    F7 = 0x242
    F8 = 0x243
    F9 = 0x244
    F10 = 0x245
    F11 = 0x246
    F12 = 0x247
    Apostrophe = 0x248
    Comma = 0x249
    Minus = 0x24a
    Period = 0x24b
    Slash = 0x24c
    Semicolon = 0x24d
    Equal = 0x24e
    LeftBracket = 0x24f
    Backslash = 0x250
    RightBracket = 0x251
    GraveAccent = 0x252
    CapsLock = 0x253
    ScrollLock = 0x254
    NumLock = 0x255
    PrintScreen = 0x256
    Pause = 0x257
    Keypad0 = 0x258
    Keypad1 = 0x259
    Keypad2 = 0x25a
    Keypad3 = 0x25b
    Keypad4 = 0x25c
    Keypad5 = 0x25d
    Keypad6 = 0x25e
    Keypad7 = 0x25f
    Keypad8 = 0x260
    Keypad9 = 0x261
    KeypadDecimal = 0x262
    KeypadDivide = 0x263
    KeypadMultiply = 0x264
    KeypadSubtract = 0x265
    KeypadAdd = 0x266
    KeypadEnter = 0x267
    KeypadEqual = 0x268
    GamepadStart = 0x269
    GamepadBack = 0x26a
    GamepadFaceUp = 0x26b
    GamepadFaceDown = 0x26c
    GamepadFaceLeft = 0x26d
    GamepadFaceRight = 0x26e
    GamepadDpadUp = 0x26f
    GamepadDpadDown = 0x270
    GamepadDpadLeft = 0x271
    GamepadDpadRight = 0x272
    GamepadL1 = 0x273
    GamepadR1 = 0x274
    GamepadL2 = 0x275
    GamepadR2 = 0x276
    GamepadL3 = 0x277
    GamepadR3 = 0x278
    GamepadLStickUp = 0x279
    GamepadLStickDown = 0x27a
    GamepadLStickLeft = 0x27b
    GamepadLStickRight = 0x27c
    GamepadRStickUp = 0x27d
    GamepadRStickDown = 0x27e
    GamepadRStickLeft = 0x27f
    GamepadRStickRight = 0x280
    ModCtrl = 0x281
    ModShift = 0x282
    ModAlt = 0x283
    ModSuper = 0x284
    COUNT = 0x285
    NamedKey_BEGIN = 0x200
    NamedKey_END = 0x285
    NamedKey_COUNT = 0x85
    KeysData_SIZE = 0x285
    KeysData_OFFSET = 0x0
    KeyPadEnter = 0x267

class ImGuiModFlags_(IntEnum):
    NONE = 0x0
    Ctrl = 0x1
    Shift = 0x2
    Alt = 0x4
    Super = 0x8

class ImGuiNavInput_(IntEnum):
    Activate = 0x0
    Cancel = 0x1
    Input = 0x2
    Menu = 0x3
    DpadLeft = 0x4
    DpadRight = 0x5
    DpadUp = 0x6
    DpadDown = 0x7
    LStickLeft = 0x8
    LStickRight = 0x9
    LStickUp = 0xa
    LStickDown = 0xb
    FocusPrev = 0xc
    FocusNext = 0xd
    TweakSlow = 0xe
    TweakFast = 0xf
    KeyLeft_ = 0x10
    KeyRight_ = 0x11
    KeyUp_ = 0x12
    KeyDown_ = 0x13
    COUNT = 0x14

class ImGuiConfigFlags_(IntEnum):
    NONE = 0x0
    NavEnableKeyboard = 0x1
    NavEnableGamepad = 0x2
    NavEnableSetMousePos = 0x4
    NavNoCaptureKeyboard = 0x8
    NoMouse = 0x10
    NoMouseCursorChange = 0x20
    DockingEnable = 0x40
    ViewportsEnable = 0x400
    DpiEnableScaleViewports = 0x4000
    DpiEnableScaleFonts = 0x8000
    IsSRGB = 0x100000
    IsTouchScreen = 0x200000

class ImGuiBackendFlags_(IntEnum):
    NONE = 0x0
    HasGamepad = 0x1
    HasMouseCursors = 0x2
    HasSetMousePos = 0x4
    RendererHasVtxOffset = 0x8
    PlatformHasViewports = 0x400
    HasMouseHoveredViewport = 0x800
    RendererHasViewports = 0x1000

class ImGuiCol_(IntEnum):
    Text = 0x0
    TextDisabled = 0x1
    WindowBg = 0x2
    ChildBg = 0x3
    PopupBg = 0x4
    Border = 0x5
    BorderShadow = 0x6
    FrameBg = 0x7
    FrameBgHovered = 0x8
    FrameBgActive = 0x9
    TitleBg = 0xa
    TitleBgActive = 0xb
    TitleBgCollapsed = 0xc
    MenuBarBg = 0xd
    ScrollbarBg = 0xe
    ScrollbarGrab = 0xf
    ScrollbarGrabHovered = 0x10
    ScrollbarGrabActive = 0x11
    CheckMark = 0x12
    SliderGrab = 0x13
    SliderGrabActive = 0x14
    Button = 0x15
    ButtonHovered = 0x16
    ButtonActive = 0x17
    Header = 0x18
    HeaderHovered = 0x19
    HeaderActive = 0x1a
    Separator = 0x1b
    SeparatorHovered = 0x1c
    SeparatorActive = 0x1d
    ResizeGrip = 0x1e
    ResizeGripHovered = 0x1f
    ResizeGripActive = 0x20
    Tab = 0x21
    TabHovered = 0x22
    TabActive = 0x23
    TabUnfocused = 0x24
    TabUnfocusedActive = 0x25
    DockingPreview = 0x26
    DockingEmptyBg = 0x27
    PlotLines = 0x28
    PlotLinesHovered = 0x29
    PlotHistogram = 0x2a
    PlotHistogramHovered = 0x2b
    TableHeaderBg = 0x2c
    TableBorderStrong = 0x2d
    TableBorderLight = 0x2e
    TableRowBg = 0x2f
    TableRowBgAlt = 0x30
    TextSelectedBg = 0x31
    DragDropTarget = 0x32
    NavHighlight = 0x33
    NavWindowingHighlight = 0x34
    NavWindowingDimBg = 0x35
    ModalWindowDimBg = 0x36
    COUNT = 0x37

class ImGuiStyleVar_(IntEnum):
    Alpha = 0x0
    DisabledAlpha = 0x1
    WindowPadding = 0x2
    WindowRounding = 0x3
    WindowBorderSize = 0x4
    WindowMinSize = 0x5
    WindowTitleAlign = 0x6
    ChildRounding = 0x7
    ChildBorderSize = 0x8
    PopupRounding = 0x9
    PopupBorderSize = 0xa
    FramePadding = 0xb
    FrameRounding = 0xc
    FrameBorderSize = 0xd
    ItemSpacing = 0xe
    ItemInnerSpacing = 0xf
    IndentSpacing = 0x10
    CellPadding = 0x11
    ScrollbarSize = 0x12
    ScrollbarRounding = 0x13
    GrabMinSize = 0x14
    GrabRounding = 0x15
    TabRounding = 0x16
    ButtonTextAlign = 0x17
    SelectableTextAlign = 0x18
    COUNT = 0x19

class ImGuiButtonFlags_(IntEnum):
    NONE = 0x0
    MouseButtonLeft = 0x1
    MouseButtonRight = 0x2
    MouseButtonMiddle = 0x4
    MouseButtonMask_ = 0x7
    MouseButtonDefault_ = 0x1

class ImGuiColorEditFlags_(IntEnum):
    NONE = 0x0
    NoAlpha = 0x2
    NoPicker = 0x4
    NoOptions = 0x8
    NoSmallPreview = 0x10
    NoInputs = 0x20
    NoTooltip = 0x40
    NoLabel = 0x80
    NoSidePreview = 0x100
    NoDragDrop = 0x200
    NoBorder = 0x400
    AlphaBar = 0x10000
    AlphaPreview = 0x20000
    AlphaPreviewHalf = 0x40000
    HDR = 0x80000
    DisplayRGB = 0x100000
    DisplayHSV = 0x200000
    DisplayHex = 0x400000
    Uint8 = 0x800000
    Float = 0x1000000
    PickerHueBar = 0x2000000
    PickerHueWheel = 0x4000000
    InputRGB = 0x8000000
    InputHSV = 0x10000000
    DefaultOptions_ = 0xa900000
    DisplayMask_ = 0x700000
    DataTypeMask_ = 0x1800000
    PickerMask_ = 0x6000000
    InputMask_ = 0x18000000

class ImGuiSliderFlags_(IntEnum):
    NONE = 0x0
    AlwaysClamp = 0x10
    Logarithmic = 0x20
    NoRoundToFormat = 0x40
    NoInput = 0x80
    InvalidMask_ = 0x7000000f
    ClampOnInput = 0x10

class ImGuiMouseButton_(IntEnum):
    Left = 0x0
    Right = 0x1
    Middle = 0x2
    COUNT = 0x5

class ImGuiMouseCursor_(IntEnum):
    NONE = -0x1
    Arrow = 0x0
    TextInput = 0x1
    ResizeAll = 0x2
    ResizeNS = 0x3
    ResizeEW = 0x4
    ResizeNESW = 0x5
    ResizeNWSE = 0x6
    Hand = 0x7
    NotAllowed = 0x8
    COUNT = 0x9

class ImGuiCond_(IntEnum):
    NONE = 0x0
    Always = 0x1
    Once = 0x2
    FirstUseEver = 0x4
    Appearing = 0x8

class ImDrawFlags_(IntEnum):
    NONE = 0x0
    Closed = 0x1
    RoundCornersTopLeft = 0x10
    RoundCornersTopRight = 0x20
    RoundCornersBottomLeft = 0x40
    RoundCornersBottomRight = 0x80
    RoundCornersNone = 0x100
    RoundCornersTop = 0x30
    RoundCornersBottom = 0xc0
    RoundCornersLeft = 0x50
    RoundCornersRight = 0xa0
    RoundCornersAll = 0xf0
    RoundCornersDefault_ = 0xf0
    RoundCornersMask_ = 0x1f0

class ImDrawListFlags_(IntEnum):
    NONE = 0x0
    AntiAliasedLines = 0x1
    AntiAliasedLinesUseTex = 0x2
    AntiAliasedFill = 0x4
    AllowVtxOffset = 0x8

class ImFontAtlasFlags_(IntEnum):
    NONE = 0x0
    NoPowerOfTwoHeight = 0x1
    NoMouseCursors = 0x2
    NoBakedLines = 0x4

class ImGuiViewportFlags_(IntEnum):
    NONE = 0x0
    IsPlatformWindow = 0x1
    IsPlatformMonitor = 0x2
    OwnedByApp = 0x4
    NoDecoration = 0x8
    NoTaskBarIcon = 0x10
    NoFocusOnAppearing = 0x20
    NoFocusOnClick = 0x40
    NoInputs = 0x80
    NoRendererClear = 0x100
    TopMost = 0x200
    Minimized = 0x400
    NoAutoMerge = 0x800
    CanHostOtherWindows = 0x1000

class ImDrawCornerFlags_(IntEnum):
    NONE = 0x100
    TopLeft = 0x10
    TopRight = 0x20
    BotLeft = 0x40
    BotRight = 0x80
    All = 0xf0
    Top = 0x30
    Bot = 0xc0
    Left = 0x50
    Right = 0xa0

class ImGuiKeyModFlags_(IntEnum):
    NONE = 0x0
    Ctrl = 0x1
    Shift = 0x2
    Alt = 0x4
    Super = 0x8

