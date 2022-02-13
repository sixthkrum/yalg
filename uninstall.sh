#!/bin/bash
# uninstalls the systemd service

service_name="yalg.service"

read -p "enter 'y' to proceed: " -n 1 -r
if ! [ $REPLY = 'y' ]
then
    echo
    echo "exiting"
    exit
fi

echo

sudo systemctl stop $service_name
sudo systemctl disable $service_name
sudo rm /etc/systemd/system/$service_name
sudo rm /etc/systemd/system/multi-user.target.wants/$service_name
sudo systemctl daemon-reload
sudo systemctl reset-failed

echo
echo "uninstalled"