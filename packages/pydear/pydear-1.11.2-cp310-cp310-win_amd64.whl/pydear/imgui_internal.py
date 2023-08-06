from typing import Type, Tuple, Union, Any, Iterable
import ctypes
from enum import IntEnum
from .impl.imgui_internal import *
from .imgui import ImVec2
class ImGuiContext(ctypes.Structure):
    pass
class ImRect(ctypes.Structure):
    _fields_=[
        ("Min", ImVec2), # ImVec2WrapType: ImVec2,
        ("Max", ImVec2), # ImVec2WrapType: ImVec2,
    ]
from enum import IntEnum

class ImGuiItemFlags_(IntEnum):
    NONE = 0x0
    NoTabStop = 0x1
    ButtonRepeat = 0x2
    Disabled = 0x4
    NoNav = 0x8
    NoNavDefaultFocus = 0x10
    SelectableDontClosePopup = 0x20
    MixedValue = 0x40
    ReadOnly = 0x80
    Inputable = 0x100

class ImGuiItemStatusFlags_(IntEnum):
    NONE = 0x0
    HoveredRect = 0x1
    HasDisplayRect = 0x2
    Edited = 0x4
    ToggledSelection = 0x8
    ToggledOpen = 0x10
    HasDeactivated = 0x20
    Deactivated = 0x40
    HoveredWindow = 0x80
    FocusedByTabbing = 0x100

class ImGuiInputTextFlagsPrivate_(IntEnum):
    ImGuiInputTextFlags_Multiline = 0x4000000
    ImGuiInputTextFlags_NoMarkEdited = 0x8000000
    ImGuiInputTextFlags_MergedItem = 0x10000000

class ImGuiButtonFlagsPrivate_(IntEnum):
    ImGuiButtonFlags_PressedOnClick = 0x10
    ImGuiButtonFlags_PressedOnClickRelease = 0x20
    ImGuiButtonFlags_PressedOnClickReleaseAnywhere = 0x40
    ImGuiButtonFlags_PressedOnRelease = 0x80
    ImGuiButtonFlags_PressedOnDoubleClick = 0x100
    ImGuiButtonFlags_PressedOnDragDropHold = 0x200
    ImGuiButtonFlags_Repeat = 0x400
    ImGuiButtonFlags_FlattenChildren = 0x800
    ImGuiButtonFlags_AllowItemOverlap = 0x1000
    ImGuiButtonFlags_DontClosePopups = 0x2000
    ImGuiButtonFlags_AlignTextBaseLine = 0x8000
    ImGuiButtonFlags_NoKeyModifiers = 0x10000
    ImGuiButtonFlags_NoHoldingActiveId = 0x20000
    ImGuiButtonFlags_NoNavFocus = 0x40000
    ImGuiButtonFlags_NoHoveredOnFocus = 0x80000
    ImGuiButtonFlags_PressedOnMask_ = 0x3f0
    ImGuiButtonFlags_PressedOnDefault_ = 0x20

class ImGuiComboFlagsPrivate_(IntEnum):
    ImGuiComboFlags_CustomPreview = 0x100000

class ImGuiSliderFlagsPrivate_(IntEnum):
    ImGuiSliderFlags_Vertical = 0x100000
    ImGuiSliderFlags_ReadOnly = 0x200000

class ImGuiSelectableFlagsPrivate_(IntEnum):
    ImGuiSelectableFlags_NoHoldingActiveID = 0x100000
    ImGuiSelectableFlags_SelectOnNav = 0x200000
    ImGuiSelectableFlags_SelectOnClick = 0x400000
    ImGuiSelectableFlags_SelectOnRelease = 0x800000
    ImGuiSelectableFlags_SpanAvailWidth = 0x1000000
    ImGuiSelectableFlags_DrawHoveredWhenHeld = 0x2000000
    ImGuiSelectableFlags_SetNavIdOnHover = 0x4000000
    ImGuiSelectableFlags_NoPadWithHalfSpacing = 0x8000000

class ImGuiTreeNodeFlagsPrivate_(IntEnum):
    ImGuiTreeNodeFlags_ClipLabelForTrailingButton = 0x100000

class ImGuiSeparatorFlags_(IntEnum):
    NONE = 0x0
    Horizontal = 0x1
    Vertical = 0x2
    SpanAllColumns = 0x4

class ImGuiTextFlags_(IntEnum):
    NONE = 0x0
    NoWidthForLargeClippedText = 0x1

class ImGuiTooltipFlags_(IntEnum):
    NONE = 0x0
    OverridePreviousTooltip = 0x1

class ImGuiLayoutType_(IntEnum):
    Horizontal = 0x0
    Vertical = 0x1

class ImGuiLogType(IntEnum):
    _None = 0x0
    _TTY = 0x1
    _File = 0x2
    _Buffer = 0x3
    _Clipboard = 0x4

class ImGuiAxis(IntEnum):
    _None = -0x1
    _X = 0x0
    _Y = 0x1

class ImGuiPlotType(IntEnum):
    _Lines = 0x0
    _Histogram = 0x1

class ImGuiPopupPositionPolicy(IntEnum):
    _Default = 0x0
    _ComboBox = 0x1
    _Tooltip = 0x2

class ImGuiDataTypePrivate_(IntEnum):
    ImGuiDataType_String = 0xb
    ImGuiDataType_Pointer = 0xc
    ImGuiDataType_ID = 0xd

class ImGuiNextWindowDataFlags_(IntEnum):
    NONE = 0x0
    HasPos = 0x1
    HasSize = 0x2
    HasContentSize = 0x4
    HasCollapsed = 0x8
    HasSizeConstraint = 0x10
    HasFocus = 0x20
    HasBgAlpha = 0x40
    HasScroll = 0x80
    HasViewport = 0x100
    HasDock = 0x200
    HasWindowClass = 0x400

class ImGuiNextItemDataFlags_(IntEnum):
    NONE = 0x0
    HasWidth = 0x1
    HasOpen = 0x2

class ImGuiKeyPrivate_(IntEnum):
    ImGuiKey_LegacyNativeKey_BEGIN = 0x0
    ImGuiKey_LegacyNativeKey_END = 0x200
    ImGuiKey_Gamepad_BEGIN = 0x269
    ImGuiKey_Gamepad_END = 0x281

class ImGuiInputEventType(IntEnum):
    _None = 0x0
    _MousePos = 0x1
    _MouseWheel = 0x2
    _MouseButton = 0x3
    _MouseViewport = 0x4
    _Key = 0x5
    _Text = 0x6
    _Focus = 0x7
    _COUNT = 0x8

class ImGuiInputSource(IntEnum):
    _None = 0x0
    _Mouse = 0x1
    _Keyboard = 0x2
    _Gamepad = 0x3
    _Clipboard = 0x4
    _Nav = 0x5
    _COUNT = 0x6

class ImGuiInputReadMode(IntEnum):
    _Down = 0x0
    _Pressed = 0x1
    _Released = 0x2
    _Repeat = 0x3
    _RepeatSlow = 0x4
    _RepeatFast = 0x5

class ImGuiActivateFlags_(IntEnum):
    NONE = 0x0
    PreferInput = 0x1
    PreferTweak = 0x2
    TryToPreserveState = 0x4

class ImGuiScrollFlags_(IntEnum):
    NONE = 0x0
    KeepVisibleEdgeX = 0x1
    KeepVisibleEdgeY = 0x2
    KeepVisibleCenterX = 0x4
    KeepVisibleCenterY = 0x8
    AlwaysCenterX = 0x10
    AlwaysCenterY = 0x20
    NoScrollParent = 0x40
    MaskX_ = 0x15
    MaskY_ = 0x2a

class ImGuiNavHighlightFlags_(IntEnum):
    NONE = 0x0
    TypeDefault = 0x1
    TypeThin = 0x2
    AlwaysDraw = 0x4
    NoRounding = 0x8

class ImGuiNavDirSourceFlags_(IntEnum):
    NONE = 0x0
    RawKeyboard = 0x1
    Keyboard = 0x2
    PadDPad = 0x4
    PadLStick = 0x8

class ImGuiNavMoveFlags_(IntEnum):
    NONE = 0x0
    LoopX = 0x1
    LoopY = 0x2
    WrapX = 0x4
    WrapY = 0x8
    AllowCurrentNavId = 0x10
    AlsoScoreVisibleSet = 0x20
    ScrollToEdgeY = 0x40
    Forwarded = 0x80
    DebugNoResult = 0x100
    FocusApi = 0x200
    Tabbing = 0x400
    Activate = 0x800
    DontSetNavHighlight = 0x1000

class ImGuiNavLayer(IntEnum):
    _Main = 0x0
    _Menu = 0x1
    _COUNT = 0x2

class ImGuiOldColumnFlags_(IntEnum):
    NONE = 0x0
    NoBorder = 0x1
    NoResize = 0x2
    NoPreserveWidths = 0x4
    NoForceWithinWindow = 0x8
    GrowParentContentsSize = 0x10
    ImGuiColumnsFlags_None = 0x0
    ImGuiColumnsFlags_NoBorder = 0x1
    ImGuiColumnsFlags_NoResize = 0x2
    ImGuiColumnsFlags_NoPreserveWidths = 0x4
    ImGuiColumnsFlags_NoForceWithinWindow = 0x8
    ImGuiColumnsFlags_GrowParentContentsSize = 0x10

class ImGuiDockNodeFlagsPrivate_(IntEnum):
    ImGuiDockNodeFlags_DockSpace = 0x400
    ImGuiDockNodeFlags_CentralNode = 0x800
    ImGuiDockNodeFlags_NoTabBar = 0x1000
    ImGuiDockNodeFlags_HiddenTabBar = 0x2000
    ImGuiDockNodeFlags_NoWindowMenuButton = 0x4000
    ImGuiDockNodeFlags_NoCloseButton = 0x8000
    ImGuiDockNodeFlags_NoDocking = 0x10000
    ImGuiDockNodeFlags_NoDockingSplitMe = 0x20000
    ImGuiDockNodeFlags_NoDockingSplitOther = 0x40000
    ImGuiDockNodeFlags_NoDockingOverMe = 0x80000
    ImGuiDockNodeFlags_NoDockingOverOther = 0x100000
    ImGuiDockNodeFlags_NoDockingOverEmpty = 0x200000
    ImGuiDockNodeFlags_NoResizeX = 0x400000
    ImGuiDockNodeFlags_NoResizeY = 0x800000
    ImGuiDockNodeFlags_SharedFlagsInheritMask_ = -0x1
    ImGuiDockNodeFlags_NoResizeFlagsMask_ = 0xc00020
    ImGuiDockNodeFlags_LocalFlagsMask_ = 0xc1fc70
    ImGuiDockNodeFlags_LocalFlagsTransferMask_ = 0xc1f870
    ImGuiDockNodeFlags_SavedFlagsMask_ = 0xc1fc20

class ImGuiDataAuthority_(IntEnum):
    Auto = 0x0
    DockNode = 0x1
    Window = 0x2

class ImGuiDockNodeState(IntEnum):
    _Unknown = 0x0
    _HostWindowHiddenBecauseSingleWindow = 0x1
    _HostWindowHiddenBecauseWindowsAreResizing = 0x2
    _HostWindowVisible = 0x3

class ImGuiWindowDockStyleCol(IntEnum):
    _Text = 0x0
    _Tab = 0x1
    _TabHovered = 0x2
    _TabActive = 0x3
    _TabUnfocused = 0x4
    _TabUnfocusedActive = 0x5
    _COUNT = 0x6

class ImGuiContextHookType(IntEnum):
    _NewFramePre = 0x0
    _NewFramePost = 0x1
    _EndFramePre = 0x2
    _EndFramePost = 0x3
    _RenderPre = 0x4
    _RenderPost = 0x5
    _Shutdown = 0x6
    _PendingRemoval__ = 0x7

class ImGuiTabBarFlagsPrivate_(IntEnum):
    ImGuiTabBarFlags_DockNode = 0x100000
    ImGuiTabBarFlags_IsFocused = 0x200000
    ImGuiTabBarFlags_SaveSettings = 0x400000

class ImGuiTabItemFlagsPrivate_(IntEnum):
    ImGuiTabItemFlags_SectionMask_ = 0xc0
    ImGuiTabItemFlags_NoCloseButton = 0x100000
    ImGuiTabItemFlags_Button = 0x200000
    ImGuiTabItemFlags_Unsorted = 0x400000
    ImGuiTabItemFlags_Preview = 0x800000

