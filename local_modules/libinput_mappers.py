from enum import IntEnum
from collections import defaultdict

# mapper for gesture swipe update event data 
class GestureSwipeUpdate(IntEnum):
    DEVICE_NUM = 0
    TYPE = 1
    # cleaup needed for entry below
    TIME = 2
    NUM_FINGERS = 3
    # cleanup needed for all entries below
    DX = 4
    DY = 5
    DX_UNACCEL = 6
    DY_UNACCEL = 7

# mapper for common fields in the events
class CommonEvent(IntEnum):
    DEVICE_NUM = 0
    TYPE = 1
    TIME = 2

# only states written here are actionable
class TouchpadState(IntEnum):
    # After end and before start of an actionable state
    # not applicable
    NA = 0
    # gesture swipe begin
    GestureSwipeBegin = 1
    # gesture swipe update
    GestureSwipeUpdate = 2
    # gesture swipe end
    GestureSwipeEnd = 3

# keep mapper names as <thing being mapped>_<left hand side>_<right hand side>
# maps type string in libinput to touch pad state
type_libinput_touchpad = defaultdict(lambda: TouchpadState.NA)
type_libinput_touchpad["GESTURE_SWIPE_BEGIN"] = TouchpadState.GestureSwipeBegin
type_libinput_touchpad["GESTURE_SWIPE_UPDATE"] = TouchpadState.GestureSwipeUpdate
type_libinput_touchpad["GESTURE_SWIPE_END"] = TouchpadState.GestureSwipeEnd 


# maps - (up) motion on trackpad to volume up (+) and volume down (-) vice versa during get
sign_libinput_alsa = defaultdict(lambda: '-')
sign_libinput_alsa['-'] = '+'