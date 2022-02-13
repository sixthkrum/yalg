import sys
import os
import subprocess
from collections import defaultdict

from local_modules.libinput_mappers import TouchpadState, CommonEvent, GestureSwipeUpdate, type_libinput_touchpad, sign_libinput_alsa
from local_modules.utils import cleanup_swipe_event_list, volume
from local_modules.config import config

# handles swipe events
def handle_swipe_event(event):
    if event[GestureSwipeUpdate.NUM_FINGERS] == '4':
        event_data = libinput_process.stdout.readline().split()
        vol = 0
        dy_threshold = int(config['GESTURE_SWIPE_FOUR_FINGER']['DY_THRESHOLD'])

        while type_libinput_touchpad.get(event_data[CommonEvent.TYPE], TouchpadState.NA) != TouchpadState.GestureSwipeEnd and type_libinput_touchpad.get(event_data[CommonEvent.TYPE], TouchpadState.NA) != TouchpadState.NA:
            cleanup_swipe_event_list(event_data)
            
            # set volume depending on dy
            # define some threshold values too
            dy_raw = abs(int(float(event_data[GestureSwipeUpdate.DY])))
            vol_sign = sign_libinput_alsa.get(event_data[GestureSwipeUpdate.DY][0], '-')
            
            if dy_raw > dy_threshold:
                # some equation to make volume scrolling feel better
                vol += volume(dy_raw)

                if vol > 1:
                    # could do this better in an independent shell script
                    os.system(f"export DISPLAY=:0 && export XDG_RUNTIME_DIR=/run/user/$(id -u) && amixer --quiet -D pulse sset Master {int(vol)}%{vol_sign}")
                    os.system("./audio-notifications/helpers/show-volume-state.sh")
                    vol = vol - int(vol)

            event_data = libinput_process.stdout.readline().split()

# maps touchpad state to function to call
state_function_mapper = defaultdict(lambda: lambda *args: 0)
state_function_mapper[TouchpadState.GestureSwipeBegin] = handle_swipe_event

# invoke libinput debug-events here
libinput_process = subprocess.Popen(["stdbuf", "-oL", "libinput", "debug-events", "--device", f"{config['GENERAL']['DEVICE']}"], bufsize = 1, stdout = subprocess.PIPE, text = True)

# main loop, read events and return here after
while True:
    event_data = libinput_process.stdout.readline().split()
    current_state = type_libinput_touchpad.get(event_data[CommonEvent.TYPE], TouchpadState.NA)
    state_function_mapper[current_state](event_data)