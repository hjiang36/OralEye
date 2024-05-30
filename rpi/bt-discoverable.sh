#!/bin/bash
sleep 10

hciconfig hci0 up
hciconfig hci0 piscan
hciconfig hci0 sspmode 1
hciconfig hci0 leadv 3

btmgmt -i hci0 connectable yes
btmgmt -i hci0 bondable yes
btmgmt -i hci0 power on
btmgmt -i hci0 name "OralEye"
btmgmt -i hci0 pairable yes

hciconfig hci0 leadv 3

bluetoothctl << EOF
agent on
default-agent
discoverable on
pairable on
EOF
