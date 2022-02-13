# xfce4 audio notifications
xfce4 bash scripts for volume control, with synchronous notifications for changes

### usage
Make sure you have high contrast 48x48 icons installed (at /usr/share/icons/HighContrast/48x48/) or change the paths for the icons in helpers/show-volume-state.sh

Hotkey the scripts for toggling, increasing and decreasing the volume using the keyboard settings menu.

### notes
Uses freedesktop notifications and should work for other distros too (should just need the icon paths changed at most). 

But if you are using ubuntu and notify-osd do not bother using this and use notify-osd with the x-canonical-private-synchronous hint instead.
