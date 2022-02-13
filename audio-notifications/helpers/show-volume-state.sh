#!/bin/bash

mute_state=$(pacmd list-sinks | grep muted | grep -Eo "yes|no")
volume=$(amixer get Master | grep -Eo -m 1 '[[:digit:]]{1,3}%' | tr -d %)
icon=''

if [ "$mute_state" = "no" ] ; then
    if [ $volume -ge 0 ] && [ $volume -le 33 ] ; then
        icon='/usr/share/icons/HighContrast/48x48/status/audio-volume-low.png'
    elif [ $volume -gt 33 ] && [ $volume -le 66 ] ; then
        icon='/usr/share/icons/HighContrast/48x48/status/audio-volume-medium.png'
    else
        icon='/usr/share/icons/HighContrast/48x48/status/audio-volume-high.png'
    fi
else
    icon='/usr/share/icons/HighContrast/48x48/status/audio-volume-muted.png'
fi

touch -a '/tmp/volume-notification-id'
volume_notification_id=$(cat /tmp/volume-notification-id)

if [ -z $volume_notification_id ] ; then
    volume_notification_id=0
    echo $volume_notification_id
fi

new_id=$(gdbus call --session --dest org.freedesktop.Notifications --object-path /org/freedesktop/Notifications --method org.freedesktop.Notifications.Notify volume-notification $volume_notification_id $icon '' ${volume}% [] {} 500 | grep -Eo [[:digit:]]*, | tr -d ,)

echo $new_id > /tmp/volume-notification-id
