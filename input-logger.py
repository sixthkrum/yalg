import sys
import os
import subprocess
from enum import IntEnum
import io

# will only be ever cleaning up as much data as needed, the rest needs cleanup too
def cleanup_swipe_event_list(event_list):
    # remove + from the start and s from the end
    event_list[GSUEDM.TIME] = event_list[GSUEDM.TIME][1:-1]
    
    # check if dy and dx are in the same entry and seperate them
    dx_dy_split = event_list[GSUEDM.DX].split('/')

    if dx_dy_split[1] != '':
        event_list[GSUEDM.DX] = dx_dy_split[0]
        event_list.insert(GSUEDM.DY, dx_dy_split[1])
    
    #otherwise remove / from dx
    else:
        event_list[GSUEDM.DX] = event_list[GSUEDM.DX][:-1]

# mapper for event data from libinput
# Gesture Swipe Update Event Data Mapper
class GSUEDM(IntEnum):
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
# Common Event Data Mapper
class CEDM(IntEnum):
    DEVICE_NUM = 0
    TYPE = 1
    TIME = 2

# only states written here are actionable
class TouchpadState(IntEnum):
    # After end and before start of an actionable state
    # not applicable
    NA = 0
    # gesture swipe begin
    GSB = 1
    # gesture swipe update
    GSU = 2
    # gesture swipe end
    GSE = 3


# maps types of input to their string in libinput
libinput_type_mapper = {
    "GESTURE_SWIPE_BEGIN" : TouchpadState.GSB,
    "GESTURE_SWIPE_UPDATE" : TouchpadState.GSU,
    "GESTURE_SWIPE_END" : TouchpadState.GSE
}

# handles swipe events
def handle_swipe_event(event):
    cleanup_swipe_event_list(event)
    if event[GSUEDM.NUM_FINGERS] == '3':
        return
    

# maps state type to function to call
libinput_state_function_mapper = {
    TouchpadState.GSB: handle_swipe_event
}

# replace
# maps - (up) motion on trackpad to volume up (+) and volume down (-) vice versa during get
libinput_to_alsa_sign_dict = {
    '-' : '+'
}

# here for poc need to move to proper place
dy_threshold = 0

# invoke libinput debug-events here
libinput_process = subprocess.Popen(["sudo", "stdbuf", "-oL", "libinput", "debug-events", "--device", "/dev/input/event4"], bufsize = 1, stdout = subprocess.PIPE, text = True)

while True:
    event_data = libinput_process.stdout.readline().split()
    current_state = libinput_type_mapper.get(event_data[CEDM.TYPE], TouchpadState.NA)

    # handling input here, should be in a function mapper in the future
    if current_state == TouchpadState.GSB:
        if event_data[GSUEDM.NUM_FINGERS] == '4':
            event_data = libinput_process.stdout.readline().split()
            vol = 0

            while libinput_type_mapper.get(event_data[CEDM.TYPE], TouchpadState.NA) != TouchpadState.GSE and libinput_type_mapper.get(event_data[CEDM.TYPE], TouchpadState.NA) != TouchpadState.NA:
                cleanup_swipe_event_list(event_data)
                
                # set volume depending on dy
                # define some threshold values too
                dy_raw = abs(int(float(event_data[GSUEDM.DY])))
                vol_sign = libinput_to_alsa_sign_dict.get(event_data[GSUEDM.DY][0], '-')
                
                if dy_raw > dy_threshold:
                    # some equation to make volume scrolling feel better
                    vol += 0.5 + (dy_raw / 20) * 3

                    if vol > 1:
                        os.system(f"amixer --quiet -D pulse sset Master {int(vol)}%{vol_sign}")
                        os.system("./audio-notifications/helpers/show-volume-state.sh")
                        vol = vol - int(vol)

                event_data = libinput_process.stdout.readline().split()
