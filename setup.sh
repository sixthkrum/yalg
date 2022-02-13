#!/bin/bash
# installs a systemd service

service_name="yalg.service"

if [ "$(systemctl list-units --full -all | grep -oF "$service_name")" = "$service_name" ] 
then
    echo "service with this name already exists, please change the service name here and in the uninstall script to proceed"
    exit
fi

rm -f $service_name
touch -a $service_name
echo '[Unit]' >> ./$service_name
echo 'Description=yet another libinput gestures service' >> ./$service_name
echo '[Service]' >> ./$service_name
echo 'Type=idle' >> ./$service_name
echo "User=${USER}" >> ./$service_name
echo 'SupplementaryGroups=input' >> ./$service_name
echo "WorkingDirectory=${PWD}" >> ./$service_name
echo "ExecStart=/usr/bin/python3 ${PWD}/main.py" >> ./$service_name
echo '[Install]' >> ./$service_name
echo 'WantedBy=multi-user.target' >> ./$service_name

sudo mv $service_name /etc/systemd/system
sudo systemctl enable $service_name
sudo systemctl start $service_name

echo
echo "installed"