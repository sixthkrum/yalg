from enum import IntEnum
from local_modules.libinput_mappers import GestureSwipeUpdate

# will only be ever cleaning up as much data as needed, the rest needs cleanup too
def cleanup_swipe_event_list(event_list):
    # remove + from the start and s from the end
    event_list[GestureSwipeUpdate.TIME] = event_list[GestureSwipeUpdate.TIME][1:-1]
    
    # check if dy and dx are in the same entry and seperate them
    dx_dy_split = event_list[GestureSwipeUpdate.DX].split('/')

    if dx_dy_split[1] != '':
        event_list[GestureSwipeUpdate.DX] = dx_dy_split[0]
        event_list.insert(GestureSwipeUpdate.DY, dx_dy_split[1])
    
    #otherwise remove / from dx
    else:
        event_list[GestureSwipeUpdate.DX] = event_list[GestureSwipeUpdate.DX][:-1]

# transform raw dy value into volume
def volume(dy):
    return 0.5 + (dy / 20) * 2